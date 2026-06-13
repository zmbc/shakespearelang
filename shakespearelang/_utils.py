"""
Backward-compatible utilities module for the Shakespeare Programming Language.

This module re-exports functions from their new domain-specific homes:
- normalize_name → name_normalization.normalize_name
- pos_context, parseinfo_context → error_formatting module

All original function signatures and behaviors are preserved.
Existing code that imports from _utils will continue to work unchanged.
"""

from .name_normalization import normalize_name
from .error_formatting import pos_context, parseinfo_context
