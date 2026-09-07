#!/usr/bin/env python3
"""Exercise positive and negative source-alignment validator fixtures."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_source_alignment.py"


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


def copy_fixture(name: str) -> Path:
    target = Path(tempfile.mkdtemp(prefix=f"sonus-source-alignment-{name}-"))
    shutil.copytree(ROOT / "governance", target / "governance")
    return target


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    baseline = run(ROOT)
    require(
        baseline.returncode == 0,
        f"baseline must pass\nstdout:\n{baseline.stdout}\nstderr:\n{baseline.stderr}",
    )
    require("canonicalDigest=sha256:" in baseline.stdout, "baseline must emit a canonical digest")

    wrong_org = copy_fixture("wrong-org")
    manifest_path = wrong_org / "governance" / "source-of-truth.toml"
    manifest = manifest_path.read_text(encoding="utf-8")
    manifest_path.write_text(
        manifest.replace(
            'organization = "sonus-auris"',
            'organization = "different-org"',
            1,
        ),
        encoding="utf-8",
    )
    result = run(wrong_org)
    require(result.returncode != 0, "wrong organization fixture must fail")
    require("organization must be sonus-auris" in result.stderr, result.stderr)

    missing_mapping = copy_fixture("missing-mapping")
    manifest_path = missing_mapping / "governance" / "source-of-truth.toml"
    manifest = manifest_path.read_text(encoding="utf-8")
    block = '''[[mappings]]
kind = "githubProject"
status = "unverified"
note = "The current GitHub connector exposes no Projects-v2 read/write operation; do not invent a project number or claim issue synchronization."

'''
    require(block in manifest, "GitHub Project fixture block must exist")
    manifest_path.write_text(manifest.replace(block, "", 1), encoding="utf-8")
    result = run(missing_mapping)
    require(result.returncode != 0, "missing mapping fixture must fail")
    require("required mapping kinds are missing" in result.stderr, result.stderr)

    enum_drift = copy_fixture("enum-drift")
    typespec_path = enum_drift / "governance" / "source-of-truth.tsp"
    typespec = typespec_path.read_text(encoding="utf-8")
    require("  pubLibCore,\n" in typespec, "TypeSpec enum fixture member must exist")
    typespec_path.write_text(
        typespec.replace("  pubLibCore,\n", "  pubLibCoreExtra,\n", 1),
        encoding="utf-8",
    )
    result = run(enum_drift)
    require(result.returncode != 0, "TypeSpec/JSON Schema enum drift fixture must fail")
    require("TypeSpec enum RepositoryRole differs" in result.stderr, result.stderr)

    print("source-alignment validator fixtures passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
