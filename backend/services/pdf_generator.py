import subprocess
import re
from pathlib import Path
from uuid import uuid4
from shutil import copyfile
from jinja2 import Environment, FileSystemLoader, pass_context

# Jinja2 environment setup
env = Environment(
    loader=FileSystemLoader("backend/templates"),
    block_start_string="{%",
    block_end_string="%}",
    variable_start_string="{{",
    variable_end_string="}}",
    comment_start_string="{#",
    comment_end_string="#}"
)

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

def recursively_escape(obj):
    if isinstance(obj, dict):
        return {k: recursively_escape(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursively_escape(i) for i in obj]
    elif isinstance(obj, str):
        return latex_escape({}, obj)
    return obj

def generate_pdf(data: dict) -> str:
    # print("📦 Input data:", data)

    # Extract and remove template name
    template_name = data.pop("templateName", "resume")
    template = env.get_template(f"{template_name}.tex.j2")

    # Extract the contact entry and promote it to a top-level field
    entries = data.get("entries", [])
    contact_entry = next((e for e in entries if e.get("__typename") == "ContactEntry"), None)
    data["contact"] = contact_entry

    # Escape LaTeX special characters
    escaped_data = recursively_escape(data)

    # Render LaTeX
    rendered_tex = template.render(escaped_data)

    # Prepare output file paths
    uid = uuid4().hex
    output_dir = Path("/tmp")
    tex_file = output_dir / f"{uid}.tex"
    pdf_file = tex_file.with_suffix(".pdf")

    # Save rendered .tex
    with open(tex_file, "w") as f:
        f.write(rendered_tex)

    # Copy class file if needed
    cls_path = Path("backend/templates") / "my-resume.cls"
    if cls_path.exists():
        copyfile(cls_path, output_dir / "my-resume.cls")

    try:
        print(f"🧪 Running pdflatex on {tex_file.name}...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file.name],
            check=True,
            cwd=output_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("✅ PDF generated successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ PDF generation failed!")
        print("\n--- Rendered LaTeX ---\n")
        print(rendered_tex)
        print("\n--- STDOUT ---\n")
        print(e.stdout.decode())
        print("\n--- STDERR ---\n")
        print(e.stderr.decode())
        raise

    return str(pdf_file)
