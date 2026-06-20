#!/usr/bin/env python3
"""
Hermes Skill Registry — FastAPI server.

Quick start:
    pip install fastapi uvicorn pyyaml
    nohup uvicorn registry:app --host 0.0.0.0 --port 8888 &
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Hermes Skill Registry", version="1.0.0")

SKILLS_DIR = Path(os.environ.get("REGISTRY_DIR", "./registry_skills"))
SKILLS_DIR.mkdir(exist_ok=True)
INDEX_FILE = SKILLS_DIR / "index.json"

if INDEX_FILE.exists():
    with open(INDEX_FILE) as f:
        index = json.load(f)
else:
    index = {}
    INDEX_FILE.write_text("{}")


class SkillMeta(BaseModel):
    name: str
    version: str
    description: str
    author: str = ""
    repo: str = ""
    category: str = "community"


def _save_index():
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


@app.get("/api/v1/search")
def search(q: str = ""):
    results = []
    for name, meta in index.items():
        ql = q.lower()
        if not q or ql in name.lower() or ql in meta.get("description", "").lower():
            results.append({"name": name, **meta})
    return {"results": results, "count": len(results)}


@app.post("/api/v1/publish")
def publish(meta: SkillMeta):
    if meta.name in index:
        raise HTTPException(409, f"Skill '{meta.name}' already exists")
    index[meta.name] = meta.dict()
    index[meta.name]["published_at"] = datetime.utcnow().isoformat()
    _save_index()
    return {"status": "published", "name": meta.name, "version": meta.version}


@app.get("/api/v1/skills/{name}")
def get_skill(name: str):
    if name not in index:
        raise HTTPException(404, f"Skill '{name}' not found")
    return {"name": name, **index[name]}


@app.get("/api/v1/skills")
def list_skills():
    return {"skills": index, "count": len(index)}
