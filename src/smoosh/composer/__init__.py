"""Content composition module for smoosh.

This module handles the composition of repository content into various formats and representations.
It acts as a content composer, similar to how a music composer arranges different parts into a
cohesive whole. The module provides:

1. Content Composition: Combines repository files in various modes (cat/fold/smoosh)
2. Format Arrangements: Structures output in different formats (text/json/yaml/markdown)
3. Statistical Analysis: Provides metrics about the composition process

The composer module is the heart of smoosh's content processing pipeline, taking analyzed
repository content and arranging it into useful, digestible formats.
"""

from .concatenator import concatenate_files
from .formatter import format_output

__all__ = ["concatenate_files", "format_output"]
