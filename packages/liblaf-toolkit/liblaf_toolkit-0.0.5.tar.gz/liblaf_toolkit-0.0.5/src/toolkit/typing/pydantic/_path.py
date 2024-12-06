from pathlib import Path
from typing import Annotated

import pydantic


def mkdir(x: Path) -> Path:
    x.mkdir(parents=True, exist_ok=True)
    return x


def parent_mkdir(x: Path) -> Path:
    x.parent.mkdir(parents=True, exist_ok=True)
    return x


SaveDirPath = Annotated[Path, pydantic.AfterValidator(mkdir)]
SaveFilePath = Annotated[Path, pydantic.AfterValidator(parent_mkdir)]
