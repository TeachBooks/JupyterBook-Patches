from jupyterbook_patches.patches import BasePatch
from sphinx.application import Sphinx

class HashJumpPatch(BasePatch):
    name = "hash"

    def initialize(self, app):
        app.add_js_file(filename="fix_hash_jump.js")
        app.connect('builder-inited',set_hash_jump_path)

def set_hash_jump_path(app:Sphinx):

    app.config.hash_jump_path = 'fix_hash_jump.js'

    pass
