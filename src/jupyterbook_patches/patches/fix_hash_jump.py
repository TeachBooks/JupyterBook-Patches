from jupyterbook_patches.patches import BasePatch, logger
from sphinx.application import Sphinx

class HashJumpPatch(BasePatch):
    name = "hash"

    def initialize(self, app):
        logger.info("Initializing HashJump patch")
        app.add_js_file(filename="fix_hash_jump.js")
        app.connect('builder-inited',set_hash_jump_path)

def set_hash_jump_path(app:Sphinx):

    app.config.hash_jump_path = 'fix_hash_jump.js'

    pass