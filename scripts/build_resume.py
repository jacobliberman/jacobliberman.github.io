#!/usr/bin/env python3
"""Build root index.html from resume/resume.json and resume/shell.template.html."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "resume" / "resume.json"
SHELL_PATH = ROOT / "resume" / "shell.template.html"
INDEX_PATH = ROOT / "index.html"

# Indentation inside `<div class="wrap">` (matches prior hand-written index.html).
I6 = "      "
I8 = "        "
I10 = "          "
I12 = "            "


def e(s: str) -> str:
    return html.escape(s, quote=True)


def require(d: dict[str, Any], key: str) -> Any:
    if key not in d:
        raise SystemExit(f"resume.json missing required key: {key!r}")
    return d[key]


def render_contact_line(parts: list[dict[str, Any]]) -> str:
    bits: list[str] = []
    for i, part in enumerate(parts):
        if i:
            bits.append('<span class="contact-sep" aria-hidden="true"> · </span>')
        ptype = part.get("type")
        if ptype == "text":
            bits.append(f'<span class="contact-plain">{e(str(part["value"]))}</span>')
        elif ptype == "link":
            href = e(str(part["href"]))
            label = e(str(part["label"]))
            bits.append(
                f'<a href="{href}" rel="noopener noreferrer">{label}</a>'
            )
        else:
            raise SystemExit(f"contact part has unknown type: {ptype!r}")
    inner = "".join(bits)
    return f'{I8}<p class="contact">\n{I10}{inner}\n{I8}</p>'


def render_nav(items: list[dict[str, Any]]) -> str:
    lis = []
    for item in items:
        hid = e(str(item["id"]))
        label = e(str(item["label"]))
        lis.append(f"{I10}<li><a href=\"#{hid}\">{label}</a></li>")
    return (
        f'{I6}<nav class="toc" aria-label="On this page">\n'
        f"{I8}<ul>\n"
        + "\n".join(lis)
        + f"\n{I8}</ul>\n"
        f"{I6}</nav>"
    )


def render_about(block: dict[str, Any]) -> str:
    heading = e(str(block["heading"]))
    hid = "about-heading"
    paras = []
    for p in block["paragraphs"]:
        cls = p.get("class", "lead")
        style = p.get("style")
        style_attr = f' style="{e(style)}"' if style else ""
        paras.append(
            f'{I10}<p class="{e(cls)}"{style_attr}>{e(str(p["text"]))}</p>'
        )
    return (
        f'{I8}<section id="about" aria-labelledby="{hid}">\n'
        f'{I10}<h2 id="{hid}">{heading}</h2>\n'
        + "\n".join(paras)
        + f"\n{I8}</section>"
    )


def render_experience(block: dict[str, Any]) -> str:
    hid = "experience-heading"
    h2 = e(str(block["heading"]))
    articles = []
    for role in block["roles"]:
        title = e(str(role["title"]))
        meta = e(str(role["meta"]))
        lis = "\n".join(
            f"{I12}<li>{e(str(b))}</li>" for b in role["bullets"]
        )
        articles.append(
            f'{I10}<article class="card">\n'
            f"{I12}<h3>{title}</h3>\n"
            f'{I12}<p class="meta">{meta}</p>\n'
            f"{I12}<ul>\n{lis}\n{I12}</ul>\n"
            f"{I10}</article>"
        )
    return (
        f'{I8}<section id="experience" aria-labelledby="{hid}">\n'
        f'{I10}<h2 id="{hid}">{h2}</h2>\n\n'
        + "\n\n".join(articles)
        + f"\n{I8}</section>"
    )


def render_skills(block: dict[str, Any]) -> str:
    hid = "skills-heading"
    h2 = e(str(block["heading"]))
    pills = "\n".join(
        f'{I12}<span class="skill-pill" role="listitem">{e(p)}</span>'
        for p in block["pills"]
    )
    return (
        f'{I8}<section id="skills" aria-labelledby="{hid}">\n'
        f'{I10}<h2 id="{hid}">{h2}</h2>\n'
        f'{I10}<div class="skills" role="list">\n{pills}\n'
        f"{I10}</div>\n"
        f"{I8}</section>"
    )


def render_projects(block: dict[str, Any]) -> str:
    hid = "projects-heading"
    h2 = e(str(block["heading"]))
    cards = []
    for item in block["items"]:
        title = e(str(item["title"]))
        desc = e(str(item["description"]))
        cards.append(
            f'{I10}<article class="card">\n'
            f"{I12}<h3>{title}</h3>\n"
            f"{I12}<p>{desc}</p>\n"
            f"{I10}</article>"
        )
    return (
        f'{I8}<section id="projects" aria-labelledby="{hid}">\n'
        f'{I10}<h2 id="{hid}">{h2}</h2>\n\n'
        + "\n\n".join(cards)
        + f"\n{I8}</section>"
    )


def render_education(block: dict[str, Any]) -> str:
    hid = "education-heading"
    h2 = e(str(block["heading"]))
    cards = []
    for item in block["items"]:
        title = e(str(item["title"]))
        meta = e(str(item["meta"]))
        cards.append(
            f'{I10}<article class="card">\n'
            f"{I12}<h3>{title}</h3>\n"
            f'{I12}<p class="meta">{meta}</p>\n'
            f"{I10}</article>"
        )
    return (
        f'{I8}<section id="education" aria-labelledby="{hid}">\n'
        f'{I10}<h2 id="{hid}">{h2}</h2>\n\n'
        + "\n".join(cards)
        + f"\n{I8}</section>"
    )


def build_wrap(data: dict[str, Any]) -> str:
    header = require(data, "header")
    contact = require(data, "contact")
    nav = require(data, "nav")
    about = require(data, "about")
    experience = require(data, "experience")
    skills = require(data, "skills")
    projects = require(data, "projects")
    education = require(data, "education")
    footer = require(data, "footer")

    eyebrow = e(str(header["eyebrow"]))
    name = e(str(header["name"]))
    tagline = e(str(header["tagline"]))

    header_html = (
        f'{I6}<header class="site-header">\n'
        f'{I8}<p class="eyebrow">{eyebrow}</p>\n'
        f"{I8}<h1>{name}</h1>\n"
        f'{I8}<p class="tagline">{tagline}</p>\n'
        f"{render_contact_line(contact)}\n"
        f"{I6}</header>"
    )

    main_inner = "\n\n".join(
        [
            render_about(about),
            render_experience(experience),
            render_skills(skills),
            render_projects(projects),
            render_education(education),
        ]
    )

    main_html = f'{I6}<main id="main">\n{main_inner}\n{I6}</main>'

    cname = e(str(footer["copyrightName"]))
    site_url = e(str(footer["siteUrl"]))
    site_label = e(str(footer["siteLabel"]))

    footer_html = (
        f'{I6}<footer class="site-footer">\n'
        f"{I8}<p>\n"
        f'{I10}© <span id="year"></span> {cname} ·\n'
        f'{I10}<a href="{site_url}">{site_label}</a>\n'
        f"{I8}</p>\n"
        f"{I6}</footer>"
    )

    return "\n\n".join([header_html, render_nav(nav), main_html, footer_html])


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    site = require(data, "site")
    title = e(str(site["title"]))
    description = e(str(site["description"]))
    wrap = build_wrap(data)

    shell = SHELL_PATH.read_text(encoding="utf-8")
    for token, value in (
        ("{{TITLE}}", title),
        ("{{DESCRIPTION}}", description),
        ("{{WRAP}}", wrap),
    ):
        if token not in shell:
            raise SystemExit(f"resume/shell.template.html must contain {token}")
        shell = shell.replace(token, value)

    INDEX_PATH.write_text(shell, encoding="utf-8", newline="\n")
    print(f"Wrote {INDEX_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
