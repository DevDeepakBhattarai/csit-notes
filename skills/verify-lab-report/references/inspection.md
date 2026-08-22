# Artifact inspection rules

Use the artifact's real structure, not only a text dump, when the requirement depends on visuals, layout, formulas, embedded media, or generated content.

## PDF

Extract text from every page. Also inspect pages visually when the source or report depends on screenshots, diagrams, tables, captions, page order, page numbers, fonts, margins, spacing, or other layout.

If the PDF is scanned or text extraction is incomplete, inspect the page images instead of treating missing extracted text as missing content.

## HTML

A generator shell is not the report. Inspect the rendered report content or the data that deterministically produces it.

For JavaScript-driven files, inspect embedded JSON, arrays, templates, and generated sections. Render the page when visual or print behavior matters. Check print CSS when the source specifies A4, margins, page breaks, one-sided printing, headers, footers, or similar requirements.

Do not count buttons, input labels, tab names, counters, or an empty report container as report evidence.

## DOCX

Inspect paragraphs, tables, headers, footers, section settings, page numbering, images, captions, and styles when relevant. Text extraction alone cannot prove screenshot, page-layout, margin, font, or pagination requirements.

## PPTX

Inspect every slide and all text boxes, tables, diagrams, images, and notes that form part of the assignment or report. Preserve slide-level question numbering when building the requirement ledger.

## XLSX or other spreadsheet

Inspect every relevant worksheet, including formulas, displayed values, tables, charts, images, and print settings when the assignment requires them. Do not treat a formula as verified merely because a displayed value exists if the formula itself is the requested work.

## Images and scans

Inspect the image directly. Pay attention to handwritten annotations, family trees, automata, network topologies, screenshots, and labels that text extraction may miss.

## Mixed bundles

A submission may spread requirements across several files, such as a main report, an index page, a separate output sheet, and a setup script. Verify the bundle as a whole only when those files are clearly intended to be submitted together. Record which file satisfies each requirement.

## Evidence strength

Match evidence to the source wording:

- "output" can be satisfied by readable output evidence.
- "screenshot of output" requires an image or captured-screen artifact, not merely typed output text.
- "draw" or "design" requires the requested visual representation when the question asks for one.
- "show all steps" requires the actual sequence of steps, not only a final result.
- "complete code" requires the complete program, not a fragment or pseudocode.
- "cite in IEEE style" requires in-text citation markers plus a corresponding IEEE-style reference list.
- a formatting rule requires inspection of the final printable or document layout when possible.

When the available artifact cannot prove the required evidence type, use `UNVERIFIABLE` or `PARTIAL` instead of guessing.
