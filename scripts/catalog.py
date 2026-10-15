#!/usr/bin/env python3
"""Validate, render, and monitor the curated Ollama catalog (standard library only)."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import html
import http.client
import json
import math
from pathlib import Path
import re
import ssl
import sys
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- BEGIN GENERATED CATALOG -->"
END = "<!-- END GENERATED CATALOG -->"
API_URL = "https://ollama.com/api/tags"
MAX_BYTES = 2 * 1024 * 1024
TAG = re.compile(r"[a-z0-9][a-z0-9._-]*(?::[a-z0-9][a-z0-9._-]*)?\Z")
STATUSES = {"active", "retiring", "retired", "unknown"}
FIELDS = {
    "id", "display_name", "provider", "family", "cloud_api_tag", "cli_cloud_tag",
    "local_tag", "context_window", "modalities", "tools", "thinking", "status",
    "sources", "verified_on", "use_cases", "notes", "pricing",
}


class CatalogError(ValueError):
    """Invalid data or stale generated documentation."""


class MonitoringError(ValueError):
    """The remote listing could not be safely interpreted."""


def require(condition, message):
    if not condition:
        raise CatalogError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CatalogError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise CatalogError(f"non-finite JSON number: {value}")


def decode_json(raw):
    try:
        return json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (json.JSONDecodeError, UnicodeError, RecursionError) as exc:
        raise CatalogError(f"invalid JSON: {exc}") from exc


def iso_date(value, field):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value),
            f"{field}: expected YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise CatalogError(f"{field}: invalid date {value!r}") from exc


def text(value, field):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 2000,
            f"{field}: expected nonempty text (at most 2000 characters)")
    require(not any(ord(c) < 32 and c not in "\n\t" for c in value),
            f"{field}: control characters are not allowed")


def tag(value, field):
    require(isinstance(value, str) and len(value) <= 128 and TAG.fullmatch(value),
            f"{field}: invalid model tag {value!r}")


def source_url(value, field):
    require(isinstance(value, str), f"{field}: expected URL string")
    try:
        u = urlsplit(value)
        valid = (u.scheme == "https" and u.netloc in {"ollama.com", "docs.ollama.com"}
                 and not any(c.isspace() or c in '<>\\\"' for c in value))
    except ValueError:
        valid = False
    require(valid, f"{field}: expected an official HTTPS Ollama URL")


def validate_catalog(data):
    require(isinstance(data, dict), "catalog: expected an object")
    require(set(data) == {"schema_version", "verified_on", "models"},
            "catalog: expected only schema_version, verified_on, models")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "schema_version: expected integer 1")
    snapshot = iso_date(data["verified_on"], "verified_on")
    require(isinstance(data["models"], list) and 0 < len(data["models"]) <= 1000,
            "models: expected 1..1000 entries")
    ids, cloud_tags, cli_tags, local_tags = set(), set(), set(), set()
    for index, model in enumerate(data["models"]):
        label = f"models[{index}]"
        require(isinstance(model, dict), f"{label}: expected an object")
        require(set(model) == FIELDS,
                f"{label}: missing fields {sorted(FIELDS - set(model))}; "
                f"unknown fields {sorted(set(model) - FIELDS)}")
        tag(model["id"], f"{label}.id")
        require(model["id"] not in ids, f"duplicate model identifier: {model['id']}")
        ids.add(model["id"])
        for field in ("display_name", "provider", "family"):
            text(model[field], f"{label}.{field}")
        require(model["status"] in STATUSES if isinstance(model["status"], str) else False,
                f"{label}.status: expected one of {sorted(STATUSES)}")
        for field, seen in (("cloud_api_tag", cloud_tags), ("cli_cloud_tag", cli_tags),
                            ("local_tag", local_tags)):
            value = model[field]
            if value is not None:
                tag(value, f"{label}.{field}")
                require(value not in seen, f"duplicate {field}: {value}")
                seen.add(value)
        cloud, cli, local = (model[k] for k in ("cloud_api_tag", "cli_cloud_tag", "local_tag"))
        require((cloud is None) == (cli is None), f"{label}: cloud API and CLI tags must be paired")
        require(cloud is not None or local is not None, f"{label}: verify at least one execution tag")
        require(model["id"] == (cloud or local), f"{label}.id: must equal the API tag or local-only tag")
        if cloud is not None:
            require(not cloud.endswith((":cloud", "-cloud")), f"{label}: API tag cannot use cloud suffix")
            require(cli.endswith((":cloud", "-cloud")), f"{label}: CLI cloud tag needs cloud suffix")
        if local is not None:
            require(not local.endswith((":cloud", "-cloud")), f"{label}: local tag cannot use cloud suffix")
        context = model["context_window"]
        require(context is None or (isinstance(context, str) and
                re.fullmatch(r"[1-9]\d*(?:\.\d+)?[KM]?", context)),
                f"{label}.context_window: expected published label such as 256K, or null")
        for field, allowed in (("modalities", {"text", "image", "audio", "video"}),):
            values = model[field]
            require(isinstance(values, list) and bool(values), f"{label}.{field}: expected a nonempty list")
            require(all(isinstance(v, str) and v in allowed for v in values), f"{label}.{field}: invalid modality")
            require(len(values) == len(set(values)), f"{label}.{field}: duplicate value")
        for field in ("tools", "thinking"):
            require(model[field] is None or type(model[field]) is bool,
                    f"{label}.{field}: expected boolean or null")
        verified = iso_date(model["verified_on"], f"{label}.verified_on")
        require(verified <= snapshot, f"{label}.verified_on: after catalog verification date")
        for field in ("sources", "use_cases"):
            values = model[field]
            require(isinstance(values, list) and bool(values), f"{label}.{field}: expected a nonempty list")
            for value in values:
                if field == "sources": source_url(value, f"{label}.{field}")
                else: text(value, f"{label}.{field}")
        if model["notes"] is not None:
            text(model["notes"], f"{label}.notes")
        pricing = model["pricing"]
        if pricing is not None:
            require(cloud is not None, f"{label}.pricing: cloud pricing needs a cloud tag")
            require(isinstance(pricing, dict) and set(pricing) == {
                "usd_per_million_input", "usd_per_million_cached_input", "usd_per_million_output",
                "source", "verified_on", "notes"}, f"{label}.pricing: invalid fields")
            for field in ("usd_per_million_input", "usd_per_million_cached_input", "usd_per_million_output"):
                n = pricing[field]
                require(n is None or (type(n) in (int, float) and 0 <= n <= 1_000_000 and math.isfinite(n)),
                        f"{label}.pricing.{field}: expected nonnegative finite number or null")
            source_url(pricing["source"], f"{label}.pricing.source")
            require(iso_date(pricing["verified_on"], f"{label}.pricing.verified_on") <= snapshot,
                    f"{label}.pricing.verified_on: after catalog date")
            if pricing["notes"] is not None: text(pricing["notes"], f"{label}.pricing.notes")
    return data


def load_catalog(path):
    raw = Path(path).read_bytes()
    require(len(raw) <= MAX_BYTES, "catalog exceeds 2 MiB")
    return validate_catalog(decode_json(raw))


def md(value):
    """Escape text, not raw Markdown; input is never interpreted as HTML."""
    value = re.sub(r"([\\`*_{}\[\]()#+!|])", r"\\\1", str(value))
    value = html.escape(value, quote=False)
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def code(value):
    return f"`{value}`" if value is not None else "Not verified"


def support(value):
    return "Yes" if value is True else "No" if value is False else "Not verified"


def render_table(data):
    rows = ["| Model / direct Cloud API ID | CLI cloud tag | Verified local tag | Context label | Input | Tools / thinking |",
            "|---|---|---|---|---|---|"]
    for m in sorted(data["models"], key=lambda m: m["id"]):
        if m["status"] not in {"active", "retiring"}: continue
        name = code(m["cloud_api_tag"]) if m["cloud_api_tag"] else md(m["display_name"]) + " (local only)"
        rows.append("| " + " | ".join([
            name, code(m["cli_cloud_tag"]), code(m["local_tag"]),
            md(m["context_window"] or "Not verified"), ", ".join(m["modalities"]),
            support(m["tools"]) + " / " + support(m["thinking"]),
        ]) + " |")
    return "\n".join(rows)


def render_catalog(data):
    out = ["# Model catalog", "", "<!-- Generated by scripts/catalog.py; edit data/models.json. -->", "",
           f"Verified {data['verified_on']}. Context labels are copied from tag pages; K/M are not converted into exact token counts.", "",
           "This is a curated snapshot, not a promise of account access or future availability. A missing local tag means local availability was not verified in this audit.", "",
           render_table(data), "", "## Published cloud prices", "",
           "USD per million tokens, as verified per entry. These are snapshots; consult each linked source before spending. A dash means unverified, not free.", "",
           "| Direct API ID | Input | Cached input | Output | Source |",
           "|---|---:|---:|---:|---|"]
    for m in sorted(data["models"], key=lambda m: m["id"]):
        p = m["pricing"]
        if p is None: continue
        prices = ["—" if p[k] is None else f"${p[k]:g}" for k in (
            "usd_per_million_input", "usd_per_million_cached_input", "usd_per_million_output")]
        out.append("| " + " | ".join([code(m["cloud_api_tag"]), *prices, f"[Official](<{p['source']}>)"]) + " |")
    out += ["", "## Evidence and lifecycle", "",
            "Active means observed in the official listing or verified local tag page on the stated date. Drift alone does not establish retirement. Unknown fields remain null in the data."]
    for m in sorted(data["models"], key=lambda m: m["id"]):
        out += ["", f"### {md(m['display_name'])}", "",
                f"- ID: {code(m['id'])}; provider: {md(m['provider'])}; family: {md(m['family'])}.",
                f"- Lifecycle: {m['status']}; verified {m['verified_on']}.",
                f"- Documented uses: {', '.join(md(v) for v in m['use_cases'])}.",
                "- Evidence: " + ", ".join(f"[Official source {i+1}](<{u}>)" for i, u in enumerate(m["sources"])) + "."]
        if m["notes"]: out.append("- Verification notes: " + md(m["notes"]))
        if m["pricing"] and m["pricing"]["notes"]:
            out.append("- Pricing notes: " + md(m["pricing"]["notes"]))
    return "\n".join(out) + "\n"


def update_readme(original, data):
    require(original.count(START) == original.count(END) == 1,
            "README.md: expected exactly one BEGIN/END GENERATED CATALOG marker pair")
    begin, end = original.index(START) + len(START), original.index(END)
    require(begin < end, "README.md: generated catalog markers are reversed")
    return original[:begin] + "\n\n" + render_table(data) + "\n\n" + original[end:]


def generate(data, root, check=False):
    root = Path(root)
    # Compute both outputs before writing either: marker errors cannot partially regenerate docs.
    outputs = {root / "MODEL_CATALOG.md": render_catalog(data),
               root / "README.md": update_readme((root / "README.md").read_text(encoding="utf-8"), data)}
    stale = [p.name for p, value in outputs.items()
             if not p.exists() or p.read_text(encoding="utf-8") != value]
    if check:
        require(not stale, f"stale generated docs: {', '.join(stale)}; run python scripts/catalog.py generate")
    else:
        for path, value in outputs.items():
            path.write_text(value, encoding="utf-8", newline="\n")
    return stale


def parse_live(data):
    if not isinstance(data, dict) or not isinstance(data.get("models"), list):
        raise MonitoringError("listing must contain a models array")
    models = data["models"]
    if not 0 < len(models) <= 1000:
        raise MonitoringError("listing must contain 1..1000 models; empty responses need manual review")
    ids = set()
    for item in models:
        if not isinstance(item, dict): raise MonitoringError("listing model must be an object")
        name = item.get("name", item.get("model"))
        try:
            tag(name, "live identifier")
        except CatalogError as exc:
            raise MonitoringError(str(exc)) from exc
        if "name" in item and "model" in item and item["name"] != item["model"]:
            raise MonitoringError("listing name and model identifiers disagree")
        if name.endswith((":cloud", "-cloud")):
            raise MonitoringError("direct cloud identifier unexpectedly uses CLI suffix")
        if name in ids: raise MonitoringError(f"duplicate live identifier: {name}")
        ids.add(name)
    return ids


def retry_delay(header, attempt):
    default = min(2 ** attempt, 8)
    if header is None: return default
    try:
        seconds = int(header)
    except (ValueError, TypeError):
        try:
            when = parsedate_to_datetime(header)
            if when.tzinfo is None: when = when.replace(tzinfo=timezone.utc)
            seconds = (when - datetime.now(timezone.utc)).total_seconds()
        except (ValueError, TypeError, OverflowError):
            return default
    return min(60, max(0, seconds))


def fetch_live(*, connection_factory=http.client.HTTPSConnection, sleep=time.sleep,
               connect_timeout=10, response_timeout=30, attempts=3):
    """Fixed public HTTPS endpoint; no credentials, redirects, or arbitrary URL input."""
    if type(attempts) is not int or not 1 <= attempts <= 3 or not 0 < connect_timeout <= 30 or not 0 < response_timeout <= 60:
        raise MonitoringError("timeouts/attempts exceed monitoring bounds")
    transient = {429, 500, 502, 503, 504}
    for attempt in range(attempts):
        conn = connection_factory("ollama.com", timeout=connect_timeout)
        delay = min(2 ** attempt, 8)
        try:
            conn.connect()
            conn.sock.settimeout(response_timeout)
            conn.request("GET", "/api/tags", headers={"Accept": "application/json",
                         "User-Agent": "awesome-ollama-models-drift/1.0"})
            response = conn.getresponse()
            if response.status == 200:
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES: raise MonitoringError("listing exceeds 2 MiB")
                try:
                    return parse_live(decode_json(raw))
                except CatalogError as exc:
                    raise MonitoringError(f"malformed listing: {exc}") from exc
            if response.status not in transient:
                raise MonitoringError(f"HTTP {response.status}: polling stopped; check endpoint/access (no retry)")
            delay = retry_delay(response.getheader("Retry-After"), attempt)
            error = f"HTTP {response.status} after {attempt + 1} attempt(s)"
        except ssl.SSLCertVerificationError as exc:
            raise MonitoringError("TLS certificate validation failed; polling stopped") from exc
        except (OSError, http.client.HTTPException) as exc:
            error = f"network failure ({type(exc).__name__}) after {attempt + 1} attempt(s)"
        finally:
            conn.close()
        if attempt < attempts - 1: sleep(delay)
    raise MonitoringError(error)


def compare(data, live):
    expected = {m["cloud_api_tag"] for m in data["models"]
                if m["cloud_api_tag"] and m["status"] in {"active", "retiring"}}
    return {"added": sorted(live - expected), "removed": sorted(expected - live)}


def drift_report(changes):
    digest = hashlib.sha256(json.dumps(changes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    lines = ["<!-- ollama-catalog-drift:v1 -->", f"<!-- change-digest:{digest} -->", "# Ollama cloud catalog drift", "",
             f"Compared with [the public Cloud API listing]({API_URL}).", "",
             "A missing identifier is an observation, not proof of deprecation. Check aliases, account availability, model pages, context, pricing, and lifecycle before editing the catalog."]
    for name in ("added", "removed"):
        lines += ["", f"## {name.title()}", ""]
        lines += [f"- {code(value)}" for value in changes[name]] or ["None."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "data/models.json")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    gen = commands.add_parser("generate")
    gen.add_argument("--check", action="store_true")
    drift = commands.add_parser("drift")
    drift.add_argument("--output-dir", type=Path, default=ROOT / "reports")
    args = parser.parse_args(argv)
    try:
        data = load_catalog(args.catalog)
        if args.command == "validate":
            print(f"Catalog valid: {len(data['models'])} entries; verified {data['verified_on']}")
        elif args.command == "generate":
            generate(data, ROOT, args.check)
            print("Generated documentation is current" if args.check else "Generated README.md catalog block and MODEL_CATALOG.md")
        else:
            # Remove previous results first: a failed poll must never publish stale drift.
            args.output_dir.mkdir(parents=True, exist_ok=True)
            for name in ("drift.json", "drift.md"):
                (args.output_dir / name).unlink(missing_ok=True)
            changes = compare(data, fetch_live())
            (args.output_dir / "drift.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8", newline="\n")
            (args.output_dir / "drift.md").write_text(drift_report(changes), encoding="utf-8", newline="\n")
            print(f"Cloud drift: {len(changes['added'])} added, {len(changes['removed'])} removed")
    except (CatalogError, MonitoringError, OSError) as exc:
        print(f"{args.command} failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
