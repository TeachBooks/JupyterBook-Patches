# Sphinx extension: JupyterBook-Patches

This Sphinx extension fixes:
- an issue where drop down menus would still take up space after being minimized, and the patch fixes it through some css.
- an issue where in drop down code cells the shown summary remained lightgray instead of turning darkgrey. Fix through css.
- an issue where the size of code in a header is not the correct font size. Fix through css.

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

## Contribute
This tool's repository is stored on [GitHub](https://github.com/TeachBooks/JupyterBook-Patches). The `README.md` of the branch `manual_docs` is also part of the [TeachBooks manual](https://teachbooks.io/manual/external/JupyterBook-Patches/README.html) as a submodule. If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/JupyterBook-Patches). To update the `README.md` shown in the TeachBooks manual, create a fork and open a merge request for the [GitHub repository of the manual](https://github.com/TeachBooks/manual). If you intent to clone the manual including its submodules, clone using: `git clone --recurse-submodulesgit@github.com:TeachBooks/manual.git`.
