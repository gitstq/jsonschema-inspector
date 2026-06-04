"""
JSON Schema Visualizer - Terminal-based schema visualization
"""

import json
from typing import Any, Dict, List, Optional, Union


class SchemaVisualizer:
    """
    Terminal-based JSON Schema visualizer with tree-like output
    """

    TYPE_COLORS = {
        "object": "\033[36m",      # Cyan
        "array": "\033[35m",       # Magenta
        "string": "\033[32m",      # Green
        "number": "\033[33m",      # Yellow
        "integer": "\033[33m",     # Yellow
        "boolean": "\033[31m",     # Red
        "null": "\033[90m",        # Gray
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    def __init__(self, use_color: bool = True):
        self.use_color = use_color

    def _color(self, text: str, color: str) -> str:
        """Apply color to text"""
        if self.use_color:
            return f"{color}{text}{self.RESET}"
        return text

    def visualize(self, schema: Union[Dict, str], title: str = "JSON Schema") -> str:
        """
        Generate visual representation of schema
        
        Args:
            schema: JSON Schema dict or file path
            title: Title for the visualization
            
        Returns:
            Formatted string representation
        """
        if isinstance(schema, str):
            with open(schema, 'r', encoding='utf-8') as f:
                schema = json.load(f)

        lines = []
        lines.append(self._color(f"╔{'═' * 58}╗", self.BOLD))
        lines.append(self._color(f"║{title:^58}║", self.BOLD))
        lines.append(self._color(f"╠{'═' * 58}╣", self.BOLD))

        draft = schema.get("$schema", "Unknown draft")
        lines.append(f"║  {self._color('Draft:', self.DIM):<12} {draft:<44}║")

        schema_id = schema.get("$id", schema.get("id", "N/A"))
        lines.append(f"║  {self._color('ID:', self.DIM):<12} {schema_id:<44}║")
        lines.append(self._color(f"╠{'═' * 58}╣", self.BOLD))

        # Schema structure
        lines.extend(self._render_schema(schema, 0))

        lines.append(self._color(f"╚{'═' * 58}╝", self.BOLD))
        return "\n".join(lines)

    def _render_schema(self, schema: Any, depth: int, 
                       is_required: bool = False) -> List[str]:
        """Recursively render schema structure"""
        lines = []
        indent = "  " * (depth + 1)
        prefix = "║" + indent

        if isinstance(schema, bool):
            status = "✓ Any" if schema else "✗ None"
            lines.append(f"{prefix}{status:<{56 - len(indent)}}║")
            return lines

        if not isinstance(schema, dict):
            return lines

        # Handle $ref
        if "$ref" in schema:
            ref = schema["$ref"]
            lines.append(f"{prefix}{self._color('→ $ref:', self.ITALIC)} {ref:<{49 - len(indent)}}║")
            return lines

        # Type info
        schema_type = schema.get("type", "any")
        if isinstance(schema_type, list):
            type_str = " | ".join(schema_type)
        else:
            type_str = schema_type

        type_color = self.TYPE_COLORS.get(type_str, "")
        type_display = self._color(type_str, type_color) if type_color else type_str

        req_marker = " *" if is_required else ""
        lines.append(f"{prefix}[{type_display}]{req_marker}")

        # Title and description
        if "title" in schema:
            title = schema["title"][:40] + "..." if len(schema["title"]) > 40 else schema["title"]
            lines.append(f"{prefix}  {self._color('Title:', self.DIM)} {title}")
        if "description" in schema:
            desc = schema["description"][:50] + "..." if len(schema["description"]) > 50 else schema["description"]
            lines.append(f"{prefix}  {self._color('Desc:', self.DIM)} {desc}")

        # Constraints summary
        constraints = []
        for key in ["minLength", "maxLength", "minimum", "maximum", "minItems", 
                    "maxItems", "minProperties", "maxProperties", "pattern", "format"]:
            if key in schema:
                constraints.append(f"{key}={schema[key]}")
        if constraints:
            constr_str = ", ".join(constraints)
            if len(constr_str) > 50:
                constr_str = constr_str[:47] + "..."
            lines.append(f"{prefix}  {self._color('Constraints:', self.DIM)} {constr_str}")

        # Enum
        if "enum" in schema:
            enum_vals = json.dumps(schema["enum"])[:50]
            lines.append(f"{prefix}  {self._color('Enum:', self.DIM)} {enum_vals}")

        # Const
        if "const" in schema:
            lines.append(f"{prefix}  {self._color('Const:', self.DIM)} {schema['const']}")

        # Default
        if "default" in schema:
            default = json.dumps(schema["default"])[:50]
            lines.append(f"{prefix}  {self._color('Default:', self.DIM)} {default}")

        # Object properties
        if "properties" in schema and isinstance(schema["properties"], dict):
            required = set(schema.get("required", []))
            lines.append(f"{prefix}  {self._color('Properties:', self.BOLD)}")
            for prop_name, prop_schema in schema["properties"].items():
                lines.append(f"{prefix}    {self._color('┌─', self.DIM)} {prop_name}")
                sub_lines = self._render_schema(prop_schema, depth + 3, 
                    prop_name in required)
                for sl in sub_lines:
                    # Adjust indentation for nested properties
                    lines.append(sl)

        # Array items
        if "items" in schema:
            lines.append(f"{prefix}  {self._color('Items:', self.BOLD)}")
            sub_lines = self._render_schema(schema["items"], depth + 2)
            for sl in sub_lines:
                lines.append(sl)

        # Prefix items (tuple schema)
        if "prefixItems" in schema:
            lines.append(f"{prefix}  {self._color('Tuple Items:', self.BOLD)}")
            for i, item_schema in enumerate(schema["prefixItems"]):
                lines.append(f"{prefix}    [{i}]")
                sub_lines = self._render_schema(item_schema, depth + 3)
                for sl in sub_lines:
                    lines.append(sl)

        # allOf
        if "allOf" in schema:
            lines.append(f"{prefix}  {self._color('allOf:', self.BOLD)}")
            for i, sub in enumerate(schema["allOf"]):
                lines.append(f"{prefix}    [{i}]")
                sub_lines = self._render_schema(sub, depth + 3)
                for sl in sub_lines:
                    lines.append(sl)

        # anyOf
        if "anyOf" in schema:
            lines.append(f"{prefix}  {self._color('anyOf:', self.BOLD)}")
            for i, sub in enumerate(schema["anyOf"]):
                lines.append(f"{prefix}    [{i}]")
                sub_lines = self._render_schema(sub, depth + 3)
                for sl in sub_lines:
                    lines.append(sl)

        # oneOf
        if "oneOf" in schema:
            lines.append(f"{prefix}  {self._color('oneOf:', self.BOLD)}")
            for i, sub in enumerate(schema["oneOf"]):
                lines.append(f"{prefix}    [{i}]")
                sub_lines = self._render_schema(sub, depth + 3)
                for sl in sub_lines:
                    lines.append(sl)

        # if/then/else
        if "if" in schema:
            lines.append(f"{prefix}  {self._color('Conditional:', self.BOLD)}")
            lines.append(f"{prefix}    if:")
            sub_lines = self._render_schema(schema["if"], depth + 3)
            for sl in sub_lines:
                lines.append(sl)
            if "then" in schema:
                lines.append(f"{prefix}    then:")
                sub_lines = self._render_schema(schema["then"], depth + 3)
                for sl in sub_lines:
                    lines.append(sl)
            if "else" in schema:
                lines.append(f"{prefix}    else:")
                sub_lines = self._render_schema(schema["else"], depth + 3)
                for sl in sub_lines:
                    lines.append(sl)

        return lines

    def generate_markdown_doc(self, schema: Union[Dict, str], 
                              title: str = "Schema Documentation") -> str:
        """Generate Markdown documentation from schema"""
        if isinstance(schema, str):
            with open(schema, 'r', encoding='utf-8') as f:
                schema = json.load(f)

        lines = [f"# {title}", ""]

        if "description" in schema:
            lines.append(schema["description"])
            lines.append("")

        lines.append("## Schema Overview")
        lines.append("")
        lines.append(f"- **Draft**: `{schema.get('$schema', 'Unknown')}`")
        lines.append(f"- **ID**: `{schema.get('$id', schema.get('id', 'N/A'))}`")
        lines.append("")

        if "properties" in schema:
            lines.append("## Properties")
            lines.append("")
            required = set(schema.get("required", []))
            for prop_name, prop_schema in schema["properties"].items():
                req = " **(required)**" if prop_name in required else ""
                lines.append(f"### `{prop_name}`{req}")
                lines.append("")
                lines.extend(self._prop_to_markdown(prop_schema, 0))
                lines.append("")

        return "\n".join(lines)

    def _prop_to_markdown(self, schema: Dict, depth: int) -> List[str]:
        """Convert property schema to markdown lines"""
        lines = []
        indent = "  " * depth

        schema_type = schema.get("type", "any")
        if isinstance(schema_type, list):
            type_str = " | ".join(f"`{t}`" for t in schema_type)
        else:
            type_str = f"`{schema_type}`"
        lines.append(f"{indent}- **Type**: {type_str}")

        if "description" in schema:
            lines.append(f"{indent}- **Description**: {schema['description']}")

        if "default" in schema:
            lines.append(f"{indent}- **Default**: `{json.dumps(schema['default'])}`")

        constraints = []
        for key in ["minLength", "maxLength", "minimum", "maximum", "exclusiveMinimum",
                    "exclusiveMaximum", "multipleOf", "minItems", "maxItems",
                    "minProperties", "maxProperties", "pattern", "format"]:
            if key in schema:
                constraints.append(f"`{key}={schema[key]}`")
        if constraints:
            lines.append(f"{indent}- **Constraints**: {', '.join(constraints)}")

        if "enum" in schema:
            vals = ", ".join(f"`{json.dumps(v)}`" for v in schema["enum"])
            lines.append(f"{indent}- **Enum**: {vals}")

        if "properties" in schema:
            lines.append(f"{indent}- **Nested Properties**:")
            for prop_name, prop_schema in schema["properties"].items():
                lines.append(f"{indent}  - `{prop_name}`:")
                lines.extend(self._prop_to_markdown(prop_schema, depth + 2))

        if "items" in schema:
            lines.append(f"{indent}- **Array Items**:")
            lines.extend(self._prop_to_markdown(schema["items"], depth + 1))

        return lines
