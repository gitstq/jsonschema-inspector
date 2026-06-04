"""
JSONSchema-Inspector - Lightweight JSON Schema Visualization & Intelligent Validation Engine
轻量级JSON Schema可视化验证与智能诊断引擎

A zero-dependency Python CLI tool for JSON Schema validation, visualization,
mock data generation, and schema diff analysis.
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .validator import SchemaValidator
from .visualizer import SchemaVisualizer
from .mock_generator import MockDataGenerator
from .diff_engine import SchemaDiffEngine
from .cli import main

__all__ = [
    "SchemaValidator",
    "SchemaVisualizer", 
    "MockDataGenerator",
    "SchemaDiffEngine",
    "main",
]
