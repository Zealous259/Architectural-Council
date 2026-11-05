# Architectural Council (v3.1)

Seven architects with incompatible convictions and a neutral chair review a design, a model, a folio or a text in one subagent pass, and the report comes back as text in the session. No files, no PDF. A Quick length gives about 500 words from the same board.

## Files

| File | Role |
|---|---|
| `skills/architectural-council/SKILL.md` | The controller: how to write the brief, run the board, check and relay |
| `agents/arch-council.md` | The board: protocol, report template, the seven lens cards and the chair. Tools: Read only. It starts without the user's CLAUDE.md files (`omitClaudeMd: true`) |
| `skills/architectural-council/council_cost.py` | Prints the token cost of every council run on this machine, read from the subagent transcripts |

## What a run produces

1. **Lenses (sealed).** Seven analyses in voice. Each has its problems, every claim tagged `[seen]`, `[brief]`, `[known]` or `[assumed]`; one fact from its own field that the brief does not contain; a generative **Move**; and one **Ask** (a question, or a view to check by eye).
2. **Collisions.** Three or four real conflicts: attack, reply, HELD or SHIFTED, then a **Third move** that answers both lenses, or "none: the conflict is real" with the choice the designer has to make.
3. **Risk register.** Convergent risks (only when lenses stand on different grounds; escalated one step) and the lens-unique ones worth keeping.
4. **Verdicts.** Approve, conditional or reject per lens, with the condition that would earn approval, and a tally.
5. **Synthesis.** A status by rule, a roadmap tagged `in brief` or `lens`, the strongest direction (assembled from the members' moves), dissent, and limits (what was not seen, what the verdict leans on, and the one question no lens on the roster would ask).

The roster: Kovács (parametricist), Tanaka (phenomenologist), Rossi (typologist), Metzger (tectonic rationalist), Okonkwo (critical regionalist), Chen (social ecologist), Berg (speculative futurist), chaired by Whitmore (no opinions, no vote). Guest lenses (a tutor, a named architect, a client) can be added in the brief.

## Why one call

v1 (April 2026) ran six phases across 20 to 48 subagents per review and wrote a PDF. Measured runs cost 0.77M to 6.5M tokens, three debate rounds moved no position, and the reviewers saw a description of the images rather than the images. A general-purpose subagent carries the whole tool and skill roster before it reads a word, so the cost was the number of spawns, not the prompts. v3 runs the whole board in one call to a Read-only agent that reads the files itself. v3.1 drops the user's CLAUDE.md and memory index from the board's context and adds rules for the limits of one model writing seven voices.

## Measured cost (Nov 2026)

From the subagent transcripts: input including cache reads and writes, plus output. The same brief-only review each time, except the two image rows.

| Version | Calls | Tokens |
|---|---|---|
| v1, six phases | 21 to 48 subagents | 0.77M to 6.5M |
| v3.0 | 1 | 29.7k |
| v3.0, report written twice (see Traps) | 1 (2 API calls) | 66.6k |
| v3.1 | 1 | 15.8k to 16.1k (3 runs) |
| v3.0, four images and an 8-question checklist | 1 (2 turns) | 90.5k |
| v3.1, the same images and checklist | 1 (2 turns) | 79.0k |
| v3.1, Quick length, brief only | 1 | 11.0k |

## Known limits, and how v3.1 contains them

| Limit | Contained by | What remains |
|---|---|---|
| One model writes all seven lenses | A risk is convergent only when lenses reach it on different grounds; lenses may not lead with the same point; Limits names the question no lens on the roster would ask | Real independence needs a context per lens, at least 16k tokens each, and separate agents still share one model's priors |
| How a space looks or feels cannot be seen | Such a judgement rests on a measure from the brief or the files, or becomes the lens's Ask, a view to check by eye. Moves are exempt | The feeling stays unjudged; the numbers become checkable |
| Facts from memory (`[known]`) can be wrong | They never carry a CRITICAL, the status or a roadmap step alone; no clause numbers, page numbers or quotes from memory; no ranking without its comparison set | They stay unverified, but none carries a decision |

## Traps

- **The report written twice.** If the board writes its report as a text reply, the harness refuses it and makes it rewrite the whole report into its hand-back call: a second full pass (66.6k against 29.7k on the same brief). The board's first paragraph sends the report straight into the hand-back.
- **The user's instructions in every call.** Subagents receive the user's CLAUDE.md and memory index (about 10k tokens on the machine this was built on, half of a brief-only run's starting context). `omitClaudeMd: true` in the agent's frontmatter dropped both.
- **Outside facts vanish if over-restricted.** The first draft of v3.1 limited what `[known]` facts may carry, and the lenses stopped bringing any. The template's "Beyond the brief" line brought them back.
- **Opus.** A council agent built the same way thought past the 128k output limit on Opus without writing a report. Keep the board on its own model; depth comes from a follow-up round.
- **Reloads.** An edited agent file may not load until a new session, whatever the docs say about seconds. A headless `claude -p` run loads the current file, so it can test an edit; give it `--tools Agent Read`, since the board needs Read. `council_cost.py` shows which board each run received.

## Changing the board

Each lens is one paragraph in `agents/arch-council.md`: conviction, first questions, tests, terms, contempt, and whom it attacks. Edit the paragraph, or add guest lenses in the brief for a one-off panel. Keep the cards opinionated and in conflict: that is what the collisions feed on. The chair must never acquire a design opinion.
