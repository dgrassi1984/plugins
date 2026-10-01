#!/usr/bin/env python3
"""Fail if pstack skills still depend on Cursor-only runtime bindings."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN = (
    "subagent_type",
    "cursor-team-kit",
    "control-ui",
    "control-cli",
    "/deslop",
    "/loop",
    "~/.cursor",
    ".cursor/skills",
    ".cursor/rules",
    "agent-transcripts",
    "Cursor cloud",
    "cloud-sleeper",
    "alwaysApply",
    "AskQuestion",
    "environment: \"cloud\"",
    "environment: 'cloud'",
)

problems = []
seen = set()
for path in sorted(SKILLS.glob("*/SKILL.md")):
    text = path.read_text()
    name = path.parent.name
    seen.add(name)
    if not text.startswith("---\n"):
        problems.append(f"{name}: missing frontmatter")
        continue
    end = text.find("\n---", 3)
    if end < 0:
        problems.append(f"{name}: unclosed frontmatter")
        continue
    fm = text[4:end]
    body = text[end + 4 :]
    declared = None
    for line in fm.splitlines():
        if line.startswith("name:"):
            declared = line.split(":", 1)[1].strip().strip('"').strip("'")
    if declared != name or not NAME.match(name):
        problems.append(f"{name}: name is {declared!r}")
    if "description:" not in fm:
        problems.append(f"{name}: missing description")
    if name != "bro" and "disable-model-invocation" in fm:
        problems.append(f"{name}: disable-model-invocation blocks skill-tool routing")
    if name == "bro" and "disable-model-invocation: true" not in fm:
        problems.append("bro: expected user-only invocation")
    if name != "pstack-runtime":
        haystack = fm + "\n" + body
        for token in FORBIDDEN:
            if token in haystack:
                problems.append(f"{name}: still contains {token}")

for path in sorted(SKILLS.rglob("*")):
    if not path.is_file() or path.suffix not in {".md", ".sh"}:
        continue
    if "pstack-runtime" in path.parts:
        continue
    if path.name == "SKILL.md" and path.parent.parent == SKILLS:
        continue
    text = path.read_text(errors="replace")
    rel = path.relative_to(SKILLS)
    for token in FORBIDDEN:
        if token in text:
            problems.append(f"{rel}: still contains {token}")

required = {"poteto-mode", "pstack-runtime", "comment-sicko", "poteto-agent", "setup-pstack", "bro"}
missing = sorted(required - seen)
if missing:
    problems.append("missing skills: " + ", ".join(missing))

if problems:
    print(f"{len(problems)} problem(s):")
    for item in problems:
        print(" -", item)
    sys.exit(1)
print(f"ok: {len(seen)} skills")
