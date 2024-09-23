from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util import logging

from jupyterbook_patches._version import version as __version__
from jupyterbook_patches.utils import load_patches

logger = logging.getLogger(__name__)


def set_static_path(app):
    static_path = Path(__file__).parent / "patches" / "_static"
    app.config.html_static_path.append(str(static_path))


def setup_patch_configuration(app: Sphinx, _env, _docnames):
    patch_config = app.config.patch_config
    defaults = {"disabled-patches": []}

    for key, val in defaults.items():
        if key not in patch_config:
            patch_config[key] = val

    if not isinstance(patch_config["disabled-patches"], list):
        raise TypeError(
            "Patch configuration value for 'disabled-patches' must be a list"
        )

    if len(patch_config["disabled-patches"]) == 0:
        logger.info("All patches enabled")
    else:
        logger.info("Disabled patches: %s", ", ".join(patch_config["disabled-patches"]))


def init_patches(app: Sphinx, _env, _docnames):
    patch_config = app.config.patch_config
    available_patches = load_patches()

    for patch_name, patch_class in available_patches.items():
        if patch_name in patch_config["disabled-patches"]:
            continue
        patch = patch_class()
        patch.initialize(app)


def setup(app: Sphinx):
    # Add our static path
    app.connect("builder-inited", set_static_path)
    app.connect("env-before-read-docs", setup_patch_configuration)
    app.connect("env-before-read-docs", init_patches)
    app.add_config_value("patch_config", {}, "html")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
