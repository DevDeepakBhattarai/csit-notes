# Examples

The JSON files here are **real items lifted verbatim** from the reports already
submitted from this repo. Use them as the shape and the standard: match this
length of theory, this length of algorithm, this size of program.

| File | Taken from | Shows |
|---|---|---|
| `os-item.json` | `4th Sem/OS/OS_Lab_Report_Generator.html` | The plain printable item: short theory, 4-step algorithm, ~35-line C program, footer printf with `{NAME}`/`{ROLL}`/`{SECTION}`, output matching it exactly |
| `ai-item.json` | `4th Sem/AI/AI_Lab_Report_Generator.html` | Same, plus a Mermaid `diagram` (the graph the question demanded be drawn), and a Prolog item where the question is prose |
| `toc-item.json` | `4th Sem/Theory of Computation/Theory of Computation Lab Report.html` | A file-handling program and a DFA program; theory as a single string, algorithm as short imperative steps |
| `dbms-item.json` | `4th Sem/DBMS/DBMS_Lab_Report_Part2_Verification.json` | Verified SQL items: real `columns`/`rows` straight from MariaDB, a `{{FIRST_LETTER}}` question with `dynamic`, an UPDATE with a `verify` SELECT, and a CREATE VIEW |

## The full reports they came from

Open these when you need to see a whole finished submission rather than one item:

- `4th Sem/OS/OS_Lab_Report_Generator.html` — fully printable, 25 items, 56 A4 pages
- `4th Sem/AI/AI_Lab_Report_Generator.html` — fully printable with diagrams, 22 items
- `4th Sem/Theory of Computation/Theory of Computation Lab Report.html` — fully printable, 19 items
- `4th Sem/Theory of Computation/Theory of Computation Lab Report-Writing.html` — same 19 items, output-only variant
- `4th Sem/DBMS/DBMS_Lab_Report.html` — Labs 1–2, questions + XAMPP output tabs
- `4th Sem/DBMS/DBMS_Lab_Report_Part2_Printable.html` — Labs 4–6, 116 verified SQL items, write-space + result pane
- `4th Sem/DBMS/build_part2_report.py` — the script that executed all 116 queries against MariaDB and generated that report

And the question papers they were built from, for the input side:

- `4th Sem/OS/Lab Works1.pdf` — instructions block demanding the footer printf and a name in the file path
- `4th Sem/AI/LABASSIGNMENT-1.pdf` — family-tree image on pages 1–2 that the text dump loses
- `4th Sem/DBMS/DBMS Lab 1.pptx` — `<your-name>dbms1` naming
- `4th Sem/DBMS/LAB_part2.pdf` — Group A / Group B split, "first letter of your name" questions
- `4th Sem/Computer Network/CN Lab list.pdf` — Packet Tracer labs, screenshot-driven
