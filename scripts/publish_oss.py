import hashlib
import logging
import re
import subprocess
import sys
from argparse import ArgumentError
from pathlib import Path

import compress_dist

ossutil = "ossutil"


def _call_oss(*args) -> str:
    try:
        output = subprocess.check_output([ossutil, *args]).decode()
        print(output)
        return output
    except subprocess.CalledProcessError as e:
        logging.exception(
            f"CalledProcessError: {e}\nstderr:\n{e.stderr}\nstdout:\n{e.stdout}"
        )
        raise
    except Exception as e:
        logging.exception(f"Call ossutil failed: {e}")
        raise


def main(bucket_name: str, folder: Path, *args):
    folder = folder.resolve()
    list_result = _call_oss("ls", f"oss://{bucket_name}", *args)
    # return
    remote_etags: dict[str, str] = {}
    for match in re.findall(
        r"(?<=\n)(.{29})\s+(\d+)\s+(.+)\s+([0-9A-Z]{32})\s+(oss://.+)\n", list_result
    ):
        remote_etags[match[4][len(f"oss://{bucket_name}/") :]] = str(match[3]).upper()
    print(f"Found {len(remote_etags)} files at remote")

    uploaded, deleted, unchanged = 0, 0, 0
    for file in folder.glob("**/*.json"):
        if file.name.startswith(".") or file.name.startswith("_"):
            continue
        key = str(file.resolve().relative_to(folder))
        md5 = hashlib.md5(file.read_bytes()).hexdigest().upper()
        if md5 == remote_etags.pop(key, None):
            unchanged += 1
            continue
        print(f">>> Uploading {key} ...")
        _call_oss(
            "cp",
            str(file.absolute()),
            f"oss://{bucket_name}/{key}",
            "-f",
            *args,
        )
        uploaded += 1

    for key in remote_etags.keys():
        print(f">>> Deleting {key} ...")
        _call_oss("rm", f"oss://{bucket_name}/{key}", *args)
        deleted += 1

    print(
        f">>> Published to OSS: {uploaded} uploaded, {deleted} deleted, {unchanged} remain unchanged."
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ArgumentError(None, "must provide bucket name")
    compress_dist.main()
    main(sys.argv[1], compress_dist.project_root / "dist", *sys.argv[2:])
