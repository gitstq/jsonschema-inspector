"""
Unit tests for MockDataGenerator
"""

import unittest
from jsonschema_inspector.mock_generator import MockDataGenerator


class TestMockDataGenerator(unittest.TestCase):
    """Test cases for MockDataGenerator"""

    def setUp(self):
        self.generator = MockDataGenerator(seed=42)

    def test_string_generation(self):
        """Test string mock generation"""
        schema = {"type": "string", "minLength": 5, "maxLength": 10}
        result = self.generator.generate(schema)
        self.assertIsInstance(result, str)
        self.assertGreaterEqual(len(result), 5)
        self.assertLessEqual(len(result), 10)

    def test_integer_generation(self):
        """Test integer mock generation"""
        schema = {"type": "integer", "minimum": 0, "maximum": 100}
        result = self.generator.generate(schema)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 100)

    def test_number_generation(self):
        """Test number mock generation"""
        schema = {"type": "number", "minimum": 0, "maximum": 1}
        result = self.generator.generate(schema)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 1)

    def test_boolean_generation(self):
        """Test boolean mock generation"""
        schema = {"type": "boolean"}
        result = self.generator.generate(schema)
        self.assertIsInstance(result, bool)

    def test_null_generation(self):
        """Test null mock generation"""
        schema = {"type": "null"}
        result = self.generator.generate(schema)
        self.assertIsNone(result)

    def test_object_generation(self):
        """Test object mock generation"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        result = self.generator.generate(schema)
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertIsInstance(result["name"], str)

    def test_array_generation(self):
        """Test array mock generation"""
        schema = {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 5
        }
        result = self.generator.generate(schema)
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 2)
        self.assertLessEqual(len(result), 5)
        for item in result:
            self.assertIsInstance(item, int)

    def test_enum_generation(self):
        """Test enum mock generation"""
        schema = {"enum": ["red", "green", "blue"]}
        result = self.generator.generate(schema)
        self.assertIn(result, ["red", "green", "blue"])

    def test_const_generation(self):
        """Test const mock generation"""
        schema = {"const": "fixed_value"}
        result = self.generator.generate(schema)
        self.assertEqual(result, "fixed_value")

    def test_format_generation(self):
        """Test format-based mock generation"""
        formats = {
            "email": {"type": "string", "format": "email"},
            "date": {"type": "string", "format": "date"},
            "uuid": {"type": "string", "format": "uuid"},
            "ipv4": {"type": "string", "format": "ipv4"},
        }
        for fmt_name, schema in formats.items():
            result = self.generator.generate(schema)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

    def test_multiple_generation(self):
        """Test generating multiple samples"""
        schema = {"type": "integer"}
        results = self.generator.generate(schema, count=5)
        self.assertEqual(len(results), 5)
        for r in results:
            self.assertIsInstance(r, int)

    def test_reproducible_seed(self):
        """Test reproducible output with seed"""
        gen1 = MockDataGenerator(seed=42)
        gen2 = MockDataGenerator(seed=42)
        schema = {"type": "string", "minLength": 10, "maxLength": 10}

        result1 = gen1.generate(schema)
        result2 = gen2.generate(schema)
        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main()
