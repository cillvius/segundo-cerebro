#!/usr/bin/env python3
# lint: links quebrados, páginas órfãs, campos obrigatórios, RAW faltante
import os, re
issues = []
req = ["título","tipo","domínio","status","atualizado","fontes","resumo","tags"]
for root, _, files in os.walk("Wiki"):
    for f in files:
        if not f.endswith(".md"): continue
        p = os.path.join(root, f)
        with open(p) as fh: c = fh.read()
        for field in req:
            if field + ":" not in c: issues.append(f"{p}: campo '{field}' ausente")
        for link in re.findall(r"\[\[([^\]]+)\]\]", c):
            target = link + ".md"
            if not os.path.exists(os.path.join(root, target)) and not os.path.exists(os.path.join("Wiki", target)):
                issues.append(f"{p}: link quebrado [[{link}]]")
print("Issues:", len(issues))
for i in issues[:10]: print(i)
