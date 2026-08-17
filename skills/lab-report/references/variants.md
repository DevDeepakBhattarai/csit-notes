# The three templates

Copy the template to the subject folder, replace `{{SUBJECT}}` / `{{FOLDER}}`,
and rewrite the `report-data` JSON block. Nothing else in the file needs to
change — pagination, the index page, the terminal chrome and the print CSS are
already correct and proven on real submissions.

`{{FOLDER}}` is the lowercase subject slug used in the fake path
(`C:\deepak_bhattarai\os\lab_1a_fcfs.exe`): `os`, `ai`, `toc`, `dbms`, `cn`.

---

## A. `printable.html` — everything is printed

Their AI, OS and TOC (printable) reports. Prints: index page, then per question
the question, optional diagram, theory, algorithm, full source code, and the
terminal output.

```json
{
  "no": "1(a)",
  "title": "FCFS CPU Scheduling Algorithm",
  "question": "WAP to simulate FCFS CPU Scheduling Algorithm.",
  "theory": ["2-3 sentences."],
  "algorithm": ["Step.", "Step.", "Step."],
  "diagram": { "title": "Graph used for BFS", "code": "flowchart LR\n  A((A)) --> B((B))", "size": "short" },
  "filename": "lab_1a_fcfs.c",
  "code": "#include <stdio.h>\n...{NAME}...",
  "output": "FCFS Gantt Chart\n...{NAME}..."
}
```

- `no` and `title` build the index table; `question` is the printed heading.
- `theory`, `algorithm`, `diagram` are all optional — omit the key entirely.
- `diagram.size`: `short` (43mm), default (57mm), `tall` (89mm). Mermaid loads
  from a CDN; offline it degrades to the diagram source in a `<pre>`.
- Code is paginated **one line per block**, so a 200-line program flows across
  pages instead of overflowing.
- `report-meta` at the top of the file sets `subject`, `folder`, index column
  headings, the date cell, and `showPageFooter` (a Name/Roll line at the bottom
  of every page — the AI report uses it, OS does not).

Check it with `scripts/check_pages.py`; `OVERFLOW` must be `none`.

## B. `output-only.html` — code copied by hand, outputs printed

Their TOC "Writing" report. Two screen tabs:

- **Theory + Code** — expandable cards with a Copy button. Never printed; this is
  the thing the student reads while writing the answer out on paper.
- **Output** — the terminals. The green button measures every terminal, packs
  them biggest-first into two columns on A4, and prints just those pages.

Same item shape as A (`theory`, `algorithm`, `code`, `output`, `filename`), so
data is portable between the two templates — if the user changes their mind
about the variant, you move the JSON block across and change nothing else.

`check_pages.py` does not apply here (pages are built at print time). Sanity-check
by opening the Output tab and confirming every program has a terminal.

## C. `sql-output.html` — SQL written by hand, results printed

Their DBMS Part 2 report. Each question becomes a **pair**: blank writing space
sized to the length of the query, then the phpMyAdmin result pane underneath.
The student writes the SQL in the gap; the printed pane is the evidence it ran.

```json
{
  "id": "4A-08", "lab": 4,
  "title": "Customer City by Name Initial",
  "question": "SELECT all from customers who are from a city whose name starts with the first letter of your name.",
  "sql": "SELECT * FROM customers WHERE City LIKE '{{FIRST_LETTER}}%';",
  "verify": null,
  "columns": ["CustomerID", "CustomerName", "City", "Country"],
  "rows": [[1, "Alfreds Futterkiste", "Berlin", "Germany"]],
  "affected": 0,
  "dynamic": "customer_city_initial"
}
```

- `columns` / `rows` / `affected` come from `scripts/verify_sql.py`. Do not type
  them by hand.
- `verify`: the follow-up SELECT for INSERT/UPDATE/DELETE questions. It is shown
  under the answer as `-- Verification query` and its result is what the pane
  displays.
- `lab` groups the questions; a new `lab` value starts a new page.
- Tokens: `{{FIRST_LETTER}}`, `{{NAME_SLUG}}`, `{{NAME}}`.
- `dynamic` names an entry in the `DYNAMIC` map at the top of the script, which
  re-filters the printed rows when the name box changes. Add one only for
  questions whose *result* depends on the name — copy the shape already in the
  file:

```js
"customer_city_initial": {
  columns: ["CustomerID","CustomerName","City","Country"],
  rows: [[1,"Alfreds Futterkiste","Berlin","Germany"]],
  match: (row, letter) => String(row[2]).toUpperCase().startsWith(letter)
}
```

- The **Writing space** dropdown (Tight / Normal / Roomy) rescales every gap;
  use it to land on a page count the user is happy with. The existing DBMS report
  shipped two builds for exactly this reason.

---

## Printing

A4, margins **None**, background graphics **ON**. All three templates set
`@page { size: A4; margin: 0 }` and draw their own 2px page border, so the
browser must not add its own margins.
