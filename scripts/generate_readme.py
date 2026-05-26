from urllib.parse import quote


README_PATH = "README.md"
DEFAULT_REPOSITORY = "maksim-sergienko/jupyter-dataset"
DEFAULT_BRANCH = "main"


def build_service_links(repository, branch, notebook_path):
    encoded_path = quote(notebook_path, safe="/")
    encoded_filepath = quote(notebook_path, safe="")
    return {
        "Colab": f"https://colab.research.google.com/github/{repository}/blob/{branch}/{encoded_path}",
        "Binder": f"https://mybinder.org/v2/gh/{repository}/{branch}?filepath={encoded_filepath}",
        "github.dev": f"https://github.dev/{repository}/blob/{branch}/{encoded_path}",
    }


def badge(label, color):
    encoded_label = quote(label.replace("-", "--"), safe="")
    return f"https://img.shields.io/badge/{encoded_label}-{color}?style=for-the-badge"


def render_readme(notebooks, repository, branch):
    lines = [
        "# Jupyter Dataset Notebooks",
        "",
        "Generated notebooks for the available datasets.",
        "",
    ]

    for notebook in notebooks:
        lines.extend([
            f"## {notebook['name']}",
            "",
            f"`{notebook['path']}`",
            "",
        ])

        links = build_service_links(repository, branch, notebook["path"])
        lines.extend([
            f"[![Open in Colab]({badge('Open in Colab', 'F9AB00')})]({links['Colab']})",
            f"[![Launch Binder]({badge('Launch Binder', '579ACA')})]({links['Binder']})",
            f"[![Open in github.dev]({badge('Open in github.dev', '24292F')})]({links['github.dev']})",
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"
