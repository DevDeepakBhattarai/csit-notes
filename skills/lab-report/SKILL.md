---
name: lab-report
description: Build a complete B.Sc. CSIT lab report from a question paper in any format (PDF, PPTX, DOCX, image, pasted text). Reads and extracts the questions, detects the ones that depend on the student's name or roll number, asks whether the report is fully printable or only the outputs get printed, writes short theory + algorithm + correct code (or SQL), verifies every answer by actually running it, and renders a paginated A4 HTML ready to print. Use whenever the user mentions a lab report, lab assignment, lab work, lab sheet, or hands over a question paper to answer.
---

# Lab report builder

You are producing a **student lab report**, not production software. The grader
reads it once and signs the index page. Speed and literal correctness are the
whole job.

The deliverable is one self-contained HTML file, opened in a browser, printed to
A4. Templates in `templates/` already handle pagination, the index page, the fake
Windows terminal, and the phpMyAdmin result panes — you only ever fill in a JSON
array of items.

## Step 0 — Pick the variant (ask, once)

The user names the questions file (or pastes the questions). Before writing
anything, ask with **AskUserQuestion** — one question, three options:

| Option | When | Template |
|---|---|---|
| **Fully printable** | Everything is printed: question, theory, algorithm, code, output. Their AI / OS / TOC reports are this. | `templates/printable.html` |
| **Output only (hand-written code)** | The code has to be copied out by hand on paper; only the terminal screenshots get printed. Their TOC "Writing" report is this. | `templates/output-only.html` |
| **Output only (SQL / phpMyAdmin)** | Same, but the answers are SQL and the printed evidence is a phpMyAdmin result pane, with blank space above each pane to hand-write the query. Their DBMS Part 2 report is this. | `templates/sql-output.html` |

Do not ask anything else. Student name / roll / section are typed into the input
boxes at the top of the generated page at print time — write `{NAME}`, `{ROLL}`,
`{SECTION}` (and `{{FIRST_LETTER}}`, `{{NAME_SLUG}}` in SQL) into the data
instead of hard-coding a name. If the user already stated the variant, skip the
question entirely.

## Step 1 — Read the question paper

```bash
python .claude/skills/lab-report/scripts/extract_questions.py "<file>"
```

Handles PDF / PPTX / DOCX / TXT, prints the text per page or slide, then a
`STUDENT-SPECIFIC` section (every line mentioning the student) and an `IMAGES`
section. If pages carry images, **Read those pages with the Read tool** — the
text dump loses family trees, DFA drawings and topology diagrams. For a photo or
scan of a question paper, just Read it directly.

Then:

- Copy the **question text verbatim** into `question`, keeping the paper's own
  numbering (`1(a)`, `II.4`, `4A-08`). The grader matches numbers.
- Read the **instructions block** at the top of the paper — it carries global
  requirements that apply to every single answer: a footer `printf`, "file path
  must contain your name", "one side of A4", "index page attached". Obey all of
  them.
- Count the questions and state the count back to the user. Never silently drop
  a sub-question.

## Step 2 — Mark the student-specific questions

Anything that varies per student must become a token, never a baked-in value.
See `references/authoring-rules.md` for the full table. The common ones here:

| Paper says | Do |
|---|---|
| "Print your name, roll number and lab number at the end in each output" | Append the footer `printf` block to every program, using `{NAME}` / `{ROLL}` / `{SECTION}` |
| "file path will contain your name" | Nothing — the terminal title bar is built from the name input already |
| "city whose name starts with the first letter of your name" | `{{FIRST_LETTER}}` in the SQL + a `dynamic` entry so the rows re-filter live |
| "create a database `<your-name>dbms1`" | `{{NAME_SLUG}}dbms1` |
| "add two categories of your choice" | Pick something sane once and keep it stable across related questions |

## Step 3 — Write the answers

Read `references/authoring-rules.md` before writing the first item. The rules
that matter most:

- **Answer exactly the question asked.** Nothing extra. No `ORDER BY` that was
  not requested, no input validation nobody asked for, no menu loops, no error
  handling for cases the question does not mention.
- **Theory: 2–3 sentences.** **Algorithm: 3–6 short steps.** These are filler
  the grader skims; long ones only burn paper and your time.
- **Code must compile and run and be short.** Hard-coded sample data beats
  `scanf` unless the question says "user input".
- Reuse one dataset across a whole lab so the outputs stay coherent.

## Step 4 — Verify. Actually run it.

```bash
# C / C++ / Python items: compile, run, diff against the declared output
python .claude/skills/lab-report/scripts/verify_c.py <report.html>
python .claude/skills/lab-report/scripts/verify_c.py <report.html> --write   # paste the real stdout in

# SQL items: fresh database per question, seeded from the setup script
python .claude/skills/lab-report/scripts/verify_sql.py <report.html> --setup setup.sql --letter D
```

`--write` is the fast path: write the code, let the compiler produce the real
output, and the `output` field is true by construction.

If `verify_c.py` prints `TOOLCHAIN UNAVAILABLE`, or MySQL is not running, then
**nothing is verified**. Say so plainly in your final message and tell the user
which command to run themselves. Never describe hand-derived output as tested.

## Step 5 — Render and check the pages

```bash
python .claude/skills/lab-report/scripts/check_pages.py <report.html>
# -> PAGES=56 OVERFLOW=none
```

`OVERFLOW` must be `none`; any listed page is being silently clipped on paper —
shorten that block or split it. (Applies to `printable.html` and
`sql-output.html`; `output-only.html` packs its pages at print time instead.)

## Step 6 — Hand it over

Save next to the question paper: `4th Sem/<Subject>/<Subject>_Lab_Report.html`
(add `_Part2` etc. when the paper is split). Then tell the user, briefly:

- the file path and how many questions and A4 pages it came to
- what was verified and what was not
- print settings: **A4, margins None, Background graphics ON**

## Non-negotiables

1. Do what the question asks, literally. Nothing more.
2. Every question on the paper gets an answer, in the paper's numbering.
3. Never claim verified output you did not actually run.
4. Student-specific values are tokens, never hard-coded.
5. Theory and algorithm stay short.

## Files

- `references/authoring-rules.md` — literalism, theory/algorithm/code/SQL rules, output rules
- `references/variants.md` — the three templates, item shapes, what prints
- `examples/` — real items lifted from the reports already in this repo
