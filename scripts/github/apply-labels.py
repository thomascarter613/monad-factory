from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LABELS_FILE = ROOT / ".github" / "labels.yml"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def parse_labels() -> list[dict[str, str]]:
    labels: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in LABELS_FILE.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()

        if not stripped or stripped.startswith("#"):
            continue

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


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    if not LABELS_FILE.is_file():
        fail(".github/labels.yml is missing")

    if shutil.which("gh") is None:
        fail("GitHub CLI `gh` is not installed or is not on PATH")

    subprocess.run(["python3", "scripts/github/check-github-planning.py"], cwd=ROOT, check=True)

    labels = parse_labels()

    for label in labels:
        name = label["name"]
        color = label["color"].lstrip("#")
        description = label["description"]

        run(
            [
                "gh",
                "label",
                "create",
                name,
                "--color",
                color,
                "--description",
                description,
                "--force",
            ]
        )

    print(f"applied {len(labels)} labels")


if __name__ == "__main__":
    main()
