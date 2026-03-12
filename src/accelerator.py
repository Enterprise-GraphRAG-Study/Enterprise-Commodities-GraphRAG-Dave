"""Hardware acceleration helpers for PyTorch-backed workloads."""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class AcceleratorInfo:
    """Describes the preferred PyTorch execution device."""

    device: str
    backend: str
    torch_version: str
    cuda_version: str | None
    device_name: str | None


def detect_accelerator() -> AcceleratorInfo:
    """Return the best available accelerator in priority order CUDA -> MPS -> CPU."""
    if torch.cuda.is_available():
        return AcceleratorInfo(
            device="cuda",
            backend="cuda",
            torch_version=torch.__version__,
            cuda_version=torch.version.cuda,
            device_name=torch.cuda.get_device_name(0),
        )

    mps_backend = getattr(torch.backends, "mps", None)
    if mps_backend is not None and mps_backend.is_available():
        return AcceleratorInfo(
            device="mps",
            backend="mps",
            torch_version=torch.__version__,
            cuda_version=torch.version.cuda,
            device_name="Apple Metal Performance Shaders",
        )

    return AcceleratorInfo(
        device="cpu",
        backend="cpu",
        torch_version=torch.__version__,
        cuda_version=torch.version.cuda,
        device_name=None,
    )


def resolve_device(preferred: str | None = None) -> torch.device:
    """Resolve a concrete PyTorch device, honoring an explicit preference when possible."""
    if preferred is not None:
        candidate = preferred.lower()
        if candidate == "cuda" and torch.cuda.is_available():
            return torch.device("cuda")
        if candidate == "mps":
            mps_backend = getattr(torch.backends, "mps", None)
            if mps_backend is not None and mps_backend.is_available():
                return torch.device("mps")
        if candidate == "cpu":
            return torch.device("cpu")

    return torch.device(detect_accelerator().device)
