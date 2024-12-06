import jax.numpy as jnp
import pydantic
import torch

import toolkit.array_types.numpy as tn

AsJax = pydantic.BeforeValidator(jnp.asarray)
AsNumpy = pydantic.BeforeValidator(tn.as_numpy)
AsTorch = pydantic.BeforeValidator(torch.as_tensor)
