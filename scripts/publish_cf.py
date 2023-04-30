import shutil
import sys
from pathlib import Path

import compress_dist


def copy_functions():
    root = Path(__file__).parents[1]
    shutil.copy(root / "functions" / "_routes.json", root / "dist" / "_routes.json")
    shutil.copytree(root / "functions", root / "dist" / "functions")


if __name__ == "__main__":
    compress_dist.main()
    if "--function" in sys.argv[1:]:
        copy_functions()
