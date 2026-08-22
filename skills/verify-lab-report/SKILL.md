---
name: verify-lab-report
description: Verify a generated lab report against its source question paper or assignment. Use when checking whether a lab report, practical report, case study, or generated HTML/PDF/DOCX/PPTX/XLSX covers every required question, sub-question, output, screenshot, diagram, table, student detail, and formatting instruction.
---

# Verify lab report

Use a **ledger-first** audit. The question paper defines the requirements. The generated report is only evidence against those requirements.

## 1. Pair the source and report

Identify which artifact is the source question, assignment, lab sheet, or manual and which artifact or bundle is the generated report. Pair by course, lab number, title, and question numbering rather than filename alone.

If several generated files make one submission, such as a report plus index page, treat them as one bundle.

## 2. Build the requirement ledger first

Read the source completely **before inspecting the report**. Read every page, slide, sheet, table, note, image, diagram, caption, and instruction block that can affect the submission.

Create an internal ledger with one row for each atomic requirement:

- source location and original question number
- scope: whole report, one lab, one question, or one sub-question
- requirement
- required evidence type, such as prose, code, SQL, command, output, screenshot, diagram, transition table, citation, cover page, index, page number, or formatting
- whether the requirement must repeat for every applicable answer

Split compound instructions into separate rows. A question that asks for a transition diagram, transition table, and C/C++ program produces three requirements. A global rule such as "print Lab No., Name and Roll No./Section after every output" produces one rule whose scope is every applicable program.

Treat parenthetical text and examples as requirements when they constrain the answer. Distinguish real tasks from headings or grouping labels so a numbered heading is not automatically counted as an unanswered question.

The ledger is complete only when:

1. every source question and sub-question is accounted for,
2. every global instruction has a scope,
3. every required evidence type is explicit, and
4. the question count and numbering reconcile with the source.

Do not weaken or invent requirements after seeing what the report contains. If later inspection reveals a genuine extraction mistake, correct the ledger and state the correction.

## 3. Inspect the generated report

Read [references/inspection.md](references/inspection.md) for format-specific inspection rules.

For each ledger row, find concrete evidence in the report and record its location. Use these statuses:

- `PRESENT`: the required item is actually there and matches the requested evidence type.
- `PARTIAL`: something related is present, but part of the requirement is missing or the evidence type is weaker than requested.
- `MISSING`: no matching evidence exists.
- `UNVERIFIABLE`: the artifact or available tools cannot establish whether the requirement is satisfied.

Question text by itself is not an answer. A heading named "Diagram" with no diagram is not a diagram. A styled terminal pane is output text, not automatically a captured screenshot. A placeholder field for student details is not proof that the submitted copy contains those details.

When a requirement must repeat, check every applicable item. One correct footer, screenshot, citation, or output does not satisfy a rule that applies to all questions.

## 4. Check coverage and consistency

After mapping every ledger row, reconcile the report as a whole:

- all questions and sub-questions are present in the correct numbering or are unambiguously mapped
- required sections appear in the requested order
- diagrams, tables, screenshots, code, SQL, commands, and outputs are attached to the correct question
- student-specific requirements are not hard-coded to the wrong student
- cover page, index or contents page, references, lists, captions, page numbering, and other report-wide requirements are present when requested
- formatting requirements are checked only when the artifact can be inspected at the relevant visual or document-structure level
- no placeholder, empty panel, collapsed generator shell, or control page is mistaken for final report content

Flag obvious contradictions separately, such as an answer for the wrong algorithm, SQL against the wrong table, an output that contradicts the shown code, or a report claiming to cover labs that are absent. Do not turn a coverage check into a full technical re-derivation unless the user asks for correctness verification or correctness is necessary to decide whether a stated requirement was met.

If execution is required to establish compliance, use the available compiler, interpreter, database, or project verification script. State plainly when execution could not be performed.

## 5. Give the verdict

Return a short compliance result first:

- `PASS`: every mandatory ledger row is `PRESENT` and no unresolved `UNVERIFIABLE` row can change the result.
- `NEEDS FIXES`: one or more rows are `PARTIAL` or `MISSING`.
- `CANNOT VERIFY`: the source or report cannot be inspected well enough to judge the mandatory requirements.

Then give counts such as `42 present, 3 partial, 1 missing` and list the missing or partial items first. For each issue, name the source requirement, its source location or question number, and what the report has or lacks.

If everything passes, say how many atomic requirements were checked. Keep the response concise unless the user asks for the full ledger.

## Hard rules

1. Source first, report second.
2. Verify atomic requirements, not topic similarity.
3. Preserve the source's scope and numbering.
4. Require the evidence type the source actually asks for.
5. Never infer a pass from filenames, titles, table of contents entries, or generator controls.
6. Never claim visual, layout, screenshot, or execution compliance without inspecting evidence that can prove it.
