from jupyterbook_patches.patches import BasePatch, logger
from sphinx.application import Sphinx

class MarginPatch(BasePatch):
    name = "margin"

    def initialize(self, app):
        logger.info("Initializing Margin patch")
        app.add_css_file(filename="margin_patch.css")