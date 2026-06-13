"""
Pure logic functions for the Shakespeare Programming Language.

This module provides a unified entry point for all pure (side-effect-free,
deterministic) functions used by the SPL interpreter. These functions are
ideal for regression testing and behavioral fingerprinting because they
produce identical outputs for identical inputs, regardless of execution
environment or timing.

The actual implementations live in domain-specific modules:
- name_normalization: Character name normalization
- char_codec: Character code conversion
- arithmetic: Pure mathematical operations (noun values, factorial, etc.)
- stack_ops: Character stack operation simulation
- comparison: Value comparison logic

This module re-exports all functions with their original names for backward
compatibility and as the single entry point for Regrets fingerprinting.
"""

from .name_normalization import normalize_name as normalize_character_name
from .char_codec import character_code_to_char
from .arithmetic import (
    positive_noun_phrase_value as compute_positive_noun_value,
    negative_noun_phrase_value as compute_negative_noun_value,
    factorial as compute_factorial,
    truncated_square_root as compute_square_root,
    truncated_quotient as compute_quotient,
    truncated_remainder as compute_remainder,
)
from .stack_ops import simulate_stack_operations as character_push_pop_sequence
from .comparison import evaluate_comparison as compare_values
