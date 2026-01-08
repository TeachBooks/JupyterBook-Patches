from jupyterbook_patches.patches import BasePatch, logger


class DarkModePatch(BasePatch):
    name = "layout"

    def initialize(self, app):
        logger.info("Initializing layout patch")
        app.add_css_file(filename="fix_admonition_style.css")
        app.add_css_file(filename="fix_dropdown_style.css")
        app.add_css_file(filename="fix_code_header_style.css")
        app.add_css_file(filename="fix_sidebar_scroll.css")
        app.add_css_file(filename="fix_margin.css")
        app.add_css_file(filename="fix_align_text_captions.css")
        app.add_css_file(filename="fix_align_code.css")
