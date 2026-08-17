"""Run every SQL answer against a real MySQL/MariaDB and store the real result.

    python verify_sql.py <report.html|items.json> --setup setup.sql [--letter D] [--json out.json]

Each item gets a FRESH database seeded from --setup, so a DELETE in question 12
cannot corrupt the result of question 13. For each item it runs:

    setup.sql  ->  item["pre"] (optional)  ->  item["sql"]  ->  item["verify"] (optional)

and writes `columns`, `rows`, `affected` back into the item. `{{FIRST_LETTER}}`
is replaced with --letter (the first letter of the student's name).

Needs XAMPP (or any MySQL) running:  pip install pymysql
Exit code is non-zero if any statement raised.
"""
from __future__ import annotations

import argparse
import datetime as dt
import decimal
import json
import re
import sys
from pathlib import Path

try:
    import pymysql
except ImportError:
    sys.exit("pip install pymysql")

DATA_RE = re.compile(
    r'(<script type="application/json" id="report-data">\s*)(.*?)(\s*</script>)',
    re.DOTALL,
)


def split_sql(sql: str) -> list[str]:
    """Split on ';' while respecting single-quoted strings."""
    statements, current = [], []
    in_single = escaped = False
    for char in sql:
        if char == "\\" and not escaped:
            escaped = True
            current.append(char)
            continue
        if char == "'" and not escaped:
            in_single = not in_single
        if char == ";" and not in_single:
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
        else:
            current.append(char)
        escaped = False
    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements


def normalize(value):
    if isinstance(value, decimal.Decimal):
        return format(value, "f")
    if isinstance(value, (dt.date, dt.datetime, dt.time)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def execute(cursor, sql: str, letter: str) -> tuple[list[str], list[list], int]:
    columns: list[str] = []
    rows: list[list] = []
    affected = 0
    for statement in split_sql(sql):
        cursor.execute(statement.replace("{{FIRST_LETTER}}", letter))
        if cursor.description:                       # last SELECT wins - that is what phpMyAdmin shows
            columns = [c[0] for c in cursor.description]
            rows = [[normalize(v) for v in row] for row in cursor.fetchall()]
        elif cursor.rowcount > 0:
            affected += cursor.rowcount
    return columns, rows, affected


def load(path: Path) -> tuple[list[dict], str | None]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text), None
    match = DATA_RE.search(text)
    if not match:
        sys.exit(f'No <script type="application/json" id="report-data"> block in {path}')
    return json.loads(match.group(2)), text


def save(path: Path, items: list[dict], original: str | None) -> None:
    body = json.dumps(items, ensure_ascii=False, indent=2)
    if original is None:
        path.write_text(body + "\n", encoding="utf-8")
    else:
        path.write_text(DATA_RE.sub(lambda m: m.group(1) + body + m.group(3), original, count=1), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("report")
    parser.add_argument("--setup", required=True, help="schema + sample data SQL run before every item")
    parser.add_argument("--letter", default="D", help="first letter of the student's name")
    parser.add_argument("--json", help="also write a standalone verification record here")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--user", default="root")
    parser.add_argument("--password", default="")
    parser.add_argument("--db", default="lab_verify_scratch")
    args = parser.parse_args()

    path = Path(args.report).resolve()
    items, original = load(path)
    setup_sql = Path(args.setup).resolve().read_text(encoding="utf-8")

    connection = pymysql.connect(host=args.host, user=args.user, password=args.password,
                                 charset="utf8mb4", autocommit=True)
    record, failures = [], 0
    try:
        with connection.cursor() as cursor:
            for index, item in enumerate(items, 1):
                ident = item.get("id", item.get("no", index))
                cursor.execute(f"DROP DATABASE IF EXISTS `{args.db}`")
                cursor.execute(f"CREATE DATABASE `{args.db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                cursor.execute(f"USE `{args.db}`")
                try:
                    execute(cursor, setup_sql, args.letter)
                    if item.get("pre"):
                        execute(cursor, item["pre"], args.letter)
                    columns, rows, affected = execute(cursor, item["sql"], args.letter)
                    if item.get("verify"):
                        v_cols, v_rows, v_affected = execute(cursor, item["verify"], args.letter)
                        columns, rows = v_cols, v_rows
                        affected += v_affected
                except Exception as error:               # noqa: BLE001 - the message is the whole point
                    failures += 1
                    print(f"[{index:03d}] FAIL {ident}: {error}")
                    continue

                item["columns"], item["rows"], item["affected"] = columns, rows, affected
                record.append({"id": ident, "question": item.get("question"), "sql": item.get("sql"),
                               "verify": item.get("verify"), "columns": columns, "rows": rows, "affected": affected})
                print(f"[{index:03d}/{len(items)}] PASS {ident} - {len(rows)} row(s)")
    finally:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"DROP DATABASE IF EXISTS `{args.db}`")
        finally:
            connection.close()

    save(path, items, original)
    print(f"\nupdated {path.name}")
    if args.json:
        Path(args.json).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote {args.json}")
    print(f"{len(items)} items, {failures} failure(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
