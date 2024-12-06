from __future__ import annotations

from typing import Any, TypeGuard

import numpy as np

import toolkit as tk
import toolkit.typing as tp


def is_numpy(obj: Any) -> TypeGuard[np.ndarray]:
    return tp.is_instance_named_partial(obj, "numpy.ndarray")


def as_numpy(obj: Any) -> np.ndarray:
    if tk.is_numpy(obj):
        return obj
    if tk.is_torch(obj):
        return obj.numpy(force=True)
    return np.asarray(obj)
