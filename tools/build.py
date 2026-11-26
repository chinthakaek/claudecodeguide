"""Build index.html from Claude_Code_Guide.md.

Usage:  python3 tools/build.py Claude_Code_Guide.md index.html
Needs:  pip install markdown
"""
import re, sys, html, datetime, pathlib, markdown
from markdown.extensions.toc import TocExtension

src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()

def gh_slug(value, separator="-"):
    # Mimic GitHub anchor slugs so the guide's internal links keep working
    value = value.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return value.replace(" ", "-")

# Drop the hand-written Markdown TOC; the HTML gets a sidebar instead
text = re.sub(r"## Table of Contents\n.*?\n---\n", "", text, count=1, flags=re.S)


# GitHub renders a list right after a paragraph; Python-Markdown needs a blank line first
def add_list_gaps(t):
    out, in_code, prev = [], False, ""
    for line in t.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        is_item = re.match(r"(- |\d+\. )", line)
        prev_item = re.match(r"\s*(- |\d+\. )", prev)
        if not in_code and is_item and prev.strip() and not prev_item and not prev.startswith("```"):
            out.append("")
        out.append(line); prev = line
    return "\n".join(out)
text = add_list_gaps(text)

md = markdown.Markdown(extensions=[
    "tables", "fenced_code", "sane_lists",
    TocExtension(slugify=gh_slug, toc_depth="2-3"),
])
body = md.convert(text)

# Sidebar nav from h2/h3 tokens
def nav(tokens):
    out = ["<ul>"]
    for t in tokens:
        if t["name"] == "Table of Contents":
            continue
        out.append(f'<li><a href="#{t["id"]}">{t["name"]}</a>')
        if t["children"] and t["level"] == 1 or t["level"] == 2 and t["children"]:
            out.append(nav(t["children"]))
        out.append("</li>")
    out.append("</ul>")
    return "".join(out)

tokens = md.toc_tokens
# top-level token is the h1; use its children (h2s)
h2s = tokens[0]["children"] if tokens and tokens[0]["level"] == 1 else tokens
def nav2(items, depth=0):
    s = '<ul>'
    for t in items:
        s += f'<li class="d{depth}"><a href="#{t["id"]}">{t["name"]}</a>'
        if depth == 0 and t["children"] and t["name"][:3] in ("8. ", "10.", "11."):
            s += nav2(t["children"], 1)
        s += '</li>'
    return s + '</ul>'
sidebar = nav2(h2s)

title = "Claude Code: A Beginner's Guide and Best Practices"
page = open(pathlib.Path(__file__).with_name("template.html"), encoding="utf-8").read()
page = page.replace("{{TITLE}}", html.escape(title)).replace("{{NAV}}", sidebar).replace("{{BODY}}", body).replace("{{UPDATED}}", datetime.date.today().strftime("%d %B %Y"))
open(dst, "w", encoding="utf-8").write(page)
print("wrote", dst)
