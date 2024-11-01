# Sphinx extension: JupyterBook-Patches

```{admonition} User types
:class: tip
This section is useful for user type 4-5.
```

This Sphinx extension fixes an issue where drop down menus would still take up space after being minimized, and the patch fixes it through some css.

## Installation
To install the Sphinx-JupyterBook-Patches, follow these steps:

**Step 1: Install the Package**

Install the `jupyterbook_patches` package using `pip`:
```
pip install jupyterbook_patches
```

**Step 2: Add to `requirements.txt`**

Make sure that the package is included in your project's `requirements.txt` to track the dependency:
```
jupyterbook_patches
```

**Step 3: Enable in `_config.yml`**

In your `_config.yml` file, add the extension to the list of Sphinx extra extensions:
```
sphinx: 
    extra_extensions:
        - jupyterbook_patches
```
