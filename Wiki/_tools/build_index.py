#!/usr/bin/env python3
# build_index: lê frontmatter, agrupa por domínio/tipo
import os, re
domains = {}
for root, _, files in os.walk("Wiki"):
    for f in files:
        if f.endswith(".md") and f != "index.md":
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            m = re.search(r"domínio:\s*(\w+)", content)
            dom = m.group(1) if m else "meta"
            m2 = re.search(r"tipo:\s*(\w+)", content)
            typ = m2.group(1) if m2 else "nota"
            domains.setdefault(dom, {}).setdefault(typ, []).append(f)
with open("Wiki/index.md", "w") as out:
    out.write("# Índice\n")
    for dom in sorted(domains):
        out.write(f"\n## {dom}\n")
        for typ in sorted(domains[dom]):
            out.write(f"- {typ}: {', '.join(domains[dom][typ])}\n")
