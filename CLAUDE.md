# CLAUDE.md: architectural-council

## Plugin overview

An architectural review board of seven architects with incompatible convictions and a neutral chair, run as ONE subagent call. It reviews a design, model, folio or text and returns a text report in the session: sealed lens analyses that each end in a generative move, collisions that end in a third move, a risk register, verdicts with conditions, and a synthesis with a status, a roadmap and the strongest direction. A Quick length gives about 500 words. No grades, no files.

## File structure

| File | What it controls |
|------|-----------------|
| `skills/architectural-council/SKILL.md` | The controller only: how the main session writes the brief, spawns the agent, checks and relays |
| `agents/arch-council.md` | The board itself: ground rules, the five sections, the report template, the chair and the seven lens cards |
| `skills/architectural-council/README.md` | History, the measured token costs and the traps |
| `skills/architectural-council/council_cost.py` | The cost of every council run on the machine, from the subagent transcripts |

## Rules for agents working here

- Behaviour changes go in `agents/arch-council.md`. One card per lens, one paragraph each. The cards are meant to conflict: do not moderate their positions.
- `SKILL.md` stays small: everything it holds enters the main context on every run.
- The chair (Whitmore) never gives a design opinion and adds nothing the seven did not say.
- One call. Never add a phase that spawns more agents: the cost scales with spawns and turns, not with words.
- Keep the agent's tools to Read and keep `omitClaudeMd: true`.
- No em dashes or en dashes in any file here.
- After editing the agent file, start a new session before testing, then check the board version a run received with `council_cost.py`.
