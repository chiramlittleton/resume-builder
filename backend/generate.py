import subprocess
from jinja2 import Environment, FileSystemLoader
from uuid import uuid4
from pathlib import Path

env = Environment(loader=FileSystemLoader("templates"))

def generate_pdf(data: dict) -> str:
    template = env.get_template("resume.tex.j2")
    rendered = template.render(data)

    # Save .tex and .pdf to /tmp
    uid = uuid4().hex
    tex_file = Path(f"/tmp/{uid}.tex")
    pdf_file = tex_file.with_suffix(".pdf")

    with open(tex_file, "w") as f:
        f.write(rendered)

    try:
        subprocess.run(
            ["pdflatex", "-output-directory", "/tmp", str(tex_file)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print("LaTeX compilation failed!")
        with open(tex_file, "r") as f:
            print("--- Rendered LaTeX ---")
            print(f.read())
        raise

    return str(pdf_file)
