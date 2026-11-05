"""Token cost of every Architectural Council run on this machine.

Claude Code keeps each subagent's transcript under ~/.claude/projects. This reads
them, picks the council runs (the arch-council agent, and the general-purpose
fallback whose description starts with "Architectural council"), and prints one
row per run:

- board: the board version the run actually received (from the prompt it
  recorded; an edited agent file is not always reloaded mid-session)
- calls, context (input plus cache reads and writes), output, total
- forced: times the harness had to force the hand-back. The board wrote its
  report as a text reply, then rewrote all of it into SubagentHandback: a second
  full pass (5 Nov 2026: 66.6k against 29.7k on the same brief). A text brief
  should take 1 call, an image brief 2.
- instr: characters of CLAUDE.md and memory index handed to the run (25,800 on
  5 Nov 2026; `omitClaudeMd: true` in the agent file should cut it)

Streamed lines repeat a message, so each message counts once, at its largest usage.

    python council_cost.py
"""
import json
import statistics
from pathlib import Path

ROOT = Path.home() / ".claude" / "projects"
VERSIONS = [("Prefer this building's or this type's own history", "v3.1"),
            ("never whether you bring one", "v3.1-r"), ("Judge space through a number", "v3.1-d"),
            ("You write no files", "v3.0")]


def council_runs():
    for meta in ROOT.glob("*/*/subagents/agent-*.meta.json"):
        try:
            info = json.loads(meta.read_bytes().decode("utf-8"))
        except (OSError, ValueError):
            continue
        kind = info.get("agentType", "")
        desc = info.get("description", "")
        if kind != "arch-council" and not desc.startswith("Architectural council"):
            continue
        log = meta.with_name(meta.name[: -len(".meta.json")] + ".jsonl")
        if log.exists():
            yield kind, desc, log


def usage(log):
    calls, first, forced, version, instr = {}, "", 0, "?", None
    for line in log.read_bytes().decode("utf-8", "replace").splitlines():
        if version == "?":
            version = next((v for marker, v in VERSIONS if marker in line), "?")
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        first = first or rec.get("timestamp", "")
        att = rec.get("attachment") if isinstance(rec.get("attachment"), dict) else {}
        if instr is None and att.get("type") == "instructions":
            instr = sum(len(f.get("content") or "") for f in att.get("files", []))
        if rec.get("type") == "user" and "[handback-send-enforce]" in line:
            forced += 1
        msg = rec.get("message") if isinstance(rec.get("message"), dict) else {}
        use = msg.get("usage")
        if rec.get("type") != "assistant" or not use:
            continue
        ctx = (use.get("input_tokens", 0) + use.get("cache_creation_input_tokens", 0)
               + use.get("cache_read_input_tokens", 0))
        out = use.get("output_tokens", 0)
        key = msg.get("id") or len(calls)
        old = calls.get(key, (0, 0))
        calls[key] = (max(old[0], ctx), max(old[1], out))
    ctx = sum(c for c, _ in calls.values())
    out = sum(o for _, o in calls.values())
    return first, version, len(calls), ctx, out, forced, instr or 0


def main():
    rows = sorted((*usage(log), kind, desc) for kind, desc, log in council_runs())
    print(f"{'started (UTC)':16}  {'agent':15}  {'board':6}  {'calls':>5}  {'context':>8}  "
          f"{'output':>7}  {'total':>8}  {'forced':>6}  {'instr':>6}  description")
    for first, version, n, ctx, out, forced, instr, kind, desc in rows:
        print(f"{first[:16]:16}  {kind[:15]:15}  {version:6}  {n:5}  {ctx:8,}  {out:7,}  "
              f"{ctx + out:8,}  {forced:6}  {instr:6,}  {desc}")
    own = [r[3] + r[4] for r in rows if r[7] == "arch-council"]
    if own:
        print(f"\narch-council runs: {len(own)}, median {statistics.median(own):,.0f} tokens")


if __name__ == "__main__":
    main()
