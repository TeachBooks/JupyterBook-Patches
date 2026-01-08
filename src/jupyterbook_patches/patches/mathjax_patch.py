from jupyterbook_patches.patches import BasePatch, logger
from sphinx.application import Sphinx

class MathJaxPatch(BasePatch):
    name = "mathjax"

    def initialize(self, app):
        logger.info("Initializing MathJax patch")
        app.add_js_file(filename="mathjax_patch.js")
        app.add_css_file(filename="mathjax_patch.css")
        app.connect('builder-inited',set_mathjax_path)

def set_mathjax_path(app:Sphinx):

    app.config.mathjax_path = 'mathjax_patch.js'

    pass

def set_mathjax_loading(app:Sphinx,config):

    # check if mathjax patch is disabled
    patch_config = app.config.patch_config
    if 'mathjax' in patch_config['disabled-patches']:
        return

    if 'mathjax3_config' not in config or config.mathjax3_config is None: # make sure some mathjax3_config exists
        config.mathjax3_config = {}

    if 'loader' not in config.mathjax3_config: # make sure loader exists
        config.mathjax3_config['loader'] = {}

    if 'load' not in config.mathjax3_config['loader']: # if load is not set, set it to load ui/lazy
        config.mathjax3_config['loader']['load'] = ['ui/lazy']
    else: # check if any ui/nonlazy has been set to load, if not add ui/lazy
        has_ui = False
        for item in config.mathjax3_config['loader']['load']:
            if item.startswith('ui/nonlazy'):
                has_ui = True
                break
        if not has_ui:
            config.mathjax3_config['loader']['load'].append('ui/lazy')
        # if item is ui/nonlazy, remove it (as it is not recognised by MathJax)
        if 'ui/nonlazy' in config.mathjax3_config['loader']['load']:
            config.mathjax3_config['loader']['load'].remove('ui/nonlazy')
    pass    