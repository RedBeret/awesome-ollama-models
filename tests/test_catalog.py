import copy
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
import http.client
import io
import json
from pathlib import Path
import ssl
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import catalog as c

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = c.load_catalog(ROOT / "data/models.json")

    def test_valid_catalog_and_captured_live_fixture(self):
        live = c.parse_live(json.loads((ROOT / "tests/fixtures/cloud-tags.json").read_text()))
        self.assertEqual(c.compare(self.data, live), {"added": [], "removed": []})
        self.assertEqual(len(self.data["models"]), 20)

    def test_missing_unknown_and_wrong_fields(self):
        for change in (lambda m: m.pop("sources"), lambda m: m.update(extra="typo"),
                       lambda m: m.update(tools="yes"), lambda m: m.update(modalities="text"),
                       lambda m: m.update(modalities=[[]]), lambda m: m.update(status=[]),
                       lambda m: m.update(context_window=True), lambda m: m.update(use_cases=[]),
                       lambda m: m.update(sources=[123])):
            with self.subTest(change=change):
                data = copy.deepcopy(self.data); change(data["models"][0])
                with self.assertRaises(c.CatalogError): c.validate_catalog(data)

    def test_invalid_top_level(self):
        for data in ([], {}, {**self.data, "schema_version": True}, {**self.data, "models": []}):
            with self.subTest(data=type(data)):
                with self.assertRaises(c.CatalogError): c.validate_catalog(data)

    def test_duplicate_model_and_duplicate_execution_tags(self):
        data = copy.deepcopy(self.data)
        data["models"].append(copy.deepcopy(data["models"][0]))
        with self.assertRaisesRegex(c.CatalogError, "duplicate model identifier"):
            c.validate_catalog(data)
        data = copy.deepcopy(self.data)
        data["models"][1]["cli_cloud_tag"] = data["models"][0]["cli_cloud_tag"]
        with self.assertRaisesRegex(c.CatalogError, "duplicate cli_cloud_tag"):
            c.validate_catalog(data)

    def test_invalid_dates_and_status(self):
        for field, value in (("verified_on", "2026-02-30"), ("verified_on", "20261014"),
                             ("verified_on", "2026-10-15"), ("status", "deprecated-ish")):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data); data["models"][0][field] = value
                with self.assertRaises(c.CatalogError): c.validate_catalog(data)

    def test_invalid_tags_and_unpaired_cloud_metadata(self):
        for field, value in (("id", "bad tag"), ("id", "[inject](url)"),
                             ("cloud_api_tag", "thing:cloud"), ("local_tag", "thing:cloud"),
                             ("cli_cloud_tag", "thing:plain"), ("cli_cloud_tag", None)):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data); data["models"][0][field] = value
                with self.assertRaises(c.CatalogError): c.validate_catalog(data)

    def test_invalid_urls(self):
        for url in ("http://ollama.com/library/gemma4", "https://ollama.com.evil.test/x",
                    "https://user@ollama.com/x", "https://ollama.com/x\n", "javascript:alert(1)"):
            with self.subTest(url=url):
                data = copy.deepcopy(self.data); data["models"][0]["sources"] = [url]
                with self.assertRaises(c.CatalogError): c.validate_catalog(data)

    def test_invalid_prices(self):
        for price in (-1, True, "free", float("nan"), float("inf"), 10 ** 1000):
            with self.subTest(price=price):
                data = copy.deepcopy(self.data)
                data["models"][0]["pricing"]["usd_per_million_input"] = price
                with self.assertRaises(c.CatalogError): c.validate_catalog(data)

    def test_json_rejects_duplicate_keys_and_nonfinite_numbers(self):
        for raw in ('{"id":1,"id":2}', '{"x":NaN}', '{"x":Infinity}', '{broken', b'\xff'):
            with self.subTest(raw=raw):
                with self.assertRaises(c.CatalogError): c.decode_json(raw)

    def test_render_is_deterministic_and_sorts_models(self):
        reversed_data = copy.deepcopy(self.data); reversed_data["models"].reverse()
        self.assertEqual(c.render_catalog(self.data), c.render_catalog(reversed_data))
        self.assertEqual(c.render_table(self.data), c.render_table(reversed_data))
        self.assertNotIn("datetime", c.render_catalog(self.data))

    def test_markdown_escaping(self):
        rendered = c.md("a|b\n<script> [x](bad) `code` *bold* " + chr(92))
        self.assertEqual(rendered, r"a\|b<br>&lt;script&gt; \[x\]\(bad\) \`code\` \*bold\* " + chr(92) * 2)
        self.assertEqual(c.md("variant's & <tag>"), "variant's &amp; &lt;tag&gt;")

    def test_readme_preserves_surrounding_sections(self):
        original = f"prefix\n{c.START}\nold\n{c.END}\nsuffix\n"
        result = c.update_readme(original, self.data)
        self.assertTrue(result.startswith("prefix\n" + c.START))
        self.assertTrue(result.endswith(c.END + "\nsuffix\n"))
        self.assertEqual(c.update_readme(result, self.data), result)

    def test_invalid_markers(self):
        for original in ("none", c.START, c.END + c.START, c.START + c.START + c.END):
            with self.subTest(original=original):
                with self.assertRaises(c.CatalogError): c.update_readme(original, self.data)

    def test_generation_stale_check_and_no_writes_in_check_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text(f"keep\n{c.START}\nold\n{c.END}\nkeep\n", encoding="utf-8")
            before = readme.read_bytes()
            with self.assertRaisesRegex(c.CatalogError, "stale generated docs"):
                c.generate(self.data, root, check=True)
            self.assertEqual(readme.read_bytes(), before)
            self.assertFalse((root / "MODEL_CATALOG.md").exists())
            c.generate(self.data, root)
            self.assertEqual(c.generate(self.data, root, check=True), [])
            (root / "MODEL_CATALOG.md").write_text("stale", encoding="utf-8")
            with self.assertRaisesRegex(c.CatalogError, "MODEL_CATALOG.md"):
                c.generate(self.data, root, check=True)

    def test_marker_failure_does_not_partially_write_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / "README.md").write_text("no markers")
            with self.assertRaises(c.CatalogError): c.generate(self.data, root)
            self.assertFalse((root / "MODEL_CATALOG.md").exists())

    def test_add_remove_comparison_and_report(self):
        live = c.parse_live({"models": [{"name": "new-model"}]})
        changes = c.compare(self.data, live)
        self.assertEqual(changes["added"], ["new-model"])
        self.assertEqual(len(changes["removed"]), 18)
        report = c.drift_report(changes)
        self.assertIn("not proof of deprecation", report)
        self.assertEqual(c.drift_report(changes), report)
        changed = c.drift_report({"added": ["other-model"], "removed": []})
        self.assertNotEqual(report.splitlines()[1], changed.splitlines()[1])

    def test_retired_and_local_only_excluded_from_drift_baseline(self):
        data = copy.deepcopy(self.data); data["models"][0]["status"] = "retired"
        expected = {m["cloud_api_tag"] for m in data["models"] if m["cloud_api_tag"] and m["status"] == "active"}
        self.assertEqual(c.compare(data, expected), {"added": [], "removed": []})

    def test_added_only(self):
        live = {m["cloud_api_tag"] for m in self.data["models"] if m["cloud_api_tag"]}
        self.assertEqual(c.compare(self.data, live | {"new-model"}), {"added": ["new-model"], "removed": []})

    def test_removed_only(self):
        live = {m["cloud_api_tag"] for m in self.data["models"] if m["cloud_api_tag"]}
        removed = sorted(live)[0]
        self.assertEqual(c.compare(self.data, live - {removed}), {"added": [], "removed": [removed]})

    def test_malformed_api_listing(self):
        for data in ([], {}, {"models": []}, {"models": "wrong"}, {"models": [None]},
                     {"models": [{"name": "bad tag"}]},
                     {"models": [{"name": "a", "model": "b"}]},
                     {"models": [{"name": "a"}, {"name": "a"}]},
                     {"models": [{"name": "a:cloud"}]}):
            with self.subTest(data=data):
                with self.assertRaises(c.MonitoringError): c.parse_live(data)

    def test_cli_failure_has_actionable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"; path.write_text("{}")
            with patch("sys.stderr", new_callable=io.StringIO) as stderr:
                self.assertEqual(c.main(["--catalog", str(path), "validate"]), 1)
                self.assertIn("validate failed:", stderr.getvalue())

    def test_failed_poll_removes_stale_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            for name in ("drift.json", "drift.md"): (output / name).write_text("stale")
            with patch.object(c, "fetch_live", side_effect=c.MonitoringError("HTTP 503")), patch("sys.stderr", new_callable=io.StringIO):
                self.assertEqual(c.main(["drift", "--output-dir", directory]), 1)
            self.assertEqual(list(output.iterdir()), [])

    def test_invalid_local_catalog_also_removes_stale_reports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); output = root / "reports"; output.mkdir()
            for name in ("drift.json", "drift.md"): (output / name).write_text("stale")
            bad = root / "bad.json"; bad.write_text("{}")
            with patch("sys.stderr", new_callable=io.StringIO), patch.object(c, "fetch_live") as fetch:
                self.assertEqual(c.main(["--catalog", str(bad), "drift", "--output-dir", str(output)]), 1)
                fetch.assert_not_called()
            self.assertEqual(list(output.iterdir()), [])


class NetworkTests(unittest.TestCase):
    def response(self, status=200, body=b'{"models":[{"name":"a"}]}', retry=None):
        response = Mock(status=status)
        response.read.return_value = body
        response.getheader.return_value = retry
        return response

    def run_fetch(self, responses, **kwargs):
        connections = []
        for response in responses:
            conn = Mock()
            if isinstance(response, Exception): conn.connect.side_effect = response
            else: conn.getresponse.return_value = response
            connections.append(conn)
        factory = Mock(side_effect=connections); sleep = Mock()
        result = c.fetch_live(connection_factory=factory, sleep=sleep, **kwargs)
        return result, factory, sleep, connections

    def test_success_and_separate_timeouts(self):
        result, factory, sleep, connections = self.run_fetch([self.response()])
        self.assertEqual(result, {"a"})
        factory.assert_called_once_with("ollama.com", timeout=10)
        connections[0].sock.settimeout.assert_called_once_with(30)
        connections[0].request.assert_called_once()
        self.assertNotIn("Authorization", connections[0].request.call_args.kwargs["headers"])
        connections[0].close.assert_called_once(); sleep.assert_not_called()

    def test_transient_http_and_network_retry_then_success(self):
        for failure in (self.response(429, retry="9999"), self.response(503),
                        TimeoutError(), OSError(), http.client.RemoteDisconnected()):
            with self.subTest(failure=failure):
                result, _, sleep, connections = self.run_fetch([failure, self.response()])
                self.assertEqual(result, {"a"}); self.assertEqual(sleep.call_count, 1)
                self.assertLessEqual(sleep.call_args.args[0], 60)
                for conn in connections: conn.close.assert_called_once()

    def test_auth_and_permanent_http_errors_do_not_retry(self):
        for status in (301, 400, 401, 403, 404):
            factory = Mock(); conn = factory.return_value
            conn.getresponse.return_value = self.response(status)
            sleep = Mock()
            with self.subTest(status=status):
                with self.assertRaisesRegex(c.MonitoringError, f"HTTP {status}"):
                    c.fetch_live(connection_factory=factory, sleep=sleep)
                factory.assert_called_once(); sleep.assert_not_called(); conn.close.assert_called_once()

    def test_retry_exhaustion_is_monitoring_error(self):
        factory = Mock(); factory.return_value.getresponse.return_value = self.response(502)
        sleep = Mock()
        with self.assertRaisesRegex(c.MonitoringError, "HTTP 502 after 3"):
            c.fetch_live(connection_factory=factory, sleep=sleep)
        self.assertEqual(factory.call_count, 3); self.assertEqual(sleep.call_count, 2)

    def test_certificate_failure_stops(self):
        factory = Mock(); factory.return_value.connect.side_effect = ssl.SSLCertVerificationError()
        sleep = Mock()
        with self.assertRaisesRegex(c.MonitoringError, "TLS certificate"):
            c.fetch_live(connection_factory=factory, sleep=sleep)
        factory.assert_called_once(); sleep.assert_not_called()

    def test_invalid_json_oversize_and_empty_are_errors_not_removals(self):
        for body in (b'{broken', b'\xff', b'{"models":[]}', b'x' * (c.MAX_BYTES + 1)):
            factory = Mock(); factory.return_value.getresponse.return_value = self.response(body=body)
            sleep = Mock()
            with self.subTest(body_length=len(body)):
                with self.assertRaises(c.MonitoringError): c.fetch_live(connection_factory=factory, sleep=sleep)
                factory.assert_called_once(); sleep.assert_not_called()

    def test_retry_after_parsing(self):
        self.assertEqual(c.retry_delay("999", 0), 60)
        self.assertEqual(c.retry_delay("-4", 0), 0)
        self.assertEqual(c.retry_delay("invalid", 2), 4)
        self.assertEqual(c.retry_delay(None, 0), 1)
        future = format_datetime(datetime.now(timezone.utc) + timedelta(seconds=30))
        self.assertTrue(0 <= c.retry_delay(future, 0) <= 30)

    def test_unbounded_configuration_rejected(self):
        for kwargs in ({"attempts": 20}, {"attempts": 0}, {"attempts": 1.5}, {"connect_timeout": 0}, {"response_timeout": 1000}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(c.MonitoringError): c.fetch_live(**kwargs)


if __name__ == "__main__":
    unittest.main()
