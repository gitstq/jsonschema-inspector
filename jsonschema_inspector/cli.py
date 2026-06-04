#!/usr/bin/env python3
"""
JSONSchema-Inspector CLI
Main command-line interface
"""

import argparse
import json
import sys
import os
from typing import Optional

from .validator import SchemaValidator
from .visualizer import SchemaVisualizer
from .mock_generator import MockDataGenerator
from .diff_engine import SchemaDiffEngine


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog="jsonschema-inspector",
        description="🔍 JSONSchema-Inspector - Lightweight JSON Schema Visualization & Intelligent Validation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s validate schema.json data.json
  %(prog)s visualize schema.json
  %(prog)s mock schema.json --count 3
  %(prog)s diff old_schema.json new_schema.json
  %(prog)s doc schema.json --output api.md
        """
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate JSON data against schema",
        description="Validate JSON data against a JSON Schema"
    )
    validate_parser.add_argument("schema", help="JSON Schema file path")
    validate_parser.add_argument("data", help="JSON data file path")
    validate_parser.add_argument(
        "--draft",
        choices=["draft-07", "draft-2019-09", "draft-2020-12"],
        help="Schema draft version"
    )
    validate_parser.add_argument(
        "--output", "-o",
        help="Output file for validation report (JSON)"
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )

    # Visualize command
    viz_parser = subparsers.add_parser(
        "visualize",
        aliases=["viz"],
        help="Visualize schema structure",
        description="Generate terminal visualization of schema structure"
    )
    viz_parser.add_argument("schema", help="JSON Schema file path")
    viz_parser.add_argument(
        "--title", "-t",
        default="JSON Schema",
        help="Title for visualization"
    )
    viz_parser.add_argument(
        "--output", "-o",
        help="Output file for visualization"
    )

    # Mock command
    mock_parser = subparsers.add_parser(
        "mock",
        help="Generate mock data from schema",
        description="Generate sample data conforming to schema"
    )
    mock_parser.add_argument("schema", help="JSON Schema file path")
    mock_parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Number of samples to generate (default: 1)"
    )
    mock_parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible output"
    )
    mock_parser.add_argument(
        "--output", "-o",
        help="Output file for mock data"
    )

    # Diff command
    diff_parser = subparsers.add_parser(
        "diff",
        help="Compare two schemas",
        description="Compare two JSON Schemas and show differences"
    )
    diff_parser.add_argument("old_schema", help="Original schema file path")
    diff_parser.add_argument("new_schema", help="New schema file path")
    diff_parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format"
    )
    diff_parser.add_argument(
        "--output", "-o",
        help="Output file for diff report"
    )

    # Doc command
    doc_parser = subparsers.add_parser(
        "doc",
        help="Generate Markdown documentation",
        description="Generate Markdown documentation from schema"
    )
    doc_parser.add_argument("schema", help="JSON Schema file path")
    doc_parser.add_argument(
        "--title", "-t",
        default="Schema Documentation",
        help="Document title"
    )
    doc_parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output Markdown file"
    )

    return parser


def cmd_validate(args) -> int:
    """Handle validate command"""
    try:
        # Load schema
        with open(args.schema, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        # Load data
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Detect draft
        draft_map = {
            "draft-07": SchemaValidator.DRAFT_7,
            "draft-2019-09": SchemaValidator.DRAFT_2019_09,
            "draft-2020-12": SchemaValidator.DRAFT_2020_12,
        }
        draft = draft_map.get(args.draft)

        # Validate
        validator = SchemaValidator(schema, draft)
        is_valid = validator.validate(data)

        summary = validator.get_summary()

        # Print results
        use_color = not args.no_color
        green = "\033[32m" if use_color else ""
        red = "\033[31m" if use_color else ""
        yellow = "\033[33m" if use_color else ""
        reset = "\033[0m" if use_color else ""
        bold = "\033[1m" if use_color else ""

        print(f"\n{bold}╔{'═' * 58}╗{reset}")
        print(f"{bold}║{'Validation Result':^58}║{reset}")
        print(f"{bold}╠{'═' * 58}╣{reset}")

        if is_valid and (not args.strict or len(summary["warnings"]) == 0):
            status = f"{green}✓ VALID{reset}"
        else:
            status = f"{red}✗ INVALID{reset}"

        print(f"║  Status:     {status:<49}║")
        print(f"║  Errors:     {summary['error_count']:<49}║")
        print(f"║  Warnings:   {summary['warning_count']:<49}║")
        print(f"║  Draft:      {summary['draft']:<49}║")
        print(f"{bold}╠{'═' * 58}╣{reset}")

        if summary["errors"]:
            print(f"║  {red}{bold}Errors:{reset:<52}║")
            for error in summary["errors"]:
                path = error["path"] or "(root)"
                msg = error["message"][:45]
                print(f"║    {red}✗{reset} {path}: {msg:<37}║")

        if summary["warnings"]:
            print(f"║  {yellow}{bold}Warnings:{reset:<50}║")
            for warning in summary["warnings"]:
                path = warning["path"] or "(root)"
                msg = warning["message"][:45]
                print(f"║    {yellow}⚠{reset} {path}: {msg:<37}║")

        print(f"{bold}╚{'═' * 58}╝{reset}\n")

        # Save report if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            print(f"Report saved to: {args.output}")

        return 0 if is_valid else 1

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_visualize(args) -> int:
    """Handle visualize command"""
    try:
        visualizer = SchemaVisualizer(use_color=not args.no_color)
        output = visualizer.visualize(args.schema, args.title)

        if args.output:
            # Strip ANSI codes for file output
            import re
            clean_output = re.sub(r'\033\[[0-9;]*m', '', output)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(clean_output)
            print(f"Visualization saved to: {args.output}")
        else:
            print(output)

        return 0

    except FileNotFoundError:
        print(f"Error: Schema file not found: {args.schema}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_mock(args) -> int:
    """Handle mock command"""
    try:
        generator = MockDataGenerator(seed=args.seed)
        data = generator.generate(args.schema, args.count)

        output = json.dumps(data, indent=2, ensure_ascii=False)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Mock data saved to: {args.output}")
        else:
            print(output)

        return 0

    except FileNotFoundError:
        print(f"Error: Schema file not found: {args.schema}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_diff(args) -> int:
    """Handle diff command"""
    try:
        engine = SchemaDiffEngine()
        changes = engine.compare(args.old_schema, args.new_schema)

        report = engine.generate_report(args.format)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                # Strip ANSI for non-text formats
                if args.format == "text":
                    import re
                    report = re.sub(r'\033\[[0-9;]*m', '', report)
                f.write(report)
            print(f"Diff report saved to: {args.output}")
        else:
            print(report)

        summary = engine.get_summary()
        return 1 if summary["breaking_changes"] > 0 else 0

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_doc(args) -> int:
    """Handle doc command"""
    try:
        visualizer = SchemaVisualizer(use_color=False)
        doc = visualizer.generate_markdown_doc(args.schema, args.title)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(doc)

        print(f"Documentation saved to: {args.output}")
        return 0

    except FileNotFoundError:
        print(f"Error: Schema file not found: {args.schema}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main(argv: Optional[list] = None) -> int:
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "validate": cmd_validate,
        "visualize": cmd_visualize,
        "viz": cmd_visualize,
        "mock": cmd_mock,
        "diff": cmd_diff,
        "doc": cmd_doc,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
