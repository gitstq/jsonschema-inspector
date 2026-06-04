"""
Unit tests for SchemaValidator
"""

import json
import unittest
from jsonschema_inspector.validator import SchemaValidator, ValidationError


class TestSchemaValidator(unittest.TestCase):
    """Test cases for SchemaValidator"""

    def test_type_validation(self):
        """Test type validation"""
        schema = {"type": "string"}
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate("hello"))
        self.assertFalse(validator.validate(123))
        self.assertFalse(validator.validate(None))

    def test_number_constraints(self):
        """Test number constraint validation"""
        schema = {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "multipleOf": 5
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate(50))
        self.assertFalse(validator.validate(-1))
        self.assertFalse(validator.validate(101))
        self.assertFalse(validator.validate(7))

    def test_string_constraints(self):
        """Test string constraint validation"""
        schema = {
            "type": "string",
            "minLength": 3,
            "maxLength": 10,
            "pattern": "^[a-z]+$"
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate("hello"))
        self.assertFalse(validator.validate("hi"))
        self.assertFalse(validator.validate("hello world"))
        self.assertFalse(validator.validate("Hello123"))

    def test_array_validation(self):
        """Test array validation"""
        schema = {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 5,
            "uniqueItems": True
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate([1, 2, 3]))
        self.assertFalse(validator.validate([1]))
        self.assertFalse(validator.validate([1, 2, 3, 4, 5, 6]))
        self.assertFalse(validator.validate([1, 1, 2]))
        self.assertFalse(validator.validate([1, "two", 3]))

    def test_object_validation(self):
        """Test object validation"""
        schema = {
            "type": "object",
            "required": ["name", "age"],
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0}
            },
            "additionalProperties": False
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate({"name": "John", "age": 30}))
        self.assertFalse(validator.validate({"name": "John"}))
        self.assertFalse(validator.validate({"name": "John", "age": -1}))
        self.assertFalse(validator.validate({"name": "John", "age": 30, "extra": "value"}))

    def test_enum_validation(self):
        """Test enum validation"""
        schema = {"enum": ["red", "green", "blue"]}
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate("red"))
        self.assertFalse(validator.validate("yellow"))

    def test_const_validation(self):
        """Test const validation"""
        schema = {"const": 42}
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate(42))
        self.assertFalse(validator.validate(43))

    def test_allof_validation(self):
        """Test allOf validation"""
        schema = {
            "allOf": [
                {"type": "integer"},
                {"minimum": 0},
                {"maximum": 100}
            ]
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate(50))
        self.assertFalse(validator.validate(150))
        self.assertFalse(validator.validate("not a number"))

    def test_anyof_validation(self):
        """Test anyOf validation"""
        schema = {
            "anyOf": [
                {"type": "string"},
                {"type": "integer"}
            ]
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate("hello"))
        self.assertTrue(validator.validate(42))
        self.assertFalse(validator.validate(True))

    def test_oneof_validation(self):
        """Test oneOf validation"""
        schema = {
            "oneOf": [
                {"type": "integer", "minimum": 0},
                {"type": "integer", "maximum": 0}
            ]
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate(5))
        self.assertTrue(validator.validate(-5))
        self.assertFalse(validator.validate(0))

    def test_not_validation(self):
        """Test not validation"""
        schema = {"not": {"type": "string"}}
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate(42))
        self.assertFalse(validator.validate("hello"))

    def test_if_then_else(self):
        """Test if/then/else validation"""
        schema = {
            "if": {"type": "integer"},
            "then": {"minimum": 0},
            "else": {"type": "string"}
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate(5))
        self.assertFalse(validator.validate(-5))
        self.assertTrue(validator.validate("hello"))
        self.assertFalse(validator.validate(True))

    def test_format_validation(self):
        """Test format validation (warnings only)"""
        schema = {"type": "string", "format": "email"}
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate("test@example.com"))
        validator.validate("not-an-email")
        self.assertEqual(len(validator.get_warnings()), 1)

    def test_ref_validation(self):
        """Test $ref validation"""
        schema = {
            "definitions": {
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"}
                    }
                }
            },
            "type": "object",
            "properties": {
                "home": {"$ref": "#/definitions/address"}
            }
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate({
            "home": {"street": "123 Main St", "city": "NYC"}
        }))

    def test_validation_error(self):
        """Test ValidationError object"""
        error = ValidationError("path", "message", "schema_path", "constraint")
        self.assertEqual(error.path, "path")
        self.assertEqual(error.message, "message")
        self.assertEqual(error.to_dict()["path"], "path")

    def test_draft_detection(self):
        """Test automatic draft detection"""
        schema_v7 = {"$schema": "http://json-schema.org/draft-07/schema#"}
        schema_2020 = {"$schema": "https://json-schema.org/draft/2020-12/schema"}

        validator_v7 = SchemaValidator(schema_v7)
        validator_2020 = SchemaValidator(schema_2020)

        self.assertEqual(validator_v7.draft, SchemaValidator.DRAFT_7)
        self.assertEqual(validator_2020.draft, SchemaValidator.DRAFT_2020_12)

    def test_boolean_schema(self):
        """Test boolean schema (true/false)"""
        validator_true = SchemaValidator(True)
        validator_false = SchemaValidator(False)

        self.assertTrue(validator_true.validate("anything"))
        self.assertFalse(validator_false.validate("anything"))


class TestComplexSchemas(unittest.TestCase):
    """Test complex real-world schemas"""

    def test_nested_object(self):
        """Test deeply nested object"""
        schema = {
            "type": "object",
            "properties": {
                "level1": {
                    "type": "object",
                    "properties": {
                        "level2": {
                            "type": "object",
                            "properties": {
                                "value": {"type": "string"}
                            },
                            "required": ["value"]
                        }
                    }
                }
            }
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate({
            "level1": {"level2": {"value": "deep"}}
        }))

    def test_array_of_objects(self):
        """Test array containing objects"""
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                },
                "required": ["id", "name"]
            }
        }
        validator = SchemaValidator(schema)

        self.assertTrue(validator.validate([
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]))
        self.assertFalse(validator.validate([
            {"id": 1}
        ]))


if __name__ == "__main__":
    unittest.main()
