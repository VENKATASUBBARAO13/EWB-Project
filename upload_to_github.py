#!/usr/bin/env python3
"""Upload this prepared EWB project bundle to an existing GitHub repository.

Set GITHUB_TOKEN in your local shell to a fine-grained token with Contents: Read and write
for the repository. The token is read from the environment and is never written to files.
"""
import os, sys, json, base64, urllib.request, urllib.error
from pathlib import Path

OWNER = os.environ.get("GITHUB_OWNER", "VENKATASUBBARAO13")
REPO = os.environ.get("GITHUB_REPO", "EWB-Project")
BRANCH = os.environ.get("GITHUB_BRANCH", "main")
TOKEN = os.environ.get("GITHUB_TOKEN")
ROOT = Path(__file__).resolve().parent
if not TOKEN:
    sys.exit("Set GITHUB_TOKEN in your terminal first. Never paste it into chat or commit it.")
BASE = f"https://api.github.com/repos/{OWNER}/{REPO}"

def api(method, url, data=None):
    raw = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=raw, method=method, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "EWB-VPC-Peering-Project-Uploader"
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            return json.loads(body.decode("utf-8")) if body else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:1500]
        raise RuntimeError(f"GitHub API {method} {url} failed: HTTP {e.code}: {detail}") from e

# Add the prepared assets; do not include the uploader itself.
files = []
for p in ROOT.rglob("*"):
    if not p.is_file() or p.name == Path(__file__).name:
        continue
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith(".git/") or rel.lower().endswith((".pem", ".key", ".p12")):
        continue
    files.append((rel, p))
files.sort(key=lambda v: v[0])
print(f"Uploading {len(files)} files to {OWNER}/{REPO} branch {BRANCH}...")
ref = api("GET", f"{BASE}/git/ref/heads/{BRANCH}")
parent = ref["object"]["sha"]
head_commit = api("GET", f"{BASE}/git/commits/{parent}")
base_tree = head_commit["tree"]["sha"]
tree_entries = []
for i, (rel, p) in enumerate(files, 1):
    payload = base64.b64encode(p.read_bytes()).decode("ascii")
    blob = api("POST", f"{BASE}/git/blobs", {"content": payload, "encoding": "base64"})
    tree_entries.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    print(f"[{i}/{len(files)}] staged {rel}")
new_tree = api("POST", f"{BASE}/git/trees", {"base_tree": base_tree, "tree": tree_entries})
new_commit = api("POST", f"{BASE}/git/commits", {
    "message": "Add AWS VPC peering architecture, report, and screenshot evidence",
    "tree": new_tree["sha"], "parents": [parent]
})
api("PATCH", f"{BASE}/git/refs/heads/{BRANCH}", {"sha": new_commit["sha"], "force": False})
print("Upload complete:", f"https://github.com/{OWNER}/{REPO}/commit/{new_commit['sha']}")
