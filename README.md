# Sphinx extension: JupyterBook-Patches

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15101012.svg)](https://doi.org/10.5281/zenodo.15101012)

This Sphinx extension fixes:
- with a `layout` patch:
    - an issue where drop down menus would still take up space after being minimized, and the patch fixes it through some css.
    - an issue where in drop down code cells the shown summary remained lightgray instead of turning darkgrey. Fix through css.
    - an issue where the size of code in a header is not the correct font size. Fix through css.
    - an issue where the sidebar shows a scrollbar even if that's not needed
    - an issue where the margin causes a scroll bar for a window between 992 and 1200px.
    - an issue where the caption text of a figure is aligned on the left for multi-line caption text
- with a `button` patch:
    - an issue where two buttons for interactive matplotlib widget do not appear.
- with a `mathjax` patch:
    - an issue where in the Firefox browser the CHTML renderer of MathJax does not render thin lines consistently. Fixed by selecting the SVG renderer *only* for the Firefox browser. 
- with a `download` patch:
    - an issue where the standard download button for downloading `.ipynb` and `.md` files opens a new tab instead of downloading the file. Fixed by adding the `download` attribute to the download links.

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

**Step 4 (optional): Disable patches in `_config.yml`**

In your `_config.yml` file, add disable patches you do not wish:
```
sphinx: 
    config:
        patch_config:
            disabled-patches: []
```

Replace `[]` by a list of strings to disable patches. Use the patch name as indicated at the top of this document.

For example, to disable the `mathjax` patch:

```
sphinx: 
    config:
        patch_config:
            disabled-patches: ["mathjax"]
```

For example, to disable the `layout` and `button` patches:

```
sphinx: 
    config:
        patch_config:
            disabled-patches: ["button","layout"]
```


## Contribute
This tool's repository is stored on [GitHub](https://github.com/TeachBooks/JupyterBook-Patches). The `README.md` of the branch `manual_docs` is also part of the [TeachBooks manual](https://teachbooks.io/manual/external/JupyterBook-Patches/README.html) as a submodule. If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/JupyterBook-Patches). To update the `README.md` shown in the TeachBooks manual, create a fork and open a merge request for the [GitHub repository of the manual](https://github.com/TeachBooks/manual). If you intent to clone the manual including its submodules, clone using: `git clone --recurse-submodulesgit@github.com:TeachBooks/manual.git`.
