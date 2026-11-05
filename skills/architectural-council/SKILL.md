---
name: architectural-council
description: The full Architectural Council in one subagent pass. Seven architect lenses (Kovács parametricist, Tanaka phenomenologist, Rossi typologist, Metzger tectonic rationalist, Okonkwo critical regionalist, Chen social ecologist, Berg speculative futurist) chaired by Whitmore. Sealed analyses that each end in a generative move, collisions that end in a third move, a convergent risk register, verdicts with conditions, a status, a roadmap and the strongest direction. Text in the session; no files, no PDF. Use for "archi council", "architectural council", "present it to the council", "run the council", "council this" on any design, model, drawing, folio, plan or brief; "lite", "quick council" or "quick crit" get the same board at a Quick length of about 500 words. About 16k tokens a brief-only run (measured).
---

# Architectural Council (v3.1, Nov 2026)

The board lives in the agent `arch-council`, whose file is `~/.claude/agents/arch-council.md` (in a plugin install, `agents/arch-council.md` at the plugin root, two folders above this skill). Its system prompt holds the protocol, the report template and the seven lens cards, so almost nothing enters the main context. Do not read the agent file unless the fallback in step 2 needs it.

## 1. Write the brief

One block, at most about 300 words. Neutral: state the weak and unfinished parts too, never sell the work.

- **What and stage:** type, course or client, design stage, what the user wants from the crit.
- **Questions:** anything the user asked the council to answer, as a checklist in their words. The board answers every one or lists it under Limits.
- **Intent:** the thesis or driver, in the designer's terms.
- **Site facts:** city, hemisphere, which face takes the hot afternoon sun, the main faces in compass terms (never "left side"), slope and datum.
- **Program and users.**
- **Key moves:** form, structure, material, generative method.
- **Constraints and assessment:** deadline, brief criteria, the tutor's stated direction.
- **Numbers:** each says what it measures and where (site-wide, or at the entry). A bare "8 columns at 971.6 mm" was read three ways in testing.
- **Not shown:** what the council cannot see, so it does not invent it.
- **Files:** absolute paths, at most 8 (images, PDFs, notes). A folio or long PDF goes as contact sheets (8 to 12 pages per sheet, page numbers burned in). A live 3D model goes as captured PNG views: the council reads images, never a model file.
- **Guest lenses** (optional): a tutor, a named architect or the client, one line each.

For a text (essay, speech, report) or a folio, the same block states what it argues, for whom, and its word or page count; skip the site lines that do not apply.

If key geometry or structure is unclear and no file shows it, ask the user one question first. Otherwise do not wait for confirmation: the report opens with the brief.

## 2. Run it

One Agent call: `subagent_type: "arch-council"` (a plugin install may list it as `architectural-council:arch-council`; use the name the agent list shows), `description: "Architectural council"`, prompt = the brief block and nothing else. No opinion of yours and none of the session's history: the council stays independent of whoever built the work.

**Quick** (the user says lite, quick council or quick crit): end the brief with the line `Length: Quick`; same call. The board writes about 500 words: a line per lens, the one or two real collisions, the status and the one change that would help most.

Keep the board on its own model even when asked for a deeper review: a council agent built the same way thought past the 128k output limit on Opus without writing a report (tested Nov 2026). Depth comes from a follow-up round (step 4).

Fallback when no such agent type is listed (installed during this session, before a restart, or missing): Read the agent file and spawn ONE `general-purpose` agent with `model: "sonnet"`, prompt = the file's body below the frontmatter, then the brief. Same report, but about 50k more tokens of spawn overhead per turn (measured).

## 3. Check, then relay

1. **Depth gate** (full length only). Every checklist question answered or under Limits, a Move in every lens, three or four collisions each ending in a third move or "none: the conflict is real", a status by rule. If one is missing, rerun once and say why.
2. Fact-check the `[seen]` and `[brief]` claims the status and the roadmap stand on, against the model or the files. A decision carried by a `[known]` or `[assumed]` claim alone breaks the board's rule 2: flag it. Do not edit the report: add a short **Fact check** list under it.
3. Relay the report verbatim, as text in the session. No file, no PDF.
4. Tag per the working protocol if CLAUDE.md defines one, once and not per line: what the council says about how a space will feel, sound, read or photograph was judged without seeing it (its numbers are checkable, the feeling is not); every `[known]` line, and any precedent, date or standard it names, is unverified; a convergent risk has several grounds, not several independent judges.

## 4. Follow-ups

A second round, or depth on one lens: one more `arch-council` call with the brief, the previous report, every correction from your fact check, and the specific question. Never rerun all seven unless asked.

## Cost (measured Nov 2026)

About 15k to 16k tokens for a brief-only run, 11k at Quick length and about 79k with four images and an eight-question checklist (measured). `council_cost.py` in this folder prints every council run on the machine.

## Changing the board

Edit a lens card in the agent file (one paragraph each). An edited agent file may not load until a new session. For a one-off panel, pass guest lenses in the brief instead. History, costs and traps: `README.md` in this folder.
