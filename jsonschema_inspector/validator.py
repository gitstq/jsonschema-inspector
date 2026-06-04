"""
JSON Schema Validator Engine
Supports Draft 7, 2019-09, and 2020-12
"""

import json
import re
import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse


class ValidationError:
    """Represents a single validation error"""
    def __init__(self, path: str, message: str, schema_path: str = "", 
                 constraint: str = "", severity: str = "error"):
        self.path = path
        self.message = message
        self.schema_path = schema_path
        self.constraint = constraint
        self.severity = severity

    def __repr__(self):
        return f"ValidationError(path='{self.path}', message='{self.message}')"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "message": self.message,
            "schema_path": self.schema_path,
            "constraint": self.constraint,
            "severity": self.severity,
        }


class SchemaValidator:
    """
    Zero-dependency JSON Schema validator supporting Draft 7/2019-09/2020-12
    """

    DRAFT_7 = "http://json-schema.org/draft-07/schema#"
    DRAFT_2019_09 = "https://json-schema.org/draft/2019-09/schema"
    DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"

    def __init__(self, schema: Union[Dict, str, bool], draft: Optional[str] = None):
        """
        Initialize validator with schema
        
        Args:
            schema: JSON Schema dict, file path, or boolean
            draft: Schema draft version (auto-detected if None)
        """
        if isinstance(schema, str):
            with open(schema, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
            self.schema_path = schema
        else:
            self.schema = schema
            self.schema_path = ""

        self.draft = draft or self._detect_draft()
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
        self._ref_cache: Dict[str, Dict] = {}

    def _detect_draft(self) -> str:
        """Auto-detect schema draft version"""
        if isinstance(self.schema, bool):
            return self.DRAFT_7
        schema_id = self.schema.get("$schema", "")
        if "2020-12" in schema_id:
            return self.DRAFT_2020_12
        elif "2019-09" in schema_id:
            return self.DRAFT_2019_09
        return self.DRAFT_7

    def validate(self, data: Any, schema: Optional[Dict] = None, 
                 path: str = "", schema_path: str = "") -> bool:
        """
        Validate data against schema
        
        Args:
            data: Data to validate
            schema: Schema to validate against (uses instance schema if None)
            path: Current data path for error reporting
            schema_path: Current schema path for error reporting
            
        Returns:
            True if valid, False otherwise
        """
        self.errors = []
        self.warnings = []
        schema = schema or self.schema
        self._validate_value(data, schema, path, schema_path)
        return len(self.errors) == 0

    def _validate_value(self, data: Any, schema: Union[Dict, bool], 
                        path: str, schema_path: str):
        """Validate a value against schema"""
        if schema is True:
            return
        if schema is False:
            self.errors.append(ValidationError(
                path, "Value not allowed", schema_path, "false"
            ))
            return

        if not isinstance(schema, dict):
            return

        # Handle $ref
        if "$ref" in schema:
            ref_schema = self._resolve_ref(schema["$ref"])
            if ref_schema:
                self._validate_value(data, ref_schema, path, schema_path)
            else:
                self.errors.append(ValidationError(
                    path, f"Cannot resolve reference: {schema['$ref']}",
                    schema_path, "$ref"
                ))
            return

        # Handle type validation
        if "type" in schema:
            self._validate_type(data, schema["type"], path, schema_path)

        # Handle enum
        if "enum" in schema:
            self._validate_enum(data, schema["enum"], path, schema_path)

        # Handle const
        if "const" in schema:
            if data != schema["const"]:
                self.errors.append(ValidationError(
                    path, f"Expected const value: {schema['const']}",
                    schema_path, "const"
                ))

        # Type-specific validations
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            self._validate_number(data, schema, path, schema_path)
        elif isinstance(data, str):
            self._validate_string(data, schema, path, schema_path)
        elif isinstance(data, list):
            self._validate_array(data, schema, path, schema_path)
        elif isinstance(data, dict):
            self._validate_object(data, schema, path, schema_path)

        # Handle allOf
        if "allOf" in schema:
            for i, subschema in enumerate(schema["allOf"]):
                self._validate_value(data, subschema, path, 
                    f"{schema_path}/allOf/{i}")

        # Handle anyOf
        if "anyOf" in schema:
            any_valid = False
            sub_errors = []
            for i, subschema in enumerate(schema["anyOf"]):
                validator = SchemaValidator(subschema, self.draft)
                if validator.validate(data, subschema, path):
                    any_valid = True
                    break
                sub_errors.extend(validator.errors)
            if not any_valid:
                self.errors.append(ValidationError(
                    path, "Data does not match any of the anyOf schemas",
                    schema_path, "anyOf"
                ))

        # Handle oneOf
        if "oneOf" in schema:
            valid_count = 0
            for i, subschema in enumerate(schema["oneOf"]):
                validator = SchemaValidator(subschema, self.draft)
                if validator.validate(data, subschema, path):
                    valid_count += 1
            if valid_count != 1:
                self.errors.append(ValidationError(
                    path, f"Data matches {valid_count} oneOf schemas, expected exactly 1",
                    schema_path, "oneOf"
                ))

        # Handle not
        if "not" in schema:
            validator = SchemaValidator(schema["not"], self.draft)
            if validator.validate(data, schema["not"], path):
                self.errors.append(ValidationError(
                    path, "Data should not match the 'not' schema",
                    schema_path, "not"
                ))

        # Handle if/then/else
        if "if" in schema:
            validator = SchemaValidator(schema["if"], self.draft)
            if validator.validate(data, schema["if"], path):
                if "then" in schema:
                    self._validate_value(data, schema["then"], path,
                        f"{schema_path}/then")
            else:
                if "else" in schema:
                    self._validate_value(data, schema["else"], path,
                        f"{schema_path}/else")

    def _validate_type(self, data: Any, expected_type: Union[str, List], 
                       path: str, schema_path: str):
        """Validate data type"""
        if isinstance(expected_type, list):
            valid = any(self._check_type(data, t) for t in expected_type)
            if not valid:
                self.errors.append(ValidationError(
                    path, f"Expected one of types: {expected_type}, got: {type(data).__name__}",
                    schema_path, "type"
                ))
        else:
            if not self._check_type(data, expected_type):
                self.errors.append(ValidationError(
                    path, f"Expected type: {expected_type}, got: {type(data).__name__}",
                    schema_path, "type"
                ))

    def _check_type(self, data: Any, expected: str) -> bool:
        """Check if data matches expected type"""
        type_map = {
            "null": lambda x: x is None,
            "boolean": lambda x: isinstance(x, bool),
            "object": lambda x: isinstance(x, dict),
            "array": lambda x: isinstance(x, list),
            "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
            "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
            "string": lambda x: isinstance(x, str),
        }
        checker = type_map.get(expected)
        return checker(data) if checker else False

    def _validate_number(self, data: Union[int, float], schema: Dict, 
                         path: str, schema_path: str):
        """Validate number constraints"""
        if "minimum" in schema and data < schema["minimum"]:
            self.errors.append(ValidationError(
                path, f"Value {data} is less than minimum {schema['minimum']}",
                schema_path, "minimum"
            ))
        if "maximum" in schema and data > schema["maximum"]:
            self.errors.append(ValidationError(
                path, f"Value {data} is greater than maximum {schema['maximum']}",
                schema_path, "maximum"
            ))
        if "exclusiveMinimum" in schema:
            emin = schema["exclusiveMinimum"]
            if data <= emin:
                self.errors.append(ValidationError(
                    path, f"Value {data} is not > exclusiveMinimum {emin}",
                    schema_path, "exclusiveMinimum"
                ))
        if "exclusiveMaximum" in schema:
            emax = schema["exclusiveMaximum"]
            if data >= emax:
                self.errors.append(ValidationError(
                    path, f"Value {data} is not < exclusiveMaximum {emax}",
                    schema_path, "exclusiveMaximum"
                ))
        if "multipleOf" in schema:
            if schema["multipleOf"] != 0 and (data / schema["multipleOf"]) % 1 != 0:
                self.errors.append(ValidationError(
                    path, f"Value {data} is not a multiple of {schema['multipleOf']}",
                    schema_path, "multipleOf"
                ))

    def _validate_string(self, data: str, schema: Dict, 
                         path: str, schema_path: str):
        """Validate string constraints"""
        if "minLength" in schema and len(data) < schema["minLength"]:
            self.errors.append(ValidationError(
                path, f"String length {len(data)} < minLength {schema['minLength']}",
                schema_path, "minLength"
            ))
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            self.errors.append(ValidationError(
                path, f"String length {len(data)} > maxLength {schema['maxLength']}",
                schema_path, "maxLength"
            ))
        if "pattern" in schema:
            try:
                if not re.match(schema["pattern"], data):
                    self.errors.append(ValidationError(
                        path, f"String does not match pattern: {schema['pattern']}",
                        schema_path, "pattern"
                    ))
            except re.error:
                self.warnings.append(ValidationError(
                    path, f"Invalid regex pattern: {schema['pattern']}",
                    schema_path, "pattern", "warning"
                ))
        if "format" in schema:
            self._validate_format(data, schema["format"], path, schema_path)

    def _validate_format(self, data: str, fmt: str, path: str, schema_path: str):
        """Validate string format"""
        format_patterns = {
            "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "uri": r'^https?://[^\s/$.?#].[^\s]*$',
            "date": r'^\d{4}-\d{2}-\d{2}$',
            "date-time": r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?$',
            "time": r'^\d{2}:\d{2}:\d{2}(\.\d+)?$',
            "ipv4": r'^(\d{1,3}\.){3}\d{1,3}$',
            "ipv6": r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$',
            "uuid": r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',
        }
        pattern = format_patterns.get(fmt)
        if pattern and not re.match(pattern, data):
            self.warnings.append(ValidationError(
                path, f"String does not match format '{fmt}': {data}",
                schema_path, "format", "warning"
            ))

    def _validate_array(self, data: List, schema: Dict, 
                        path: str, schema_path: str):
        """Validate array constraints"""
        if "minItems" in schema and len(data) < schema["minItems"]:
            self.errors.append(ValidationError(
                path, f"Array length {len(data)} < minItems {schema['minItems']}",
                schema_path, "minItems"
            ))
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            self.errors.append(ValidationError(
                path, f"Array length {len(data)} > maxItems {schema['maxItems']}",
                schema_path, "maxItems"
            ))
        if "uniqueItems" in schema and schema["uniqueItems"]:
            seen = []
            for i, item in enumerate(data):
                for j, prev in enumerate(seen):
                    if self._deep_equal(item, prev):
                        self.errors.append(ValidationError(
                            f"{path}[{i}]", 
                            f"Duplicate item found at index {j}",
                            schema_path, "uniqueItems"
                        ))
                        break
                seen.append(item)

        if "items" in schema:
            items_schema = schema["items"]
            for i, item in enumerate(data):
                self._validate_value(item, items_schema, 
                    f"{path}[{i}]", f"{schema_path}/items")

        if "prefixItems" in schema:
            for i, item_schema in enumerate(schema["prefixItems"]):
                if i < len(data):
                    self._validate_value(data[i], item_schema,
                        f"{path}[{i}]", f"{schema_path}/prefixItems/{i}")

        if "contains" in schema:
            contains_count = 0
            for i, item in enumerate(data):
                validator = SchemaValidator(schema["contains"], self.draft)
                if validator.validate(item, schema["contains"], f"{path}[{i}]"):
                    contains_count += 1
            if contains_count == 0:
                self.errors.append(ValidationError(
                    path, "Array does not contain any matching items",
                    schema_path, "contains"
                ))
            if "minContains" in schema and contains_count < schema["minContains"]:
                self.errors.append(ValidationError(
                    path, f"Array contains {contains_count} matching items, minimum {schema['minContains']}",
                    schema_path, "minContains"
                ))
            if "maxContains" in schema and contains_count > schema["maxContains"]:
                self.errors.append(ValidationError(
                    path, f"Array contains {contains_count} matching items, maximum {schema['maxContains']}",
                    schema_path, "maxContains"
                ))

    def _validate_object(self, data: Dict, schema: Dict, 
                         path: str, schema_path: str):
        """Validate object constraints"""
        if "minProperties" in schema and len(data) < schema["minProperties"]:
            self.errors.append(ValidationError(
                path, f"Object has {len(data)} properties, minimum {schema['minProperties']}",
                schema_path, "minProperties"
            ))
        if "maxProperties" in schema and len(data) > schema["maxProperties"]:
            self.errors.append(ValidationError(
                path, f"Object has {len(data)} properties, maximum {schema['maxProperties']}",
                schema_path, "maxProperties"
            ))

        properties = schema.get("properties", {})
        pattern_properties = schema.get("patternProperties", {})
        required = schema.get("required", [])
        additional_properties = schema.get("additionalProperties", True)

        # Validate required properties
        for prop in required:
            if prop not in data:
                self.errors.append(ValidationError(
                    f"{path}.{prop}" if path else prop,
                    f"Required property '{prop}' is missing",
                    schema_path, "required"
                ))

        # Validate properties
        for prop, value in data.items():
            prop_path = f"{path}.{prop}" if path else prop
            if prop in properties:
                self._validate_value(value, properties[prop], prop_path,
                    f"{schema_path}/properties/{prop}")
            else:
                # Check patternProperties
                matched = False
                for pattern, pat_schema in pattern_properties.items():
                    if re.match(pattern, prop):
                        matched = True
                        self._validate_value(value, pat_schema, prop_path,
                            f"{schema_path}/patternProperties/{pattern}")
                if not matched:
                    if additional_properties is False:
                        self.errors.append(ValidationError(
                            prop_path, f"Additional property '{prop}' is not allowed",
                            schema_path, "additionalProperties"
                        ))
                    elif isinstance(additional_properties, dict):
                        self._validate_value(value, additional_properties, prop_path,
                            f"{schema_path}/additionalProperties")

        # Validate propertyNames
        if "propertyNames" in schema:
            for prop in data.keys():
                self._validate_value(prop, schema["propertyNames"],
                    f"{path}[key]", f"{schema_path}/propertyNames")

        # Validate dependencies
        if "dependencies" in schema:
            for prop, dep in schema["dependencies"].items():
                if prop in data:
                    if isinstance(dep, list):
                        for required_prop in dep:
                            if required_prop not in data:
                                self.errors.append(ValidationError(
                                    path,
                                    f"Dependency: property '{prop}' requires '{required_prop}'",
                                    schema_path, "dependencies"
                                ))
                    elif isinstance(dep, dict):
                        self._validate_value(data, dep, path,
                            f"{schema_path}/dependencies/{prop}")

        # Validate dependentRequired (Draft 2019-09+)
        if "dependentRequired" in schema:
            for prop, deps in schema["dependentRequired"].items():
                if prop in data:
                    for dep in deps:
                        if dep not in data:
                            self.errors.append(ValidationError(
                                path,
                                f"dependentRequired: '{prop}' requires '{dep}'",
                                schema_path, "dependentRequired"
                            ))

        # Validate dependentSchemas (Draft 2019-09+)
        if "dependentSchemas" in schema:
            for prop, dep_schema in schema["dependentSchemas"].items():
                if prop in data:
                    self._validate_value(data, dep_schema, path,
                        f"{schema_path}/dependentSchemas/{prop}")

    def _validate_enum(self, data: Any, enum_values: List, 
                       path: str, schema_path: str):
        """Validate enum values"""
        if not any(self._deep_equal(data, ev) for ev in enum_values):
            self.errors.append(ValidationError(
                path, f"Value must be one of: {enum_values}",
                schema_path, "enum"
            ))

    def _deep_equal(self, a: Any, b: Any) -> bool:
        """Deep equality check"""
        if type(a) != type(b):
            return False
        if isinstance(a, dict):
            if set(a.keys()) != set(b.keys()):
                return False
            return all(self._deep_equal(a[k], b[k]) for k in a)
        if isinstance(a, list):
            if len(a) != len(b):
                return False
            return all(self._deep_equal(x, y) for x, y in zip(a, b))
        return a == b

    def _resolve_ref(self, ref: str) -> Optional[Dict]:
        """Resolve JSON Schema $ref"""
        if ref in self._ref_cache:
            return self._ref_cache[ref]

        if ref.startswith("#"):
            # Local reference
            parts = ref[1:].split("/")
            current = self.schema
            for part in parts:
                if not part:
                    continue
                part = part.replace("~1", "/").replace("~0", "~")
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
            self._ref_cache[ref] = current
            return current
        else:
            # External reference - try to load from file
            try:
                parsed = urlparse(ref)
                if parsed.scheme in ('http', 'https'):
                    # For external URLs, we can't fetch without requests
                    return None
                # Local file reference
                base_path = os.path.dirname(self.schema_path) if self.schema_path else "."
                file_path = os.path.join(base_path, ref.split("#")[0])
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        doc = json.load(f)
                    if "#" in ref:
                        fragment = ref.split("#")[1]
                        parts = fragment.split("/")
                        current = doc
                        for part in parts:
                            if not part:
                                continue
                            part = part.replace("~1", "/").replace("~0", "~")
                            if isinstance(current, dict) and part in current:
                                current = current[part]
                            else:
                                return None
                        self._ref_cache[ref] = current
                        return current
                    self._ref_cache[ref] = doc
                    return doc
            except Exception:
                pass
            return None

    def get_errors(self) -> List[ValidationError]:
        """Get validation errors"""
        return self.errors

    def get_warnings(self) -> List[ValidationError]:
        """Get validation warnings"""
        return self.warnings

    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        return {
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "draft": self.draft,
        }
