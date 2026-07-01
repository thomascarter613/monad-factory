from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Finding:
    level: str
    message: str


class Doctor:
    def __init__(self, *, ci: bool, strict: bool) -> None:
        self.ci = ci
        self.strict = strict
        self.findings: list[Finding] = []

    def ok(self, message: str) -> None:
        self.findings.append(Finding("OK", message))

    def warn(self, message: str) -> None:
        self.findings.append(Finding("WARN", message))

    def fail(self, message: str) -> None:
        self.findings.append(Finding("FAIL", message))

    def command_exists(self, command: str) -> bool:
        return shutil.which(command) is not None

    def run_text(self, command: list[str]) -> tuple[int, str, str]:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return completed.returncode, completed.stdout.strip(), completed.stderr.strip()

    def check_required_files(self) -> None:
        required_files = [
            "README.md",
            "AGENTS.md",
            "CODEOWNERS",
            "LICENSE",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "workspace.toml",
            "mise.toml",
            "package.json",
            "bun.lock",
            "tsconfig.base.json",
            "biome.json",
            "lefthook.yml",
            ".moon/workspace.yml",
            ".moon/toolchains.yml",
            "moon.yml",
            ".github/labels.yml",
            ".github/workflows/ci.yml",
            "docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
            "docs/adr/00-index.md",
            ".monad/config.toml",
            ".monad/memory/MEMORY.md",
            "scripts/check-foundation.sh",
            "scripts/check-root-toolchain.sh",
            "scripts/check-ci.sh",
            "scripts/github/check-github-planning.py",
                "Cargo.toml",
                "Cargo.lock",
                "rust-toolchain.toml",
                "rustfmt.toml",
                ".cargo/config.toml",
                "scripts/check-rust-workspace.sh",
        ]

        missing = [path for path in required_files if not (ROOT / path).is_file()]

        if missing:
            self.fail("missing required files: " + ", ".join(missing))
        else:
            self.ok(f"required file set present ({len(required_files)} files)")

    def check_required_directories(self) -> None:
        required_directories = [
            "apps",
            "crates",
            "docs",
            "infra",
            "packages",
            "plugins",
            "policies",
            "services",
            "templates",
            ".github",
            ".moon",
            ".monad",
        ]

        missing = [path for path in required_directories if not (ROOT / path).is_dir()]

        if missing:
            self.fail("missing required directories: " + ", ".join(missing))
        else:
            self.ok(f"required directory set present ({len(required_directories)} directories)")

    def check_package_json(self) -> None:
        path = ROOT / "package.json"

        try:
            package = json.loads(path.read_text(encoding="utf-8"))
        except Exception as error:
            self.fail(f"package.json is not valid JSON: {error}")
            return

        expected_scripts = [
            "check",
            "check:ci",
            "check:foundation",
            "check:github-planning",
            "check:toolchain",
            "ci:local",
            "doctor",
            "doctor:ci",
            "doctor:strict",
            "format:check",
            "format:write",
            "github:issues",
            "github:issues:dry-run",
            "github:labels",
            "hooks:install",
            "lint",
            "moon:check",
            "moon:version",
            "typecheck",
        ]

        scripts = package.get("scripts", {})
        missing_scripts = [script for script in expected_scripts if script not in scripts]

        if missing_scripts:
            self.fail("package.json missing scripts: " + ", ".join(missing_scripts))
        else:
            self.ok(f"package.json scripts present ({len(expected_scripts)} scripts)")

        expected_dev_dependencies = [
            "@biomejs/biome",
            "@moonrepo/cli",
            "lefthook",
            "typescript",
        ]

        dev_dependencies = package.get("devDependencies", {})
        missing_dependencies = [
            dependency
            for dependency in expected_dev_dependencies
            if dependency not in dev_dependencies
        ]

        if missing_dependencies:
            self.fail(
                "package.json missing devDependencies: " + ", ".join(missing_dependencies)
            )
        else:
            self.ok(
                f"package.json devDependencies present ({len(expected_dev_dependencies)} dependencies)"
            )

    def check_git(self) -> None:
        if not self.command_exists("git"):
            self.fail("git is not installed or not on PATH")
            return

        code, stdout, stderr = self.run_text(["git", "rev-parse", "--show-toplevel"])
        if code != 0:
            self.fail(f"not inside a git repository: {stderr or stdout}")
            return

        repo_root = Path(stdout).resolve()
        if repo_root != ROOT.resolve():
            self.fail(f"doctor expected repo root {ROOT}, but git root is {repo_root}")
        else:
            self.ok("running from monad-factory repository root")

        code, stdout, stderr = self.run_text(["git", "remote", "get-url", "origin"])
        if code != 0:
            self.warn("git remote origin is not configured")
        elif "monad-factory" not in stdout:
            self.warn(f"git remote origin does not appear to be monad-factory: {stdout}")
        else:
            self.ok(f"git remote origin configured: {stdout}")

        if not self.ci:
            code, stdout, stderr = self.run_text(["git", "status", "--short"])
            if code != 0:
                self.warn(f"could not inspect git status: {stderr or stdout}")
            elif stdout:
                self.warn("working tree has uncommitted changes")
            else:
                self.ok("working tree is clean")

    def check_runtime_commands(self) -> None:
        commands = {
            "bun": ["bun", "--version"],
            "node": ["node", "--version"],
            "python3": ["python3", "--version"],
                "cargo": ["cargo", "--version"],
                "rustc": ["rustc", "--version"],
        }

        for name, command in commands.items():
            if not self.command_exists(name):
                self.fail(f"{name} is not installed or not on PATH")
                continue

            code, stdout, stderr = self.run_text(command)
            if code != 0:
                self.fail(f"{name} exists but version command failed: {stderr or stdout}")
            else:
                self.ok(f"{name} available: {stdout or stderr}")

        optional_commands = {
            "gh": ["gh", "--version"],
            "mise": ["mise", "--version"],
        }

        for name, command in optional_commands.items():
            if not self.command_exists(name):
                self.warn(f"{name} is not installed or not on PATH")
                continue

            code, stdout, stderr = self.run_text(command)
            if code != 0:
                self.warn(f"{name} exists but version command failed: {stderr or stdout}")
            else:
                first_line = (stdout or stderr).splitlines()[0]
                self.ok(f"{name} available: {first_line}")

    def check_node_modules_tools(self) -> None:
        tool_paths = {
            "biome": ROOT / "node_modules" / ".bin" / "biome",
            "moon": ROOT / "node_modules" / ".bin" / "moon",
            "lefthook": ROOT / "node_modules" / ".bin" / "lefthook",
            "tsc": ROOT / "node_modules" / ".bin" / "tsc",
        }

        missing = [name for name, path in tool_paths.items() if not path.exists()]

        if missing:
            self.warn(
                "node_modules tools missing; run `bun install`: " + ", ".join(missing)
            )
        else:
            self.ok("node_modules tool binaries present: biome, moon, lefthook, tsc")

    def check_github_cli_auth(self) -> None:
        if self.ci:
            self.ok("skipping GitHub CLI auth check in CI mode")
            return

        if not self.command_exists("gh"):
            self.warn("GitHub CLI `gh` is not installed; label/issue automation cannot run")
            return

        code, stdout, stderr = self.run_text(["gh", "auth", "status"])
        if code != 0:
            self.warn("GitHub CLI is installed but not authenticated")
        else:
            self.ok("GitHub CLI authentication is available")

    def check_subcommands(self) -> None:
        checks = [
            ("foundation", ["bash", "scripts/check-foundation.sh"]),
            ("root toolchain", ["bash", "scripts/check-root-toolchain.sh"]),
            ("CI config", ["bash", "scripts/check-ci.sh"]),
            ("GitHub planning", ["python3", "scripts/github/check-github-planning.py"]),
                ("Rust workspace", ["bash", "scripts/check-rust-workspace.sh"]),
        ]

        for name, command in checks:
            code, stdout, stderr = self.run_text(command)
            if code != 0:
                self.fail(f"{name} check failed: {stderr or stdout}")
            else:
                self.ok(f"{name} check passed")

    def run(self) -> int:
        self.check_required_files()
        self.check_required_directories()
        self.check_package_json()
        self.check_git()
        self.check_runtime_commands()
        self.check_node_modules_tools()
        self.check_github_cli_auth()
        self.check_subcommands()

        print()
        print("Monad Factory Doctor")
        print("====================")

        for finding in self.findings:
            print(f"[{finding.level}] {finding.message}")

        failures = [finding for finding in self.findings if finding.level == "FAIL"]
        warnings = [finding for finding in self.findings if finding.level == "WARN"]

        print()
        print(f"Summary: {len(failures)} failure(s), {len(warnings)} warning(s)")

        if failures:
            return 1

        if self.strict and warnings:
            return 1

        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Monad Factory repository doctor checks.")
    parser.add_argument("--ci", action="store_true", help="Run in CI-safe mode.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    args = parser.parse_args()

    doctor = Doctor(ci=args.ci, strict=args.strict)
    raise SystemExit(doctor.run())


if __name__ == "__main__":
    main()
