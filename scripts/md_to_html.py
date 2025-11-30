import markdown
import sys
from pathlib import Path

def md_to_html(md_path, out_path=None):
    md_path = Path(md_path)
    text = md_path.read_text()
    html = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    if out_path is None:
        out_path = md_path.with_suffix(".html")
    Path(out_path).write_text(html)
    print(f"[OK] Exported: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <file.md> [output.html]")
        sys.exit(1)
    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    md_to_html(md_path, out_path)
