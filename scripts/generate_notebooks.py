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
from generate_readme import DEFAULT_BRANCH, DEFAULT_REPOSITORY, README_PATH, render_readme

DATASETS_URL = "https://n8n.msergienko.com/webhook/datasets"
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
        for index, md in enumerate(md_cells):
            cell = new_markdown_cell(md)
            cell["id"] = sha256_text(f"markdown:{index}:{md}")[:8]
            cells.append(cell)
    for index, c in enumerate(code_cells):
        cell = new_code_cell(c)
        cell["id"] = sha256_text(f"code:{index}:{c}")[:8]
        cells.append(cell)
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
    parser.add_argument("--readme", default=README_PATH, help="Path to generated README.md")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPOSITORY), help="GitHub repository in owner/name format")
    parser.add_argument("--branch", default=os.environ.get("GITHUB_REF_NAME", DEFAULT_BRANCH), help="GitHub branch for notebook links")
    args = parser.parse_args()

    datasets_url = args.datasets_url
    template_path = args.template
    out_dir = args.out
    readme_path = args.readme

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
    generated_notebooks = []
    for ds in data:
        ds_id = ds.get("id")
        ds_name = ds.get("Name")
        slug = ds_id

        context = {
            "DATASET_ID": ds_id,
            "DATASET_NAME": ds_name,
        }

        rendered_code = render_template(template, context)

        code_cells = [rendered_code]
        md_cells = [f"# Notebook: {ds_name}"]

        nb = notebook_from_code_cells(code_cells, md_cells)
        nb_text = nbformat.writes(nb)

        filename = FILENAME_FORMAT.format(slug=slug, id=ds_id)
        out_path = os.path.join(out_dir, filename)
        notebook_path = os.path.relpath(out_path).replace(os.sep, "/")
        generated_notebooks.append({
            "name": ds_name or filename,
            "path": notebook_path,
        })

        if write_if_changed(out_path, nb_text):
            print("Wrote:", out_path)
            changed_files.append(out_path)
        else:
            print("No changes for:", out_path)

    readme_text = render_readme(generated_notebooks, args.repository, args.branch)
    if write_if_changed(readme_path, readme_text):
        print("Wrote:", readme_path)
        changed_files.append(readme_path)
    else:
        print("No changes for:", readme_path)

    print("Done. Changed files count:", len(changed_files))
    return 0

if __name__ == "__main__":
    sys.exit(main())
