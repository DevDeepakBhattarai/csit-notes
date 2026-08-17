# Authoring rules

## 1. Literalism

The question is the specification. The whole specification. Answer it and stop.

This is a lab report, submitted once, marked against the question paper. There is
no user, no maintainer, no next release. Judgement calls that would be good
engineering instincts elsewhere are, here, just noise that costs paper and time —
and a query the grader did not ask for reads as a mistake, not as care.

**The rule:** if a clause is not in the question, it does not go in the answer.

Real example from this repo — every SELECT came back with an `ORDER BY` nobody
asked for, and all of them had to be stripped out again:

```sql
-- Question: "Project CategoryName from categories."
SELECT CategoryName FROM categories ORDER BY CategoryID;   -- wrong: invented a clause
SELECT CategoryName FROM categories;                       -- right
```

The same trap in other shapes:

| Temptation | Verdict |
|---|---|
| `ORDER BY` / `LIMIT` / `DISTINCT` not in the question | Leave it out |
| Renaming columns with `AS` when the question did not name them | Leave it out (an alias the question *does* name, like `SupplierCount`, stays) |
| Input validation, retry loops, menus | Leave it out |
| `free()`, error branches, defensive `NULL` checks in a 30-line demo | Leave it out |
| Handling an edge case the question never mentions | Leave it out |
| Extra columns "for context" in a SELECT | Leave it out — project exactly what was asked |
| Answering a question that was not asked because it seems related | Leave it out |

Where the question genuinely is ambiguous, pick the simplest reading, implement
it, and move on. Do not implement both readings.

## 2. Theory

**2–3 sentences.** What the technique is, plus the one property that matters for
this question. No history, no comparison tables, no advantages/disadvantages
lists.

> First Come First Served scheduling executes processes in the order in which
> they arrive in the ready queue. It is simple and non-preemptive, but short jobs
> may wait behind long jobs.

That is a complete, sufficient theory section.

## 3. Algorithm

**3–6 steps, one line each.** Imperative. It mirrors the code; it is not
pseudocode for a different program.

> 1. Sort the processes according to arrival time.
> 2. If the CPU is idle, move time to the next arriving process.
> 3. Run the selected process until its burst time completes.
> 4. Calculate completion, turnaround, waiting time, and the averages.

Skip the algorithm section entirely for questions that have no algorithm
(a single SQL statement, "display your name in Prolog").

## 4. Code

- Shortest correct program that answers the question. Usually 20–50 lines.
- **Hard-code the sample data** unless the question says the program reads input.
  A fixed dataset makes the output reproducible and the report consistent.
- Standard headers only. No helper libraries, no custom allocators, no macros.
- Comments: none, or one line where the logic is genuinely non-obvious. The
  theory and algorithm sections already explain it.
- Keep lines under ~80 characters — code is printed at 10pt on A4.
- Reuse one dataset across a lab so the outputs form a coherent story
  (e.g. the same four processes across FCFS, SJF, SRTF, Round Robin).
- If the question needs stdin, put the input in the item's `stdin` field so the
  verifier feeds the same bytes.

### The footer printf

Most papers here demand it — check the instructions block. OS wants
`Lab No. / Name / Roll No./Section`; AI wants name, roll, lab number; TOC wants
name and roll. Append it as the **last thing before `return 0;`**, using the
tokens so the browser can substitute the real values:

```c
    printf("\nLab No.: 1(a)\n");
    printf("Name: {NAME}\n");
    printf("Roll No./Section: {ROLL}/{SECTION}\n");

    return 0;
}
```

The same tokens must appear in the item's `output`, in the same place, so the
printed terminal matches the printed source.

## 5. SQL

- One statement per question unless the question asks for several.
- Answer with the plainest form that satisfies the question. No CTEs, no window
  functions, no aliases the question did not introduce.
- `SELECT all from X` means `SELECT * FROM x` — do not enumerate columns.
- DML questions (`INSERT` / `UPDATE` / `DELETE`) produce no rows, so add a
  `verify` SELECT that shows the effect. That is evidence, not decoration — it is
  the only thing that can be printed for those questions.
- When a question destroys rows another question needs, that is fine: every item
  is verified against a **fresh** database (see `scripts/verify_sql.py`).
- Keep the setup script in one place and pass it with `--setup`.

## 6. Output

The `output` field is a transcript of a real run. It is the part the grader
actually looks at.

- Get it from the compiler: `verify_c.py --write` runs the program and pastes
  the real stdout back into the item.
- Get it from the database: `verify_sql.py` stores the real `columns` / `rows`.
- Tokens (`{NAME}`, `{ROLL}`) stay as tokens in the stored output — the page
  substitutes them live.
- Never invent numbers. A hand-computed average that disagrees with the code is
  the one error a grader always catches.
- If you truly cannot run it, say so in your final message and mark the report
  as unverified. Do not describe it as tested.

## 7. Student-specific values

| Paper phrasing | Token | Notes |
|---|---|---|
| "print your name / roll / section in the output" | `{NAME}` `{ROLL}` `{SECTION}` | In both `code` and `output` |
| "file path must contain your name" | — | The terminal title bar is built from the name input |
| "starts with the first letter of your name" | `{{FIRST_LETTER}}` | SQL only; add a `dynamic` entry so the rows re-filter |
| "database `<your-name>dbms1`" | `{{NAME_SLUG}}dbms1` | Lowercase, alphanumeric only |
| "of your choice" | — | Choose once, keep it stable across related questions |
| "draw the graph in the report" | `diagram` | Mermaid; `printable.html` renders it |

A hard-coded "Deepak" anywhere in the data is a bug — it breaks the moment the
file is shared or the name box is edited.

## 8. Pace

Do the whole paper in one pass: extract → write every item → verify all →
render → check pages. Do not stop after three questions to ask whether the style
is right. The variant question in Step 0 is the only interruption.
