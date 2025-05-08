from jupyterbook_patches.patches import BasePatch, logger
from sphinx.application import Sphinx

class MathJaxPatch(BasePatch):
    name = "mathjax"

    def initialize(self, app):
        logger.info("Initializing MathJax patch")
        app.add_js_file(filename="mathjax_patch.js")
        app.connect('builder-inited',set_mathjax_path)

def set_mathjax_path(app:Sphinx):

    app.config.mathjax_path = 'mathjax_patch.js'

    pass