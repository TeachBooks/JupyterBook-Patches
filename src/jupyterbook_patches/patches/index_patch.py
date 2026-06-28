from jupyterbook_patches.patches import BasePatch
from sphinx.application import Sphinx

from sphinx.environment.adapters.indexentries import IndexEntries
from pathlib import PurePosixPath
from docutils import nodes
import yaml
import os
import re


class IndexPatch(BasePatch):
    name = "index"

    def initialize(self, app):
        app.connect('builder-inited', add_template_path)
        app.connect("builder-inited", patch_index)

def add_template_path(app:Sphinx, exception=None):
    if exception:
        return

    X = app.config.patch_config["templates_path"]

    # Update the Jinja2 environment's template loader
    if hasattr(app.builder, 'templates'):
        for loader in app.builder.templates.loaders:
            if hasattr(loader, 'searchpath'):
                loader.searchpath.insert(0, X)

def patch_index(app):
    env = app.env

    # -----------------------------
    # Build TOC document order
    # -----------------------------
    doc_order = build_doc_order(env)

    # -----------------------------
    # Build anchor positions per doc
    # -----------------------------
    anchor_positions = build_anchor_positions(env)

    # -----------------------------
    # Monkeypatch
    # -----------------------------
    original = IndexEntries.create_index

    def custom_create_index(self, builder, group_entries=True):
        content = original(self, builder, group_entries)

        for _, entries in content:
            for i, (term, (links, subitems, key)) in enumerate(entries):

                def sort_key(link):
                    # Current Sphinx index targets are (main, uri) pairs.
                    _, uri = link

                    if not uri:
                        return (10**9, 10**9)

                    target = uri.split("#", 1)[0]
                    anchor = uri.split("#", 1)[1] if "#" in uri else ""
                    docname = target[:-5] if target.endswith(".html") else target

                    # 1. TOC order
                    doc_pos = doc_order.get(docname, 10**9)

                    # 2. Prefer numeric index anchors when available so same-document
                    # entries follow their source order in the generated index.
                    index_match = re.search(r"index-(\d+)$", anchor)
                    if index_match:
                        anchor_pos = (0, int(index_match.group(1)))
                    else:
                        anchor_map = anchor_positions.get(docname, {})
                        anchor_pos = (1, anchor_map.get(anchor, 10**9))

                    return (doc_pos, anchor_pos)

                links.sort(key=sort_key)

                entries[i] = (term, (links, subitems, key))

        return content

    IndexEntries.create_index = custom_create_index


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def build_doc_order(env):
    """
    Build document order based on the external TOC file order.
    """
    order = {}
    counter = [0]

    def normalize_docname(path):
        if not path:
            return None
        normalized = path.replace("\\", "/")
        return str(PurePosixPath(normalized).with_suffix(""))

    def add_doc(path):
        docname = normalize_docname(path)
        if docname and docname not in order:
            order[docname] = counter[0]
            counter[0] += 1

    def walk_item(item):
        if not isinstance(item, dict):
            return

        add_doc(item.get("file"))

        for key in ("parts", "chapters", "sections"):
            for child in item.get(key, []) or []:
                walk_item(child)

    toc_name = getattr(env.config, "external_toc_path", "_toc.yml")
    toc_path = toc_name if os.path.isabs(toc_name) else os.path.join(env.app.srcdir, toc_name)

    if os.path.exists(toc_path):
        try:
            with open(toc_path, "r", encoding="utf-8") as toc_file:
                toc_data = yaml.safe_load(toc_file) or {}
        except Exception as exc:
            pass
        else:
            add_doc(toc_data.get("root"))
            for part in toc_data.get("parts", []) or []:
                walk_item(part)

    # fallback: include any missing docs
    for doc in env.found_docs:
        if doc not in order:
            order[doc] = counter[0]
            counter[0] += 1

    return order


def build_anchor_positions(env):
    """
    Build approximate top-to-bottom order of anchors per document
    """
    positions = {}

    for docname in env.found_docs:
        try:
            doctree = env.get_doctree(docname)
        except FileNotFoundError:
            continue
        pos = {}
        counter = 0

        for node in doctree.traverse():
            if not isinstance(node, nodes.Element):
                continue
            ids = node.get("ids", [])
            for anchor in ids:
                pos[anchor] = counter
            counter += 1

        positions[docname] = pos

    return positions
