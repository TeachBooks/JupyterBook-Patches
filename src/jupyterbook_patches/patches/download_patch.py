from jupyterbook_patches.patches import BasePatch
from sphinx.application import Sphinx

class DownloadPatch(BasePatch):
    name = "download"

    def initialize(self, app):
        app.add_js_file(filename="download_patch.js")
        app.connect('builder-inited', set_download_path)

def set_download_path(app: Sphinx):

    app.config.download_path = 'download_patch.js'

    pass
