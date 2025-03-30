import subprocess
import re
from pathlib import Path
from uuid import uuid4
from shutil import copyfile
from jinja2 import Environment, FileSystemLoader, pass_context

# Jinja2 environment setup
env = Environment(loader=FileSystemLoader("backend/templates"))

# LaTeX escape map for special characters
LATEX_ESCAPE_MAP = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}',
    '\\': r'\textbackslash{}',
}

@pass_context
def latex_escape(ctx, value):
    return re.sub(r'([&%$#_{}~^\\])', lambda m: LATEX_ESCAPE_MAP[m.group()], str(value))

env.filters['latex_escape'] = latex_escape

def generate_pdf(data: dict) -> str:
    # Extract and remove template name
    template_name = data.pop("template_name", "resume")
    template = env.get_template(f"{template_name}.tex.j2")

    # Render LaTeX using Jinja2
    rendered_tex = template.render(data)

    # Prepare output file paths
    uid = uuid4().hex
    output_dir = Path(".")
    tex_file = output_dir / f"{uid}.tex"
    pdf_file = tex_file.with_suffix(".pdf")

    # Save .tex file
    with open(tex_file, "w") as f:
        f.write(rendered_tex)

    # Copy class file if used
    cls_path = Path("templates") / "my-resume.cls"
    if cls_path.exists():
        copyfile(cls_path, output_dir / "my-resume.cls")

    try:
        print(f"🧪 Running pdflatex on {tex_file.name}...")
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", str(tex_file.name)],
            check=True,
            cwd=output_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("✅ pdflatex finished successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ LaTeX compilation failed!")
        print("\n--- Rendered LaTeX ---\n")
        print(rendered_tex)
        print("\n--- STDOUT ---\n")
        print(e.stdout.decode())
        print("\n--- STDERR ---\n")
        print(e.stderr.decode())
        raise

    return str(pdf_file)
