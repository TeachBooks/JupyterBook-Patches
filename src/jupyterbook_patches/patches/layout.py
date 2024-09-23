from jupyterbook_patches.patches import BasePatch, logger


class DarkModePatch(BasePatch):
    name = "layout"

    def initialize(self, app):
        logger.info("Initializing layout patch")
        app.add_css_file(filename="fix_admonition_style.css")
