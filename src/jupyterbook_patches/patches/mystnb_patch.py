"""
This patch performs the following fixes for MyST-NB in Sphinx:
- Colon fences (such as `:::`) for top-level `code-cell`s are now allowed, next to backtick fences (such as ```` ``` ````), inside markdown files.
- The `include` directive now correctly handles included content from markdown files with top-level `code-cell`s and/or YAML front-matter from markdown files.
- Markdown files that contain and/or include top-level `code-cell`s are ensured to be a text-based notebook file.
"""

from __future__ import annotations

from jupyterbook_patches.patches import BasePatch, logger
from myst_nb.core.read import is_myst_markdown_notebook
from pathlib import Path

import re


class MySTNBPatch(BasePatch):
    name = "mystnb"

    def initialize(self, app):
        logger.info("Initializing MyST-NB patch")
        # Remove yaml header in included files. This does not affect the original file.
        # Included content with code-cells will not work properly, as code-cells cannot be nested.
        app.connect("include-read", fix_remove_yaml_from_include)

        # Replace include of myst notebooks with content of myst notebooks before parsing, as nested notebooks are not supported.
        # This does not affect the original files.
        # If the including file is not an md-file, no changes are made.
        # If the included file is a myst-notebook, but does not contain code cells, no changes are made.
        # if the included file is a md-file with code cells, the include directive is replaced with the content of the myst notebook ánd a yaml header is generated if needed.
        # If the including file is not a myst notebook, the yaml header of the included myst notebook is added to the yaml header of the including file.
        # If a yaml header is present in the including file, the yaml header of the included myst notebook is appended to the yaml header of the including file.
        app.connect("source-read", fix_include_with_code_cells)

        # if a md-file contains code-cells, make sure that colon fences are replaced with backtick fences and that a yaml header is present
        app.connect("source-read", fix_file_with_code_cells)


DEFAULT_YAML_FRONT_MATTER = "---\nfile_format: mystnb\nkernelspec:\n  name: python3\n---"
FENCE_COLON = ":{3,}"
FENCE_BACKTICK = "`{3,}"
FENCE_PATTERN = f"(?P<fence>{FENCE_COLON}|{FENCE_BACKTICK})"

DIRECTIVE_PATTERN = rf"^{FENCE_PATTERN}(?:\{{[^}}]+\}}|\S+)?(?:\s|$)"
INCLUDE_PATTERN = rf"^{FENCE_PATTERN}\{{include\}}(?:\s+(?P<rest>.*))?$"
CODE_CELL_PATTERN = rf"^{FENCE_PATTERN}\{{code-cell\}}(?:\s+(?P<rest>.*))?$"


def _strip_yaml(lines: list[str]) -> tuple[list[str], list[str] | list[None]]:
    # strips yaml front matter from included lines
    # returns modified lines or original lines if no changes were made
    # and returns yaml front matter if present

    if not lines:
        return lines, None
    yaml_front_matter = [None] * len(lines)
    for ix, lines_set in enumerate(lines):
        file_lines = lines_set.splitlines()
        if len(file_lines) == 0 or file_lines[0].strip() != "---":
            continue
        # yaml front matter detected
        # find closing delimiter
        closing_index = None
        for i in range(1, len(file_lines)):
            tok = file_lines[i].strip()
            if tok == "---":
                closing_index = i
                break
        if closing_index is not None:  # no closing delimiter -> leave unchanged
            yaml_front_matter[ix] = "\n".join(file_lines[0 : closing_index + 1])
            file_lines = file_lines[closing_index + 1 :]
            lines[ix] = "\n".join(file_lines)
    return lines, yaml_front_matter


def _parse_directive_blocks(lines: list[str]) -> list[list[str]]:
    """Parse list of strings and return all top-level blocks (fenced with colons or backticks) from lines."""
    blocks = []
    i = 0
    finding_end = False
    block = []
    fence = None

    while i < len(lines):
        line = lines[i]
        directive_match = re.match(DIRECTIVE_PATTERN, line)
        if directive_match and not finding_end:
            fence = directive_match.group("fence")
            block.append(line)
            finding_end = True
        elif directive_match and finding_end:
            block.append(line)
            new_fence = directive_match.group("fence")
            if new_fence == fence:
                blocks.append(block)
                finding_end = False
                block = []
                fence = None
        elif finding_end:
            block.append(line)
        i += 1

    return blocks


def _replace_block_in_content(content: str, old_block: list[str], new_block: list[str]) -> str:
    """Replace an old block with a new block in content string."""
    old_block_str = "\n".join(old_block)
    new_block_str = "\n".join(new_block)
    return content.replace(old_block_str, new_block_str)


def _add_or_combine_yaml_front_matter(source: str, yaml_to_add: str) -> str:
    """Add or combine YAML front matter to source content."""
    new_source, existing_yaml = _strip_yaml([source])
    new_source = new_source[0]
    existing_yaml = existing_yaml[0]

    if not existing_yaml:
        return yaml_to_add + "\n" + new_source
    else:
        existing_yaml_lines = existing_yaml.splitlines()[1:-1]
        new_yaml_lines = yaml_to_add.splitlines()[1:-1]
        combined_yaml = "---\n" + "\n".join(existing_yaml_lines + new_yaml_lines) + "\n---"
        return combined_yaml + "\n" + new_source


def _find_top_level_includes(lines: list[str]) -> list[dict[str, list[str] | str]]:
    includes = []
    blocks = _parse_directive_blocks(lines)

    # for each block, check if it's an include directive at top level
    for block in blocks:
        include_match = re.match(INCLUDE_PATTERN, block[0])
        if include_match:
            rest = include_match.group("rest")
            rest = rest.strip() if rest else ""

            options = block[1:-1] if len(block) > 2 else []
            options = _parse_block_options(options)
            includes.append({"file": rest, "options": options, "block": block})

    return includes


def _find_top_level_code_cells(lines: list[str]) -> tuple[bool, list[list[str]], list[list[str]]]:
    code_cells = False
    colon_fenced_blocks = []
    backtick_fenced_blocks = []

    blocks = _parse_directive_blocks(lines)

    # for each block, check if it's a code-cell directive at top level
    for block in blocks:
        code_cell_match = re.match(CODE_CELL_PATTERN, block[0])
        if code_cell_match:
            # This is a top-level code-cell, so we now at least one code cell is present
            # this might be a code-cell with a colon fence, so if that is the case, we want to change that
            # to that end, return also two blocks: the original and the modified one
            code_cells = True
            fence = code_cell_match.group("fence")
            if fence.startswith(":"):
                colon_fenced_blocks.append(block)
                # create new block with backtick fence
                backtick_fenced_block = block.copy()
                backtick_fenced_block[0] = backtick_fenced_block[0].replace(fence, "`" * len(fence))
                backtick_fenced_block[-1] = backtick_fenced_block[-1].replace(fence, "`" * len(fence))
                backtick_fenced_blocks.append(backtick_fenced_block)

    return code_cells, colon_fenced_blocks, backtick_fenced_blocks


def _parse_block_options(option_lines: list[str]) -> dict[str, str]:
    """Parse option lines of the form ":key: value" into a dictionary."""
    options_dict = {}
    for opt_line in option_lines:
        if ":" in opt_line:
            key, value = opt_line.strip().lstrip(":").split(":", 1)
            options_dict[key.strip()] = value.strip()
    return options_dict


def _apply_include_slice_options(content: list[str], options: dict[str, str]) -> list[str]:
    """Apply start-line, end-line, start-after, end-before options to slice content."""
    start_line = 0
    end_line = len(content)

    if "start-line" in options:
        start_line = int(options["start-line"]) - 1
    if "end-line" in options:
        end_line = int(options["end-line"])
    if "start-after" in options:
        for i, line in enumerate(content):
            if options["start-after"] in line:
                start_line = i + 1
                break
    if "end-before" in options:
        for i, line in enumerate(content):
            if options["end-before"] in line:
                end_line = i
                break

    return content[start_line:end_line]


def _prepare_included_content(content: list[str]) -> tuple[list[str], str]:
    """Strip YAML, detect if notebook, set appropriate YAML front matter."""
    content_str = "\n".join(content)
    if is_myst_markdown_notebook(content_str):
        new_content, yaml_fm = _strip_yaml([content_str])
        return new_content[0].splitlines(), yaml_fm[0]
    else:
        new_content, _ = _strip_yaml([content_str])
        return new_content[0].splitlines(), DEFAULT_YAML_FRONT_MATTER


def fix_remove_yaml_from_include(app, docname, path, content) -> None:
    # preferably remove yaml front matter only from included md-files
    # this is however not possible, as only the content of the included file is passed
    # and not the source
    # content is a list[str]; modify in-place
    new, _ = _strip_yaml(content)
    if new is not content:
        content[:] = new


def fix_include_with_code_cells(app, docname, source) -> None:
    # Resolve the actual source file path for this docname (with extension)
    src_path = Path(app.env.doc2path(docname))
    ext = src_path.suffix  # e.g. ".rst", ".md", ".ipynb"

    if ext != ".md":
        return
    # check if any top-level include is present
    include_files = _find_top_level_includes(source[0].splitlines())
    if include_files:
        for include in include_files:
            # resolve the included file path
            if include["file"].startswith("/"):
                include_path = Path(app.srcdir) / include["file"][1:]
            else:
                include_path = src_path.parent / include["file"]
            # load the included file content if it is a markdown file and exists
            if not include_path.exists() or include_path.suffix != ".md":
                continue
            with open(include_path, "r", encoding="utf-8") as f:
                include_content = f.readlines()
            # parse the options of the include
            include_content = _apply_include_slice_options(include_content, include["options"])
            # now check if the content to include is a myst notebook with code-cells or just contains code-cells or neither
            new_content, yaml_front_matter = _prepare_included_content(include_content)
            # check if any top-level code-cells are present in the included content (must be improved)
            has_code_cells, old_blocks, new_blocks = _find_top_level_code_cells(new_content)
            for old_block, new_block in zip(old_blocks, new_blocks):
                new_content_str = "\n".join(new_content)
                new_content_str = _replace_block_in_content(new_content_str, old_block, new_block)
                new_content = new_content_str.splitlines()
            # if code-cells are present, replace the ENTIRE include directive with the content of the myst notebook (without yaml frontmatter)
            # also check if the including file has a yaml front matter and take appropriate actions
            if has_code_cells:
                # plain replacement
                source[0] = _replace_block_in_content(source[0], include["block"], new_content)
                # check if including file has yaml front matter that specifies mystnb format
                including_file_is_mystnb = is_myst_markdown_notebook(source[0])
                # if including file is not a myst notebook, add yaml front matter
                # be careful to insert at the top of the file
                # and to respect existing yaml front matter
                if not including_file_is_mystnb:
                    source[0] = _add_or_combine_yaml_front_matter(source[0], yaml_front_matter)


def fix_file_with_code_cells(app, docname, source) -> None:
    # Resolve the actual source file path for this docname (with extension)
    src_path = Path(app.env.doc2path(docname))
    ext = src_path.suffix  # e.g. ".rst", ".md", ".ipynb"

    # first check if the file is a text-based notebook
    if ext != ".md":
        return
    source_is_notebook = is_myst_markdown_notebook(source[0])

    # then check if any top-level code-cells are present
    has_code_cells, old_blocks, new_blocks = _find_top_level_code_cells(source[0].splitlines())

    # replace colon-fenced code-cells with backtick-fenced code-cells
    for old_block, new_block in zip(old_blocks, new_blocks):
        source[0] = _replace_block_in_content(source[0], old_block, new_block)

    # if code-cells are present, but not a myst notebook, add yaml front matter
    if has_code_cells and not source_is_notebook:
        source[0] = _add_or_combine_yaml_front_matter(source[0], DEFAULT_YAML_FRONT_MATTER)
