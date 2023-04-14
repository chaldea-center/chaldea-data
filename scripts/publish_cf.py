import shutil
from pathlib import Path

import compress_dist


def copy_functions():
    root = Path(__file__).parents[1]
    shutil.copytree(root / "functions", root / "dist" / "functions")


if __name__ == "__main__":
    compress_dist.main()
    copy_functions()
