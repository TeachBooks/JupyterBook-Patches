"""Patch to preserve dropdown states during page navigation.

This patch saves and restores the open/closed state of dropdown admonitions
when navigating between page sections using hash links. This ensures that
users don't lose their expanded content when jumping to different parts of
the same page.
"""

from jupyterbook_patches.patches import BasePatch
from sphinx.application import Sphinx


class PreserveDropdownStatePatch(BasePatch):
    name = "preserve_dropdown_state"

    def initialize(self, app: Sphinx):
        app.add_js_file(filename="preserve_dropdown_state.js")
