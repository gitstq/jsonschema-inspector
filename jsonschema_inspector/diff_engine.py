"""
Schema Diff Engine - Compare two JSON Schemas and identify differences
"""

import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class SchemaChange:
    """Represents a single schema change"""

    def __init__(self, change_type: str, path: str, old_value: Any = None,
                 new_value: Any = None, description: str = ""):
        self.change_type = change_type  # added, removed, modified, type_changed
        self.path = path
        self.old_value = old_value
        self.new_value = new_value
        self.description = description

    def __repr__(self):
        return f"SchemaChange({self.change_type}: {self.path})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "change_type": self.change_type,
            "path": self.path,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "description": self.description,
        }


class SchemaDiffEngine:
    """
    Compare two JSON Schemas and produce detailed diff report
    """

    def __init__(self):
        self.changes: List[SchemaChange] = []

    def compare(self, old_schema: Union[Dict, str], 
                new_schema: Union[Dict, str]) -> List[SchemaChange]:
        """
        Compare two schemas and return list of changes
        
        Args:
            old_schema: Original schema (dict or file path)
            new_schema: New schema (dict or file path)
            
        Returns:
            List of SchemaChange objects
        """
        if isinstance(old_schema, str):
            with open(old_schema, 'r', encoding='utf-8') as f:
                old_schema = json.load(f)
        if isinstance(new_schema, str):
            with open(new_schema, 'r', encoding='utf-8') as f:
                new_schema = json.load(f)

        self.changes = []
        self._compare_schemas(old_schema, new_schema, "")
        return self.changes

    def _compare_schemas(self, old: Any, new: Any, path: str):
        """Recursively compare two schema values"""
        if old is None and new is not None:
            self.changes.append(SchemaChange(
                "added", path, None, new,
                f"Added at {path}"
            ))
            return

        if old is not None and new is None:
            self.changes.append(SchemaChange(
                "removed", path, old, None,
                f"Removed from {path}"
            ))
            return

        if type(old) != type(new):
            self.changes.append(SchemaChange(
                "type_changed", path, old, new,
                f"Type changed from {type(old).__name__} to {type(new).__name__}"
            ))
            return

        if isinstance(old, dict):
            self._compare_dicts(old, new, path)
        elif isinstance(old, list):
            self._compare_lists(old, new, path)
        elif old != new:
            self.changes.append(SchemaChange(
                "modified", path, old, new,
                f"Value changed from {self._truncate(old)} to {self._truncate(new)}"
            ))

    def _compare_dicts(self, old: Dict, new: Dict, path: str):
        """Compare two dict schemas"""
        old_keys = set(old.keys())
        new_keys = set(new.keys())

        # Added keys
        for key in new_keys - old_keys:
            self.changes.append(SchemaChange(
                "added", f"{path}.{key}" if path else key, None, new[key],
                f"Added property '{key}'"
            ))

        # Removed keys
        for key in old_keys - new_keys:
            self.changes.append(SchemaChange(
                "removed", f"{path}.{key}" if path else key, old[key], None,
                f"Removed property '{key}'"
            ))

        # Modified keys
        for key in old_keys & new_keys:
            new_path = f"{path}.{key}" if path else key
            self._compare_schemas(old[key], new[key], new_path)

    def _compare_lists(self, old: List, new: List, path: str):
        """Compare two list schemas"""
        max_len = max(len(old), len(new))
        for i in range(max_len):
            item_path = f"{path}[{i}]"
            if i >= len(old):
                self.changes.append(SchemaChange(
                    "added", item_path, None, new[i],
                    f"Added item at index {i}"
                ))
            elif i >= len(new):
                self.changes.append(SchemaChange(
                    "removed", item_path, old[i], None,
                    f"Removed item at index {i}"
                ))
            else:
                self._compare_schemas(old[i], new[i], item_path)

    def _truncate(self, value: Any, max_len: int = 50) -> str:
        """Truncate value for display"""
        s = str(value)
        if len(s) > max_len:
            return s[:max_len] + "..."
        return s

    def get_summary(self) -> Dict[str, Any]:
        """Get diff summary"""
        added = len([c for c in self.changes if c.change_type == "added"])
        removed = len([c for c in self.changes if c.change_type == "removed"])
        modified = len([c for c in self.changes if c.change_type == "modified"])
        type_changed = len([c for c in self.changes if c.change_type == "type_changed"])

        return {
            "total_changes": len(self.changes),
            "added": added,
            "removed": removed,
            "modified": modified,
            "type_changed": type_changed,
            "breaking_changes": self._count_breaking_changes(),
        }

    def _count_breaking_changes(self) -> int:
        """Count potentially breaking changes"""
        breaking = 0
        for change in self.changes:
            if change.change_type == "removed":
                breaking += 1
            elif change.change_type == "modified":
                # Check if it's a type or required change
                if "type" in change.path or "required" in change.path:
                    breaking += 1
        return breaking

    def generate_report(self, format: str = "text") -> str:
        """Generate formatted diff report"""
        if format == "json":
            return json.dumps({
                "summary": self.get_summary(),
                "changes": [c.to_dict() for c in self.changes],
            }, indent=2)

        if format == "markdown":
            return self._generate_markdown_report()

        return self._generate_text_report()

    def _generate_text_report(self) -> str:
        """Generate text diff report"""
        summary = self.get_summary()
        lines = [
            "╔" + "═" * 58 + "╗",
            "║" + " Schema Diff Report".center(58) + "║",
            "╠" + "═" * 58 + "╣",
            f"║  Total Changes:    {summary['total_changes']:<36}║",
            f"║  Added:            {summary['added']:<36}║",
            f"║  Removed:          {summary['removed']:<36}║",
            f"║  Modified:         {summary['modified']:<36}║",
            f"║  Type Changed:     {summary['type_changed']:<36}║",
            f"║  Breaking Changes: {summary['breaking_changes']:<36}║",
            "╠" + "═" * 58 + "╣",
        ]

        for change in self.changes:
            icon = {
                "added": "+",
                "removed": "-",
                "modified": "~",
                "type_changed": "!",
            }.get(change.change_type, "?")

            color = {
                "added": "\033[32m",
                "removed": "\033[31m",
                "modified": "\033[33m",
                "type_changed": "\033[35m",
            }.get(change.change_type, "")
            reset = "\033[0m"

            lines.append(f"║  {color}[{icon}]{reset} {change.path:<52}║")
            if change.description:
                desc = change.description[:52]
                lines.append(f"║      {desc:<52}║")

        lines.append("╚" + "═" * 58 + "╝")
        return "\n".join(lines)

    def _generate_markdown_report(self) -> str:
        """Generate markdown diff report"""
        summary = self.get_summary()
        lines = [
            "# Schema Diff Report",
            "",
            "## Summary",
            "",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Total Changes | {summary['total_changes']} |",
            f"| Added | {summary['added']} |",
            f"| Removed | {summary['removed']} |",
            f"| Modified | {summary['modified']} |",
            f"| Type Changed | {summary['type_changed']} |",
            f"| Breaking Changes | {summary['breaking_changes']} |",
            "",
            "## Changes",
            "",
        ]

        for change in self.changes:
            icon = {
                "added": "✅",
                "removed": "❌",
                "modified": "📝",
                "type_changed": "⚠️",
            }.get(change.change_type, "❓")

            lines.append(f"### {icon} {change.change_type.upper()}: `{change.path}`")
            lines.append("")
            if change.old_value is not None:
                lines.append(f"- **Old**: `{change.old_value}`")
            if change.new_value is not None:
                lines.append(f"- **New**: `{change.new_value}`")
            if change.description:
                lines.append(f"- **Description**: {change.description}")
            lines.append("")

        return "\n".join(lines)
