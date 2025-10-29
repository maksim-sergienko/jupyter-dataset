import os
import sys
import json
import hashlib
import argparse
from datetime import datetime
from urllib.parse import urlparse
import requests
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

DATASETS_URL = "https://raw.githubusercontent.com/maksim-sergienko/data-source/refs/heads/main/dataset-list.json"
TEMPLATE_PATH = "template/template.py"
OUT_DIR = "notebooks"
FILENAME_FORMAT = "{slug}.ipynb"

def slugify(s: str) -> str:
    import re
    s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def fetch_json(url: str):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def read_template(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def render_template(template: str, context: dict) -> str:
    out = template
    for k, v in context.items():
        out = out.replace("{{" + k + "}}", str(v if v is not None else ""))
    return out

def notebook_from_code_cells(code_cells, md_cells=None):
    nb = new_notebook()
    cells = []
    if md_cells:
        for md in md_cells:
            cells.append(new_markdown_cell(md))
    for c in code_cells:
        cells.append(new_code_cell(c))
    nb['cells'] = cells
    nb['metadata'] = {
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python"
        }
    }
    return nb

def ensure_out_dir(path):
    os.makedirs(path, exist_ok=True)

def write_if_changed(path, content):
    new_hash = sha256_text(content)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            old = f.read()
        if sha256_text(old) == new_hash:
            return False
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets-url", default=DATASETS_URL, help="URL that returns JSON list of datasets")
    parser.add_argument("--template", default=TEMPLATE_PATH, help="Path to template .py")
    parser.add_argument("--out", default=OUT_DIR, help="Output notebooks dir")
    args = parser.parse_args()

    datasets_url = args.datasets_url
    template_path = args.template
    out_dir = args.out

    print("Fetching datasets list from:", datasets_url)
    try:
        data = fetch_json(datasets_url)
    except Exception as e:
        print("Failed to fetch datasets list:", e)
        sys.exit(2)

    if not isinstance(data, list):
        print("Expected JSON array of datasets, got:", type(data))
        sys.exit(3)

    template = read_template(template_path)
    ensure_out_dir(out_dir)

    changed_files = []
    for ds in data:
        ds_id = ds.get("id") or ds.get("name") or ds.get("url")
        ds_name = ds.get("name") or ds_id
        ds_url = ds.get("url") or ""
        ds_desc = ds.get("description") or ""
        slug = slugify(ds_id)

        context = {
            "DATASET_ID": ds_id,
            "DATASET_NAME": ds_name,
            "DATASET_URL": ds_url,
            "DESCRIPTION": ds_desc
        }

        rendered_code = render_template(template, context)

        code_cells = [rendered_code]
        md_cells = [f"# Notebook: {ds_name}\n\nSource: {ds_url}\n\n{ds_desc}"]

        nb = notebook_from_code_cells(code_cells, md_cells)
        nb_text = nbformat.writes(nb)

        filename = FILENAME_FORMAT.format(slug=slug, id=ds_id)
        out_path = os.path.join(out_dir, filename)

        if write_if_changed(out_path, nb_text):
            print("Wrote:", out_path)
            changed_files.append(out_path)
        else:
            print("No changes for:", out_path)

    print("Done. Changed files count:", len(changed_files))
    return 0

if __name__ == "__main__":
    sys.exit(main())
