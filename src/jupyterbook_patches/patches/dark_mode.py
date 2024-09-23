from jupyterbook_patches.patches import BasePatch, logger


class DarkModePatch(BasePatch):
    name = "darkmode"

    def initialize(self, app):
        logger.info("Initializing dark mode patch")
        app.add_css_file(filename="fix_alert_dark_mode.css")
        app.add_css_file(filename="image_dark_mode.css")
