"""
CF Python default version: 3.11.4
"""
import shutil
from pathlib import Path

import compress_dist


def copy_cf():
    root = Path(__file__).parents[1]
    shutil.copytree(root / "cf", root / "dist", dirs_exist_ok=True)


if __name__ == "__main__":
    compress_dist.main()
    copy_cf()
