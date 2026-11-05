# Architectural Council

An architectural review board for Claude Code in one agent call. Seven architect lenses with incompatible convictions and a neutral chair review a design, model, folio or text, and the report comes back as text in the session: sealed lenses that each propose a move, collisions that end in a third move, a risk register, verdicts with conditions, and a synthesis with a status, a roadmap and the strongest direction. "lite" or "quick crit" gives a 500-word read from the same board.

## Install

By hand: copy `agents/arch-council.md` to `~/.claude/agents/` and the folder `skills/architectural-council/` to `~/.claude/skills/`, then start a new Claude Code session (agent files load at startup).

As a plugin: this folder is a plugin root (`.claude-plugin/plugin.json`). Put it in a local plugin marketplace and install `architectural-council` from there. The agent may then be listed as `architectural-council:arch-council`; the skill uses whichever name the agent list shows.

## Files

| File | Role |
|---|---|
| `skills/architectural-council/SKILL.md` | The controller: how the main session writes the brief, runs the board, checks and relays |
| `agents/arch-council.md` | The board: protocol, report template, the seven lens cards and the chair |
| `skills/architectural-council/README.md` | History, measured token costs and traps |
| `skills/architectural-council/council_cost.py` | Prints the token cost of every council run on the machine, from the local subagent transcripts |

## Security

- The board's only tool is Read, and it reads only the files the brief lists. It cannot write files, run commands or reach the network.
- It starts without the user's CLAUDE.md files (`omitClaudeMd: true`), so personal instructions and memory stay out of its context.
- `council_cost.py` reads local transcripts and prints token counts and run descriptions to the terminal. It makes no network calls and runs no commands.

## Version

v3.1, November 2026. It replaces v1 (April 2026), which ran six phases across 20 to 48 subagents per review and wrote a PDF.
