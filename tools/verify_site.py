"""Check a real Unity WebGL output before uploading it to Pages.

This checks packaging only. Browser gameplay QA is a separate required step.
"""
from pathlib import Path
import json
import re
import sys


def verify(folder):
    root = Path(folder).resolve(strict=True)
    assert (root / "index.html").is_file(), "Missing index.html"
    assert (root / "Build").is_dir(), "Missing Build directory"
    files = [p for p in root.rglob("*") if p.is_file()]
    assert not any(p.is_symlink() for p in root.rglob("*")), "Unexpected symlink"
    total = sum(p.stat().st_size for p in files)
    assert total <= 1_000_000_000, "Published site exceeds the GitHub Pages 1 GB limit"
    build = root / "Build"
    for pattern in ("*.loader.js", "*.data*", "*.wasm*", "*.framework.js*"):
        assert list(build.glob(pattern)), "Missing Unity output: " + pattern
    names = [str(p.relative_to(root)) for p in files]
    assert len({p.casefold() for p in names}) == len(names), "Case-insensitive filename collision"
    html = (root / "index.html").read_text(encoding="utf-8")
    for target in re.findall(r'(?:src|href)=["\']([^"\']+)', html):
        if target.startswith(("https:", "http:", "data:", "#", "//")):
            continue
        assert not target.startswith("/"), "Absolute asset URL breaks the repository subpath: " + target
        path = target.split("?", 1)[0].split("#", 1)[0]
        assert (root / path).is_file(), "Missing or incorrectly cased asset: " + target
    assert not any(p.name in (".DS_Store", "UnityLicense.ulf") for p in files), "Unexpected local metadata"
    return {"files": len(files), "bytes": total, "largestFileBytes": max(p.stat().st_size for p in files)}


if __name__ == "__main__":
    print(json.dumps(verify(sys.argv[1]), indent=2))
