from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ISSUES_DIR = ROOT / ".github" / "issues"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def parse_issue(path: Path) -> tuple[str, list[str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = ""
    labels: list[str] = []

    if lines and lines[0].strip() == "---":
        end = None
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                end = index
                break

        if end is None:
            fail(f"{path.relative_to(ROOT)} has opening frontmatter but no closing frontmatter")

        frontmatter = lines[1:end]
        body = "\n".join(lines[end + 1 :]).strip()
        active_key = ""

        for line in frontmatter:
            stripped = line.strip()

            if stripped.startswith("title:"):
                title = stripped.split(":", 1)[1].strip().strip('"').strip("'")
                active_key = "title"
                continue

            if stripped.startswith("labels:"):
                active_key = "labels"
                inline_value = stripped.split(":", 1)[1].strip()
                if inline_value.startswith("[") and inline_value.endswith("]"):
                    labels.extend(
                        item.strip().strip('"').strip("'")
                        for item in inline_value[1:-1].split(",")
                        if item.strip()
                    )
                continue

            if active_key == "labels" and stripped.startswith("- "):
                labels.append(stripped[2:].strip().strip('"').strip("'"))

    else:
        body = text.strip()
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                title = stripped[2:].strip()
                break

    if not title:
        for line in lines:
            stripped = line.strip()
            if stripped:
                title = stripped.removeprefix("#").strip()
                break

    if not title:
        fail(f"{path.relative_to(ROOT)} does not have a title")

    if not body:
        fail(f"{path.relative_to(ROOT)} does not have a body")

    if not labels:
        labels = ["type: work-packet", "status: ready"]

    return title, labels, body


def gh_json(command: list[str]) -> object:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    if not completed.stdout.strip():
        return None
    return json.loads(completed.stdout)


def issue_exists(title: str) -> bool:
    query = f'{title} in:title repo:@owner/@repo'
    data = gh_json(
        [
            "gh",
            "issue",
            "list",
            "--state",
            "all",
            "--search",
            query,
            "--json",
            "title,number,state",
            "--limit",
            "100",
        ]
    )

    if not isinstance(data, list):
        return False

    return any(item.get("title") == title for item in data if isinstance(item, dict))


def create_issue(title: str, labels: list[str], body: str, dry_run: bool) -> None:
    command = [
        "gh",
        "issue",
        "create",
        "--title",
        title,
        "--body",
        body,
    ]

    for label in labels:
        command.extend(["--label", label])

    if dry_run:
        print("[dry-run] " + " ".join(command[:5]) + " ...")
        print(f"          labels: {', '.join(labels)}")
        return

    print(f"creating issue: {title}")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create GitHub issues from .github/issues/*.md")
    parser.add_argument("--dry-run", action="store_true", help="Print intended actions without creating issues")
    args = parser.parse_args()

    if shutil.which("gh") is None and not args.dry_run:
        fail("GitHub CLI `gh` is not installed or is not on PATH")

    subprocess.run(["python3", "scripts/github/check-github-planning.py"], cwd=ROOT, check=True)

    issue_files = sorted(ISSUES_DIR.glob("*.md"))
    created = 0
    skipped = 0

    for path in issue_files:
        title, labels, body = parse_issue(path)

        if args.dry_run:
            create_issue(title, labels, body, dry_run=True)
            continue

        if issue_exists(title):
            print(f"skipping existing issue: {title}")
            skipped += 1
            continue

        create_issue(title, labels, body, dry_run=False)
        created += 1

    if args.dry_run:
        print(f"dry-run complete for {len(issue_files)} issue files")
    else:
        print(f"created {created} issues; skipped {skipped} existing issues")


if __name__ == "__main__":
    main()
