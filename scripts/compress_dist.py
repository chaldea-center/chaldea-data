"""
CF runtime: python 3.7
"""
import json
from hashlib import md5
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent


def load_json(fp: Path) -> dict:
    return json.loads(fp.read_text())


def dump_json(data, fp=None) -> str:
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if fp:
        Path(fp).write_text(text)
    return text


def main():
    dist_dir = project_root / "dist"
    fp_version = dist_dir / "version.json"
    version = load_json(fp_version)
    for file_version in version["files"].values():
        old_ver = dict(file_version)
        fn: str = file_version["filename"]
        file = dist_dir / fn
        content = load_json(file)
        # compressed = orjson.dumps(content)
        compressed = dump_json(content).encode()
        size = len(compressed)
        hash_val = md5(compressed).hexdigest()[:6]
        print(f'{fn:20s}: {old_ver["hash"]}->{hash_val}, {old_ver["size"]}->{size}')
        file_version["size"] = size
        file_version["hash"] = hash_val
        file.write_bytes(compressed)

    version_content = json.dumps(version, indent=2, ensure_ascii=False)
    fp_version.write_text(version_content)
    print(version_content)


if __name__ == "__main__":
    main()
