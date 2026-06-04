"""
Mock Data Generator - Generate sample data from JSON Schema
"""

import json
import random
import string
from typing import Any, Dict, List, Optional, Union


class MockDataGenerator:
    """
    Generate realistic mock data from JSON Schema definitions
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize mock data generator
        
        Args:
            seed: Random seed for reproducible output
        """
        self._seed = seed
        self._ref_cache: Dict[str, Any] = {}
        self._schema: Dict = {}
        if seed is not None:
            random.seed(seed)

    def generate(self, schema: Union[Dict, str], count: int = 1) -> Union[Dict, List[Dict]]:
        """
        Generate mock data from schema
        
        Args:
            schema: JSON Schema dict or file path
            count: Number of samples to generate
            
        Returns:
            Single sample if count=1, else list of samples
        """
        if isinstance(schema, str):
            with open(schema, 'r', encoding='utf-8') as f:
                self._schema = json.load(f)
        else:
            self._schema = schema

        # Reset random seed for reproducibility
        if self._seed is not None:
            random.seed(self._seed)

        if count == 1:
            return self._generate_value(self._schema)
        return [self._generate_value(self._schema) for _ in range(count)]

    def _generate_value(self, schema: Any) -> Any:
        """Generate a value matching the schema"""
        if schema is True:
            return self._random_primitive()
        if schema is False:
            return None
        if not isinstance(schema, dict):
            return None

        # Handle $ref
        if "$ref" in schema:
            ref_schema = self._resolve_ref(schema["$ref"])
            if ref_schema:
                return self._generate_value(ref_schema)
            return None

        # Handle const
        if "const" in schema:
            return schema["const"]

        # Handle enum
        if "enum" in schema:
            return random.choice(schema["enum"])

        # Handle type
        schema_type = schema.get("type", "any")
        if isinstance(schema_type, list):
            schema_type = random.choice(schema_type)

        type_generators = {
            "null": lambda s: None,
            "boolean": self._generate_boolean,
            "object": self._generate_object,
            "array": self._generate_array,
            "number": self._generate_number,
            "integer": self._generate_integer,
            "string": self._generate_string,
        }

        generator = type_generators.get(schema_type)
        if generator:
            return generator(schema)

        # Default: try to infer from other keywords
        if "properties" in schema or "additionalProperties" in schema:
            return self._generate_object(schema)
        if "items" in schema or "prefixItems" in schema:
            return self._generate_array(schema)

        return self._random_primitive()

    def _generate_boolean(self, schema: Dict) -> bool:
        """Generate a boolean value"""
        return random.choice([True, False])

    def _generate_object(self, schema: Dict) -> Dict:
        """Generate an object value"""
        result = {}
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        additional_props = schema.get("additionalProperties", True)

        # Generate required properties
        for prop_name, prop_schema in properties.items():
            if prop_name in required or random.random() > 0.3:
                result[prop_name] = self._generate_value(prop_schema)

        # Generate additional properties if allowed
        if additional_props is True and random.random() > 0.5:
            num_extra = random.randint(1, 3)
            for i in range(num_extra):
                key = f"extra_{i}"
                result[key] = self._random_primitive()
        elif isinstance(additional_props, dict):
            num_extra = random.randint(1, 2)
            for i in range(num_extra):
                key = f"extra_{i}"
                result[key] = self._generate_value(additional_props)

        # Respect minProperties/maxProperties
        min_props = schema.get("minProperties", 0)
        max_props = schema.get("maxProperties", float('inf'))

        while len(result) < min_props and properties:
            prop_name = random.choice(list(properties.keys()))
            if prop_name not in result:
                result[prop_name] = self._generate_value(properties[prop_name])

        if len(result) > max_props:
            keys = list(result.keys())
            random.shuffle(keys)
            for key in keys[int(max_props):]:
                del result[key]

        return result

    def _generate_array(self, schema: Dict) -> List:
        """Generate an array value"""
        result = []

        # Handle prefixItems (tuple)
        if "prefixItems" in schema:
            for item_schema in schema["prefixItems"]:
                result.append(self._generate_value(item_schema))

        # Handle items
        if "items" in schema:
            min_items = schema.get("minItems", 0)
            max_items = schema.get("maxItems", min(min_items + 5, 10))
            num_items = random.randint(min_items, max_items)

            # Fill remaining slots
            while len(result) < num_items:
                result.append(self._generate_value(schema["items"]))

        # Handle contains
        if "contains" in schema:
            contains_count = schema.get("minContains", 1)
            for _ in range(contains_count):
                result.append(self._generate_value(schema["contains"]))

        # Respect uniqueItems
        if schema.get("uniqueItems", False):
            seen = []
            unique_result = []
            for item in result:
                item_str = json.dumps(item, sort_keys=True)
                if item_str not in seen:
                    seen.append(item_str)
                    unique_result.append(item)
            result = unique_result

        return result

    def _generate_number(self, schema: Dict) -> float:
        """Generate a number value"""
        minimum = schema.get("minimum", -1000)
        maximum = schema.get("maximum", 1000)
        exclusive_min = schema.get("exclusiveMinimum")
        exclusive_max = schema.get("exclusiveMaximum")
        multiple_of = schema.get("multipleOf")

        if exclusive_min is not None:
            minimum = exclusive_min + 0.001
        if exclusive_max is not None:
            maximum = exclusive_max - 0.001

        if multiple_of:
            min_mult = int(minimum / multiple_of) + (1 if minimum % multiple_of != 0 else 0)
            max_mult = int(maximum / multiple_of)
            if min_mult <= max_mult:
                mult = random.randint(min_mult, max_mult)
                return mult * multiple_of

        return round(random.uniform(minimum, maximum), 2)

    def _generate_integer(self, schema: Dict) -> int:
        """Generate an integer value"""
        minimum = schema.get("minimum", -100)
        maximum = schema.get("maximum", 100)
        exclusive_min = schema.get("exclusiveMinimum")
        exclusive_max = schema.get("exclusiveMaximum")
        multiple_of = schema.get("multipleOf")

        if exclusive_min is not None:
            minimum = exclusive_min + 1
        if exclusive_max is not None:
            maximum = exclusive_max - 1

        if multiple_of:
            min_mult = int(minimum / multiple_of) + (1 if minimum % multiple_of != 0 else 0)
            max_mult = int(maximum / multiple_of)
            if min_mult <= max_mult:
                mult = random.randint(min_mult, max_mult)
                return mult * multiple_of

        return random.randint(int(minimum), int(maximum))

    def _generate_string(self, schema: Dict) -> str:
        """Generate a string value"""
        fmt = schema.get("format", "")
        pattern = schema.get("pattern", "")
        min_length = schema.get("minLength", 1)
        max_length = schema.get("maxLength", 50)

        # Handle format
        format_generators = {
            "email": lambda: f"user{random.randint(1,9999)}@example.com",
            "date": lambda: f"{random.randint(2020,2025)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "date-time": lambda: f"{random.randint(2020,2025)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}Z",
            "time": lambda: f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}",
            "uri": lambda: f"https://example.com/path{random.randint(1,999)}",
            "uuid": lambda: f"{self._random_hex(8)}-{self._random_hex(4)}-{self._random_hex(4)}-{self._random_hex(4)}-{self._random_hex(12)}",
            "ipv4": lambda: f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}",
            "ipv6": lambda: f"2001:0db8:85a3:{self._random_hex(4)}:{self._random_hex(4)}:{self._random_hex(4)}:{self._random_hex(4)}",
        }

        if fmt in format_generators:
            return format_generators[fmt]()

        # Generate random string
        length = random.randint(min_length, min(max_length, 50))
        chars = string.ascii_letters + string.digits + " _-"
        return ''.join(random.choice(chars) for _ in range(length))

    def _random_hex(self, length: int) -> str:
        """Generate random hex string"""
        return ''.join(random.choice(string.hexdigits.lower()) for _ in range(length))

    def _random_primitive(self) -> Any:
        """Generate a random primitive value"""
        return random.choice([
            random.randint(-100, 100),
            round(random.uniform(-100, 100), 2),
            ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 20))),
            random.choice([True, False]),
            None,
        ])

    def _resolve_ref(self, ref: str) -> Optional[Dict]:
        """Resolve JSON Schema $ref"""
        if ref in self._ref_cache:
            return self._ref_cache[ref]

        if ref.startswith("#"):
            parts = ref[1:].split("/")
            current = self._schema
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
        return None
