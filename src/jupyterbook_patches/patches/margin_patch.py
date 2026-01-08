from jupyterbook_patches.patches import BasePatch
from sphinx.application import Sphinx

class MarginPatch(BasePatch):
    name = "margin"

    def initialize(self, app):
        app.add_css_file(filename="margin_patch.css")
