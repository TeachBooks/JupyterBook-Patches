from jupyterbook_patches.patches import BasePatch, logger


class ScrollPatch(BasePatch):
    name = "scroll"

    def initialize(self, app):
        logger.info("Initializing scroll patch")
        app.add_js_file(filename="scroll.js", loading_method="async")
