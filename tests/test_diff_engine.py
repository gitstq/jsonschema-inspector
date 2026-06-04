"""
Unit tests for SchemaDiffEngine
"""

import unittest
from jsonschema_inspector.diff_engine import SchemaDiffEngine, SchemaChange


class TestSchemaDiffEngine(unittest.TestCase):
    """Test cases for SchemaDiffEngine"""

    def setUp(self):
        self.engine = SchemaDiffEngine()

    def test_no_changes(self):
        """Test identical schemas"""
        schema = {"type": "string"}
        changes = self.engine.compare(schema, schema)
        self.assertEqual(len(changes), 0)

    def test_added_property(self):
        """Test detecting added property"""
        old = {"type": "object", "properties": {}}
        new = {"type": "object", "properties": {"name": {"type": "string"}}}
        changes = self.engine.compare(old, new)

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, "added")
        self.assertIn("name", changes[0].path)

    def test_removed_property(self):
        """Test detecting removed property"""
        old = {"type": "object", "properties": {"name": {"type": "string"}}}
        new = {"type": "object", "properties": {}}
        changes = self.engine.compare(old, new)

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, "removed")
        self.assertIn("name", changes[0].path)

    def test_modified_value(self):
        """Test detecting modified value"""
        old = {"type": "string", "minLength": 1}
        new = {"type": "string", "minLength": 5}
        changes = self.engine.compare(old, new)

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, "modified")
        self.assertEqual(changes[0].old_value, 1)
        self.assertEqual(changes[0].new_value, 5)

    def test_type_changed(self):
        """Test detecting type change"""
        old = {"type": "string"}
        new = ["string", "integer"]
        changes = self.engine.compare(old, new)

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].change_type, "type_changed")

    def test_nested_changes(self):
        """Test nested object changes"""
        old = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        }
        new = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    }
                }
            }
        }
        changes = self.engine.compare(old, new)

        added = [c for c in changes if c.change_type == "added"]
        self.assertEqual(len(added), 1)
        self.assertIn("age", added[0].path)

    def test_array_changes(self):
        """Test array changes"""
        old = {"type": "array", "items": [{"type": "string"}]}
        new = {"type": "array", "items": [{"type": "string"}, {"type": "integer"}]}
        changes = self.engine.compare(old, new)

        added = [c for c in changes if c.change_type == "added"]
        self.assertTrue(len(added) > 0)

    def test_summary(self):
        """Test summary generation"""
        old = {"type": "string", "minLength": 1}
        new = {"type": "integer", "minimum": 0}
        self.engine.compare(old, new)
        summary = self.engine.get_summary()

        self.assertIn("total_changes", summary)
        self.assertIn("breaking_changes", summary)
        self.assertGreater(summary["total_changes"], 0)

    def test_breaking_changes(self):
        """Test breaking change detection"""
        old = {"type": "object", "properties": {"name": {"type": "string"}}}
        new = {"type": "object", "properties": {}}
        self.engine.compare(old, new)
        summary = self.engine.get_summary()

        self.assertGreater(summary["breaking_changes"], 0)

    def test_text_report(self):
        """Test text report generation"""
        old = {"type": "string"}
        new = {"type": "integer"}
        self.engine.compare(old, new)
        report = self.engine.generate_report("text")

        self.assertIn("Schema Diff Report", report)
        # Check for ANSI colored modified indicator or summary
        self.assertTrue("Modified:" in report or "\x1b[33m" in report)

    def test_json_report(self):
        """Test JSON report generation"""
        old = {"type": "string"}
        new = {"type": "integer"}
        self.engine.compare(old, new)
        report = self.engine.generate_report("json")

        import json
        data = json.loads(report)
        self.assertIn("summary", data)
        self.assertIn("changes", data)

    def test_markdown_report(self):
        """Test Markdown report generation"""
        old = {"type": "string"}
        new = {"type": "integer"}
        self.engine.compare(old, new)
        report = self.engine.generate_report("markdown")

        self.assertIn("# Schema Diff Report", report)
        self.assertIn("## Summary", report)


if __name__ == "__main__":
    unittest.main()
