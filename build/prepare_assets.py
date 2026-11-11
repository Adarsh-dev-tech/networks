"""Regenerate the image assets used by the annotated study guide.

Step 1: render every page of `Computer Architecture.pdf` to /tmp/ca/pages/pageNNN.png
        (200 dpi screenshots of the handwritten notes).
Step 2: write compressed /tmp/ca/embed/pageNNN.jpg and /tmp/ca/embed/caN.jpg
        (the JPEGs actually embedded in the PDF).

Run:  python3 prepare_assets.py
"""
import os, sys
import pymupdf
from PIL import Image

REPO = "/workspace/project/networks"
PAGES = "/tmp/ca/pages"
EMBED = "/tmp/ca/embed"


def render_notes():
    os.makedirs(PAGES, exist_ok=True)
    d = pymupdf.open(os.path.join(REPO, "Computer Architecture.pdf"))
    for i in range(d.page_count):
        pix = d[i].get_pixmap(dpi=200)
        pix.save(os.path.join(PAGES, f"page{i+1:03d}.png"))
    print("rendered", d.page_count, "notes pages ->", PAGES)


def make_embeds():
    os.makedirs(EMBED, exist_ok=True)
    for i in range(1, 88):
        im = Image.open(os.path.join(PAGES, f"page{i:03d}.png")).convert("RGB")
        im.save(os.path.join(EMBED, f"page{i:03d}.jpg"), "JPEG", quality=82, optimize=True)
    for i in range(1, 42):
        im = Image.open(os.path.join(REPO, f"ca{i}.png")).convert("RGB")
        im.save(os.path.join(EMBED, f"ca{i}.jpg"), "JPEG", quality=80, optimize=True)
    print("wrote embeds ->", EMBED)


if __name__ == "__main__":
    render_notes()
    make_embeds()
