"""
Unit tests for SchemaVisualizer
"""

import unittest
from jsonschema_inspector.visualizer import SchemaVisualizer


class TestSchemaVisualizer(unittest.TestCase):
    """Test cases for SchemaVisualizer"""

    def setUp(self):
        self.visualizer = SchemaVisualizer(use_color=False)

    def test_visualize_simple(self):
        """Test visualizing simple schema"""
        schema = {"type": "string"}
        output = self.visualizer.visualize(schema)
        self.assertIn("JSON Schema", output)
        self.assertIn("string", output)

    def test_visualize_object(self):
        """Test visualizing object schema"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        output = self.visualizer.visualize(schema)
        self.assertIn("object", output)
        self.assertIn("name", output)
        self.assertIn("age", output)

    def test_visualize_array(self):
        """Test visualizing array schema"""
        schema = {
            "type": "array",
            "items": {"type": "integer"}
        }
        output = self.visualizer.visualize(schema)
        self.assertIn("array", output)
        self.assertIn("Items", output)

    def test_markdown_doc(self):
        """Test markdown documentation generation"""
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Unique ID"}
            }
        }
        output = self.visualizer.generate_markdown_doc(schema, "Test Schema")
        self.assertIn("# Test Schema", output)
        self.assertIn("## Properties", output)
        self.assertIn("id", output)

    def test_color_output(self):
        """Test colored output"""
        viz = SchemaVisualizer(use_color=True)
        schema = {"type": "string"}
        output = viz.visualize(schema)
        # Should contain ANSI escape codes
        self.assertIn("\033[", output)

    def test_no_color_output(self):
        """Test no-color output"""
        schema = {"type": "string"}
        output = self.visualizer.visualize(schema)
        # Should not contain ANSI escape codes
        self.assertNotIn("\033[", output)


if __name__ == "__main__":
    unittest.main()
