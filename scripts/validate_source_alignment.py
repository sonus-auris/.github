#!/usr/bin/env python3
"""Validate Sonus Auris organization governance contracts without network access.

The validator deliberately uses only the Python standard library so pull-request
checks do not depend on an unpinned package index. It validates JSON/TOML syntax,
TypeSpec/JSON-Schema declaration parity, canonical manifest invariants, and emits
a deterministic normalized manifest digest for repository mirror pointers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Any

CANONICAL_SCHEMA_VERSION = "ores.organization-source-of-truth.v1"
POINTER_SCHEMA_VERSION = "ores.organization-source-of-truth-pointer.v1"
ORGANIZATION = "sonus-auris"
AUTHORITY_REPOSITORY = "sonus-auris/.github"
CANONICAL_PATH = "governance/source-of-truth.toml"
JSON_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"

RESOURCE_STATUSES = {
    "verified",
    "declared",
    "drift",
    "missing",
    "blocked",
    "unverified",
}
REPOSITORY_VISIBILITIES = {"public", "private", "internal", "unknown"}
REPOSITORY_ROLES = {
    "canonical",
    "documentation",
    "marketing",
    "mcpServer",
    "cli",
    "interfaces",
    "clients",
    "monorepo",
    "infrastructure",
    "desktopRust",
    "flutter",
    "lambdas",
    "apiServer",
    "adminApiServer",
    "webServer",
    "adminWebServer",
    "libCore",
    "ormCore",
    "pubLibCore",
    "sync",
    "other",
}
MAPPING_KINDS = {
    "linearProject",
    "githubProject",
    "supabaseOrganization",
    "supabaseNamespace",
    "neonOrganization",
    "cloudflareDomain",
    "gcpProject",
    "slackChannel",
}
REQUIRED_REPOSITORY_ROLES = {
    "canonical": "full",
    "documentation": "pointer",
    "marketing": "pointer",
    "mcpServer": "pointer",
}
REQUIRED_MAPPING_KINDS = {
    "linearProject",
    "githubProject",
    "neonOrganization",
    "cloudflareDomain",
    "gcpProject",
    "slackChannel",
}
MIRROR_STATUSES = {"current", "stale", "blocked", "unverified"}
REPOSITORY_NAME = re.compile(r"^sonus-auris/[A-Za-z0-9_.-]+$")
SHA256_DIGEST = re.compile(r"^sha256:[a-f0-9]{64}$")


class Validation:
    """Accumulate deterministic validation failures."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def finish(self) -> None:
        if not self.errors:
            return
        for error in self.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"ERROR: could not load JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise SystemExit(f"ERROR: JSON root must be an object: {path}")
    return value


def load_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise SystemExit(f"ERROR: could not load TOML {path}: {error}") from error
    if not isinstance(value, dict):
        raise SystemExit(f"ERROR: TOML root must be a table: {path}")
    return value


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(f"ERROR: could not load text {path}: {error}") from error


def parse_typespec(source: str) -> tuple[dict[str, set[str]], dict[str, tuple[set[str], set[str]]]]:
    enums: dict[str, set[str]] = {}
    models: dict[str, tuple[set[str], set[str]]] = {}

    for match in re.finditer(r"\benum\s+([A-Za-z_]\w*)\s*\{(.*?)\}", source, re.DOTALL):
        name, body = match.groups()
        members = {
            member.group(1)
            for member in re.finditer(
                r"^\s*([A-Za-z_]\w*)\s*,?\s*$", body, re.MULTILINE
            )
        }
        enums[name] = members

    for match in re.finditer(r"\bmodel\s+([A-Za-z_]\w*)\s*\{(.*?)\}", source, re.DOTALL):
        name, body = match.groups()
        properties: set[str] = set()
        required: set[str] = set()
        for field in re.finditer(
            r"^\s*([A-Za-z_]\w*)(\?)?\s*:", body, re.MULTILINE
        ):
            field_name, optional = field.groups()
            properties.add(field_name)
            if optional is None:
                required.add(field_name)
        models[name] = (properties, required)

    return enums, models


def schema_properties(schema: dict[str, Any]) -> set[str]:
    properties = schema.get("properties", {})
    return set(properties) if isinstance(properties, dict) else set()


def schema_required(schema: dict[str, Any]) -> set[str]:
    required = schema.get("required", [])
    return set(required) if isinstance(required, list) else set()


def compare_model(
    validation: Validation,
    *,
    model_name: str,
    typespec_models: dict[str, tuple[set[str], set[str]]],
    schema: dict[str, Any],
) -> None:
    validation.require(model_name in typespec_models, f"TypeSpec model {model_name} is missing")
    if model_name not in typespec_models:
        return
    tsp_properties, tsp_required = typespec_models[model_name]
    json_properties = schema_properties(schema)
    json_required = schema_required(schema)
    validation.require(
        tsp_properties == json_properties,
        f"{model_name} property parity differs: TypeSpec={sorted(tsp_properties)} JSON Schema={sorted(json_properties)}",
    )
    validation.require(
        tsp_required == json_required,
        f"{model_name} required-field parity differs: TypeSpec={sorted(tsp_required)} JSON Schema={sorted(json_required)}",
    )


def enum_values(schema: dict[str, Any], definition: str) -> set[str]:
    value = schema.get("$defs", {}).get(definition, {}).get("enum", [])
    return set(value) if isinstance(value, list) else set()


def validate_contract_parity(
    validation: Validation,
    canonical_schema: dict[str, Any],
    canonical_typespec: str,
    pointer_schema: dict[str, Any],
    pointer_typespec: str,
) -> None:
    validation.require(
        canonical_schema.get("$schema") == JSON_SCHEMA_DIALECT,
        "canonical JSON Schema must declare Draft 2020-12",
    )
    validation.require(
        pointer_schema.get("$schema") == JSON_SCHEMA_DIALECT,
        "pointer JSON Schema must declare Draft 2020-12",
    )

    canonical_enums, canonical_models = parse_typespec(canonical_typespec)
    pointer_enums, pointer_models = parse_typespec(pointer_typespec)
    definitions = canonical_schema.get("$defs", {})
    validation.require(isinstance(definitions, dict), "canonical JSON Schema $defs must be an object")
    if not isinstance(definitions, dict):
        definitions = {}

    compare_model(
        validation,
        model_name="OrganizationSourceOfTruth",
        typespec_models=canonical_models,
        schema=canonical_schema,
    )
    for model_name, definition_name in (
        ("RepositorySurface", "repositorySurface"),
        ("ExternalMapping", "externalMapping"),
        ("Supersession", "supersession"),
    ):
        definition = definitions.get(definition_name, {})
        validation.require(
            isinstance(definition, dict),
            f"JSON Schema definition {definition_name} must be an object",
        )
        if isinstance(definition, dict):
            compare_model(
                validation,
                model_name=model_name,
                typespec_models=canonical_models,
                schema=definition,
            )

    for enum_name, definition_name, expected in (
        ("ResourceStatus", "resourceStatus", RESOURCE_STATUSES),
        ("RepositoryVisibility", "visibility", REPOSITORY_VISIBILITIES),
        ("RepositoryRole", "repositoryRole", REPOSITORY_ROLES),
        ("MappingKind", "mappingKind", MAPPING_KINDS),
    ):
        validation.require(
            canonical_enums.get(enum_name) == expected,
            f"TypeSpec enum {enum_name} differs from the expected contract",
        )
        validation.require(
            enum_values(canonical_schema, definition_name) == expected,
            f"JSON Schema enum {definition_name} differs from the expected contract",
        )

    compare_model(
        validation,
        model_name="OrganizationSourceOfTruthPointer",
        typespec_models=pointer_models,
        schema=pointer_schema,
    )
    validation.require(
        pointer_enums.get("MirrorStatus") == MIRROR_STATUSES,
        "TypeSpec MirrorStatus differs from the expected contract",
    )
    status_schema = pointer_schema.get("properties", {}).get("status", {})
    status_values = set(status_schema.get("enum", [])) if isinstance(status_schema, dict) else set()
    validation.require(
        status_values == MIRROR_STATUSES,
        "pointer JSON Schema status enum differs from the expected contract",
    )


def require_keys(
    validation: Validation,
    value: dict[str, Any],
    *,
    allowed: set[str],
    required: set[str],
    target: str,
) -> None:
    keys = set(value)
    validation.require(not (keys - allowed), f"{target} has unknown keys: {sorted(keys - allowed)}")
    validation.require(not (required - keys), f"{target} is missing keys: {sorted(required - keys)}")


def require_timestamp(validation: Validation, value: Any, target: str) -> None:
    validation.require(isinstance(value, str) and bool(value.strip()), f"{target} must be a non-empty timestamp")
    if not isinstance(value, str) or not value.strip():
        return
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        validation.require(False, f"{target} is not an ISO-8601 timestamp: {value!r}")
        return
    validation.require(parsed.tzinfo is not None, f"{target} must include a UTC offset")


def validate_manifest(
    validation: Validation,
    manifest: dict[str, Any],
    canonical_schema: dict[str, Any],
) -> None:
    allowed = schema_properties(canonical_schema)
    required = schema_required(canonical_schema)
    require_keys(validation, manifest, allowed=allowed, required=required, target="manifest")

    validation.require(
        manifest.get("schemaVersion") == CANONICAL_SCHEMA_VERSION,
        f"schemaVersion must be {CANONICAL_SCHEMA_VERSION}",
    )
    revision = manifest.get("revision")
    validation.require(
        isinstance(revision, int) and not isinstance(revision, bool) and revision > 0,
        "revision must be a positive integer",
    )
    validation.require(manifest.get("organization") == ORGANIZATION, f"organization must be {ORGANIZATION}")
    validation.require(
        manifest.get("authorityRepository") == AUTHORITY_REPOSITORY,
        f"authorityRepository must be {AUTHORITY_REPOSITORY}",
    )
    validation.require(manifest.get("canonicalPath") == CANONICAL_PATH, f"canonicalPath must be {CANONICAL_PATH}")
    validation.require(manifest.get("synchronizationPolicy") == "append-only", "synchronizationPolicy must be append-only")
    require_timestamp(validation, manifest.get("reviewedAt"), "reviewedAt")

    repositories = manifest.get("repositories")
    validation.require(isinstance(repositories, list), "repositories must be an array of tables")
    if not isinstance(repositories, list):
        repositories = []
    repository_schema = canonical_schema.get("$defs", {}).get("repositorySurface", {})
    repository_allowed = schema_properties(repository_schema)
    repository_required = schema_required(repository_schema)
    declarations: set[tuple[str, str]] = set()
    role_counts: dict[str, int] = {}

    for index, raw_surface in enumerate(repositories):
        target = f"repositories[{index}]"
        validation.require(isinstance(raw_surface, dict), f"{target} must be a table")
        if not isinstance(raw_surface, dict):
            continue
        require_keys(
            validation,
            raw_surface,
            allowed=repository_allowed,
            required=repository_required,
            target=target,
        )
        role = raw_surface.get("role")
        repository = raw_surface.get("repository")
        status = raw_surface.get("status")
        validation.require(role in REPOSITORY_ROLES, f"{target}.role is unknown: {role!r}")
        validation.require(
            isinstance(repository, str) and REPOSITORY_NAME.fullmatch(repository) is not None,
            f"{target}.repository is not a Sonus owner-qualified name: {repository!r}",
        )
        validation.require(isinstance(raw_surface.get("required"), bool), f"{target}.required must be boolean")
        validation.require(status in RESOURCE_STATUSES, f"{target}.status is unknown: {status!r}")
        if isinstance(role, str):
            role_counts[role] = role_counts.get(role, 0) + 1
        if isinstance(role, str) and isinstance(repository, str):
            key = (role, repository.casefold())
            validation.require(key not in declarations, f"duplicate repository declaration: {role} {repository}")
            declarations.add(key)
        expected_visibility = raw_surface.get("expectedVisibility")
        observed_visibility = raw_surface.get("observedVisibility")
        if expected_visibility is not None:
            validation.require(
                expected_visibility in REPOSITORY_VISIBILITIES,
                f"{target}.expectedVisibility is unknown: {expected_visibility!r}",
            )
        if observed_visibility is not None:
            validation.require(
                observed_visibility in REPOSITORY_VISIBILITIES,
                f"{target}.observedVisibility is unknown: {observed_visibility!r}",
            )
        if status == "verified" and expected_visibility and observed_visibility:
            validation.require(
                expected_visibility == observed_visibility,
                f"{target} is verified but expected/observed visibility differ",
            )
        if status in {"verified", "drift"}:
            evidence = raw_surface.get("evidence")
            validation.require(isinstance(evidence, str) and bool(evidence.strip()), f"{target}.evidence is required")
        mirror_mode = raw_surface.get("mirrorMode")
        if mirror_mode is not None:
            validation.require(mirror_mode in {"full", "pointer", "none"}, f"{target}.mirrorMode is unknown")
        path = raw_surface.get("manifestPath")
        if path is not None:
            validation.require(
                isinstance(path, str)
                and bool(path)
                and not path.startswith("/")
                and "\\" not in path
                and all(segment not in {"", ".", ".."} for segment in path.split("/")),
                f"{target}.manifestPath is unsafe: {path!r}",
            )

    for role, mirror_mode in REQUIRED_REPOSITORY_ROLES.items():
        validation.require(role_counts.get(role, 0) == 1, f"repository role {role} must appear exactly once")
        matches = [surface for surface in repositories if isinstance(surface, dict) and surface.get("role") == role]
        if len(matches) == 1:
            validation.require(
                matches[0].get("mirrorMode") == mirror_mode,
                f"repository role {role} must use mirrorMode={mirror_mode}",
            )
            validation.require(matches[0].get("manifestPath") == CANONICAL_PATH, f"repository role {role} must use {CANONICAL_PATH}")
    cli_matches = [surface for surface in repositories if isinstance(surface, dict) and surface.get("role") == "cli"]
    validation.require(len(cli_matches) <= 1, "repository role cli may appear at most once")
    if cli_matches:
        validation.require(cli_matches[0].get("mirrorMode") == "pointer", "declared CLI must use mirrorMode=pointer")
        validation.require(cli_matches[0].get("manifestPath") == CANONICAL_PATH, f"declared CLI must use {CANONICAL_PATH}")

    canonical_matches = [surface for surface in repositories if isinstance(surface, dict) and surface.get("role") == "canonical"]
    if len(canonical_matches) == 1:
        validation.require(
            canonical_matches[0].get("repository") == AUTHORITY_REPOSITORY,
            "canonical repository declaration must identify sonus-auris/.github",
        )

    mappings = manifest.get("mappings")
    validation.require(isinstance(mappings, list), "mappings must be an array of tables")
    if not isinstance(mappings, list):
        mappings = []
    mapping_schema = canonical_schema.get("$defs", {}).get("externalMapping", {})
    mapping_allowed = schema_properties(mapping_schema)
    mapping_required = schema_required(mapping_schema)
    seen_mapping_kinds: set[str] = set()

    for index, raw_mapping in enumerate(mappings):
        target = f"mappings[{index}]"
        validation.require(isinstance(raw_mapping, dict), f"{target} must be a table")
        if not isinstance(raw_mapping, dict):
            continue
        require_keys(
            validation,
            raw_mapping,
            allowed=mapping_allowed,
            required=mapping_required,
            target=target,
        )
        kind = raw_mapping.get("kind")
        status = raw_mapping.get("status")
        validation.require(kind in MAPPING_KINDS, f"{target}.kind is unknown: {kind!r}")
        validation.require(status in RESOURCE_STATUSES, f"{target}.status is unknown: {status!r}")
        if isinstance(kind, str):
            validation.require(kind not in seen_mapping_kinds, f"duplicate mapping kind: {kind}")
            seen_mapping_kinds.add(kind)
        if status in {"verified", "declared", "drift"}:
            identifier = raw_mapping.get("identifier")
            validation.require(isinstance(identifier, str) and bool(identifier.strip()), f"{target}.identifier is required")
        if status == "verified":
            evidence = raw_mapping.get("evidence")
            validation.require(isinstance(evidence, str) and bool(evidence.strip()), f"{target}.evidence is required")

    validation.require(
        REQUIRED_MAPPING_KINDS <= seen_mapping_kinds,
        f"required mapping kinds are missing: {sorted(REQUIRED_MAPPING_KINDS - seen_mapping_kinds)}",
    )
    validation.require(
        bool({"supabaseOrganization", "supabaseNamespace"} & seen_mapping_kinds),
        "a Supabase organization or namespace mapping is required",
    )

    supersessions = manifest.get("supersessions")
    validation.require(isinstance(supersessions, list), "supersessions must be an array of tables")
    if not isinstance(supersessions, list):
        supersessions = []
    supersession_schema = canonical_schema.get("$defs", {}).get("supersession", {})
    supersession_allowed = schema_properties(supersession_schema)
    supersession_required = schema_required(supersession_schema)
    for index, raw_supersession in enumerate(supersessions, start=1):
        target = f"supersessions[{index - 1}]"
        validation.require(isinstance(raw_supersession, dict), f"{target} must be a table")
        if not isinstance(raw_supersession, dict):
            continue
        require_keys(
            validation,
            raw_supersession,
            allowed=supersession_allowed,
            required=supersession_required,
            target=target,
        )
        validation.require(raw_supersession.get("sequence") == index, f"{target}.sequence must be {index}")
        require_timestamp(validation, raw_supersession.get("recordedAt"), f"{target}.recordedAt")
        for field in ("formerStatement", "replacementStatement", "reason", "evidence"):
            value = raw_supersession.get(field)
            validation.require(isinstance(value, str) and bool(value.strip()), f"{target}.{field} must be non-empty")


def normalized_digest(manifest: dict[str, Any]) -> str:
    payload = json.dumps(
        manifest,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve()
    governance = root / "governance"

    canonical_schema = load_json(governance / "source-of-truth.schema.json")
    pointer_schema = load_json(governance / "mirror-pointer.schema.json")
    canonical_typespec = load_text(governance / "source-of-truth.tsp")
    pointer_typespec = load_text(governance / "mirror-pointer.tsp")
    manifest = load_toml(governance / "source-of-truth.toml")

    validation = Validation()
    validate_contract_parity(
        validation,
        canonical_schema,
        canonical_typespec,
        pointer_schema,
        pointer_typespec,
    )
    validate_manifest(validation, manifest, canonical_schema)
    validation.require(
        pointer_schema.get("properties", {}).get("schemaVersion", {}).get("const")
        == POINTER_SCHEMA_VERSION,
        f"pointer schemaVersion const must be {POINTER_SCHEMA_VERSION}",
    )
    digest = normalized_digest(manifest)
    validation.require(SHA256_DIGEST.fullmatch(digest) is not None, "internal digest generation failed")
    validation.finish()

    print(
        "validated source alignment "
        f"organization={manifest['organization']} "
        f"revision={manifest['revision']} "
        f"repositories={len(manifest['repositories'])} "
        f"mappings={len(manifest['mappings'])} "
        f"supersessions={len(manifest['supersessions'])} "
        f"canonicalDigest={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
