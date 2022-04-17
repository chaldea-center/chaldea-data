import json
from hashlib import md5
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent


def load_json(fp: Path) -> dict:
    return json.loads(fp.read_text())


def dump_json(data, fp: Path):
    json.dumps(data, ensure_ascii=False)


def main():
    dist_dir = project_root / "dist"
    fp_version = dist_dir / "version.json"
    version = load_json(fp_version)
    for key, file_version in version["files"].items():  # type: str, dict
        old_ver = dict(file_version)
        fn: str = file_version["filename"]
        file = dist_dir / fn
        content = load_json(file)
        compressed = json.dumps(content, ensure_ascii=False).encode()
        size = len(compressed)
        _md5 = md5()
        _md5.update(compressed)
        hash_val = _md5.hexdigest()[:6]
        print(f'{fn:20s}: {old_ver["hash"]}->{hash_val}, {old_ver["size"]}->{size}')
        file_version["size"] = size
        file_version["hash"] = hash_val
        file.write_bytes(compressed)

    version_content = json.dumps(version, indent=2, ensure_ascii=False)
    fp_version.write_text(version_content)
    print(version_content)


if __name__ == "__main__":
    main()
