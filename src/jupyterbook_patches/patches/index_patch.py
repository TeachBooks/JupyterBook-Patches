from pathlib import Path

from jupyterbook_patches.patches import BasePatch
from sphinx.application import Sphinx
from jinja2.loaders import FileSystemLoader

from sphinx.util import logging

logger = logging.getLogger(__name__)

class IndexPatch(BasePatch):
    name = "index"

    def initialize(self, app):
        app.connect('builder-inited', add_template_path)

def add_template_path(app:Sphinx, exception=None):
    if exception:
        return

    X = app.config.patch_config["templates_path"]

    # Update the Jinja2 environment's template loader
    if hasattr(app.builder, 'templates'):
        for loader in app.builder.templates.loaders:
            if hasattr(loader, 'searchpath'):
                loader.searchpath.insert(0, X)
                logger.info(f"Updated Jinja2 loader searchpath: {loader.searchpath}", color="yellow")