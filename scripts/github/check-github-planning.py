from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LABELS_FILE = ROOT / ".github" / "labels.yml"
ISSUES_DIR = ROOT / ".github" / "issues"

HEX_RE = re.compile(r"^[0-9a-fA-F]{6}$")
ISSUE_ID_RE = re.compile(r"WP-E\d{2}-\d{3}")


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def parse_labels() -> list[dict[str, str]]:
    if not LABELS_FILE.is_file():
        fail(".github/labels.yml is missing")

    labels: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in LABELS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if not line.strip() or line.lstrip().startswith("#"):
            continue

        stripped = line.strip()

        if stripped.startswith("- name:"):
            if current is not None:
                labels.append(current)
            current = {"name": stripped.split(":", 1)[1].strip().strip('"').strip("'")}
            continue

        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip().strip('"').strip("'")

    if current is not None:
        labels.append(current)

    return labels


def validate_labels() -> set[str]:
    labels = parse_labels()

    if not labels:
        fail(".github/labels.yml does not contain any labels")

    seen: set[str] = set()

    for label in labels:
        name = label.get("name", "").strip()
        color = label.get("color", "").strip()
        description = label.get("description", "").strip()

        if not name:
            fail("label entry is missing name")

        if name in seen:
            fail(f"duplicate label name: {name}")

        seen.add(name)

        if not color:
            fail(f"label {name!r} is missing color")

        if not HEX_RE.match(color):
            fail(f"label {name!r} color must be a 6-character hex value, got {color!r}")

        if not description:
            fail(f"label {name!r} is missing description")

    print(f"validated {len(labels)} labels")
    return seen


def parse_issue_metadata(path: Path) -> tuple[str, list[str], str]:
    text = path.read_text(encoding="utf-8")

    if not text.strip():
        fail(f"{path.relative_to(ROOT)} is empty")

    title = ""
    labels: list[str] = []

    lines = text.splitlines()

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
            if not stripped:
                continue

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

    if not ISSUE_ID_RE.search(path.name) and not ISSUE_ID_RE.search(title):
        fail(f"{path.relative_to(ROOT)} does not include a WP-E##-### work packet id")

    return title, labels, body


def validate_issues(known_labels: set[str]) -> None:
    if not ISSUES_DIR.is_dir():
        fail(".github/issues directory is missing")

    issue_files = sorted(ISSUES_DIR.glob("*.md"))

    if not issue_files:
        fail(".github/issues does not contain any markdown issue files")

    seen_titles: set[str] = set()

    for path in issue_files:
        title, labels, _body = parse_issue_metadata(path)

        if title in seen_titles:
            fail(f"duplicate issue title: {title}")

        seen_titles.add(title)

        unknown_labels = [label for label in labels if label not in known_labels]
        if unknown_labels:
            fail(
                f"{path.relative_to(ROOT)} references labels not present in .github/labels.yml: "
                + ", ".join(unknown_labels)
            )

    print(f"validated {len(issue_files)} issue files")


def main() -> None:
    known_labels = validate_labels()
    validate_issues(known_labels)
    print("GitHub planning files are valid")


if __name__ == "__main__":
    main()
