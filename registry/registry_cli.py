#!/usr/bin/env python3
"""Hermes Skill Registry CLI — publish, search, install."""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def _api_post(url: str, data: dict) -> dict:
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def _api_get(url: str) -> dict:
    try:
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def cmd_publish(args):
    skill_dir = os.path.abspath(args.skill_dir)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        print(f"Error: {skill_md} not found", file=sys.stderr)
        sys.exit(1)

    with open(skill_md) as f:
        content = f.read()

    lines = content.split("\n")
    meta = {"name": os.path.basename(skill_dir), "version": "1.0.0", "description": "", "repo": ""}
    in_front = False
    for line in lines:
        if line.strip() == "---":
            in_front = not in_front
            continue
        if in_front and ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key == "name":
                meta["name"] = val
            elif key == "version":
                meta["version"] = val
            elif key == "description":
                meta["description"] = val
            elif key == "url":
                meta["repo"] = val

    if not meta["description"]:
        meta["description"] = content[:200].replace("\n", " ")

    registry_url = args.registry.rstrip("/")
    result = _api_post(f"{registry_url}/api/v1/publish", meta)
    print(f"Published: {result['name']} v{result['version']}")


def cmd_search(args):
    registry_url = args.registry.rstrip("/")
    result = _api_get(f"{registry_url}/api/v1/search?q={args.query}")
    for skill in result.get("results", []):
        desc = skill.get("description", "")[:60]
        print(f"  {skill['name']:20s} v{skill.get('version','?'):6s}  {desc}")
    print(f"\n{result['count']} skills found")


def cmd_install(args):
    registry_url = args.registry.rstrip("/")
    skill = _api_get(f"{registry_url}/api/v1/skills/{args.skill_name}")
    print(f"Skill: {skill['name']} v{skill.get('version','')}")
    print(f"Description: {skill.get('description','')[:100]}")
    print(f"Repo: {skill.get('repo','')}")
    print("To install: clone repo or copy SKILL.md to ~/.hermes/skills/<category>/")


def main():
    parser = argparse.ArgumentParser(description="Hermes Skill Registry CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # Publish
    p = sub.add_parser("publish", help="Publish a skill directory")
    p.add_argument("--registry", default="http://localhost:8888")
    p.add_argument("skill_dir", help="Path to skill directory with SKILL.md")

    s = sub.add_parser("search", help="Search skills by keyword")
    s.add_argument("--registry", default="http://localhost:8888")
    s.add_argument("query", help="Search keyword")

    i = sub.add_parser("install", help="Show install info for a skill")
    i.add_argument("--registry", default="http://localhost:8888")
    i.add_argument("skill_name", help="Skill name")

    args = parser.parse_args()
    handlers = {"publish": cmd_publish, "search": cmd_search, "install": cmd_install}
    handlers[args.command](args)


if __name__ == "__main__":
    main()
