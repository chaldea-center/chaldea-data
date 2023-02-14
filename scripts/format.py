import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]

error_count = 0
success_count = 0


def check(folder: Path):
    global error_count, success_count
    for file in folder.glob("**/*.json"):
        try:
            json.loads(file.read_text())
            success_count += 1
        except json.decoder.JSONDecodeError as e:
            error_count += 1
            print(f"[\033[31merror\033[m] {file.relative_to(root)}: {e}")
            lines = e.doc.splitlines()
            for lineno in range(max(0, e.lineno - 2), min(len(lines), e.lineno + 3)):
                print(f'\033[31m{str(lineno+1)+":":<6s}{lines[lineno]}\033[m')


def main():
    check(root / "mappings")
    check(root / "wiki")
    if error_count:
        print(f"{error_count} file(s) format check failed")
        exit(1)
    print(f"{success_count} file(s) format check success")


if __name__ == "__main__":
    main()
