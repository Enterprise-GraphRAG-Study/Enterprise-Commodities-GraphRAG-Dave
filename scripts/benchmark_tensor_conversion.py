"""Benchmark simple PyTorch tensor conversion paths and emit an SVG chart."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from collections.abc import Callable
from importlib import import_module
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the benchmark runner."""
    parser = argparse.ArgumentParser(description="Benchmark PyTorch tensor conversion paths.")
    parser.add_argument("--elements", type=int, default=1_000_000, help="Number of float elements per trial.")
    parser.add_argument("--iterations", type=int, default=20, help="Number of timed iterations per benchmark path.")
    parser.add_argument(
        "--output-json",
        default="docs/assets/tensor_conversion_benchmark.json",
        help="Path to write the benchmark summary JSON.",
    )
    parser.add_argument(
        "--output-svg",
        default="docs/assets/tensor_conversion_benchmark.svg",
        help="Path to write the benchmark chart SVG.",
    )
    return parser.parse_args()


def benchmark_operation(operation: Callable[[], torch.Tensor], iterations: int, backend: str) -> float:
    """Return the median runtime in milliseconds for a tensor-producing operation."""
    samples_ms: list[float] = []
    for _ in range(iterations):
        if backend == "cuda":
            torch.cuda.synchronize()
        start = time.perf_counter()
        tensor = operation()
        if backend == "cuda":
            torch.cuda.synchronize()
        end = time.perf_counter()
        # Use the tensor so the operation is not trivially discarded.
        _ = tensor.shape
        samples_ms.append((end - start) * 1000.0)

    return statistics.median(samples_ms)


def build_svg(title: str, subtitle: str, labels: list[str], values: list[float]) -> str:
    """Build a compact SVG bar chart without external plotting dependencies."""
    width = 900
    height = 420
    chart_left = 250
    chart_right = 820
    chart_top = 90
    row_height = 90
    bar_height = 30
    max_value = max(values) if values else 1.0
    scale = (chart_right - chart_left) / max_value if max_value else 1.0

    bars: list[str] = []
    for index, (label, value) in enumerate(zip(labels, values, strict=True)):
        y = chart_top + index * row_height
        bar_width = max(1.0, value * scale)
        bars.append(
            f"<text x='40' y='{y + 20}' font-size='18' fill='#14213d'>{label}</text>"
            f"<rect x='{chart_left}' y='{y}' width='{bar_width:.1f}' height='{bar_height}' rx='6' fill='#1d3557' />"
            f"<text x='{chart_left + bar_width + 12:.1f}' y='{y + 21}' "
            f"font-size='18' fill='#14213d'>{value:.2f} ms</text>"
        )

    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"
        "<rect width='100%' height='100%' fill='#f7f3e9' />"
        f"<text x='40' y='48' font-size='28' font-weight='700' fill='#14213d'>{title}</text>"
        f"<text x='40' y='74' font-size='16' fill='#4a5568'>{subtitle}</text>"
        f"{''.join(bars)}"
        "</svg>"
    )


def ensure_parent(path: Path) -> None:
    """Create parent directories for a target output path."""
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    """Run tensor conversion benchmarks and persist summary artifacts."""
    args = parse_args()
    detect_accelerator = import_module("src.accelerator").detect_accelerator
    accelerator = detect_accelerator()
    python_values = [float(index % 1024) / 1024.0 for index in range(args.elements)]

    results: list[dict[str, float | str]] = []
    cpu_median = benchmark_operation(
        lambda: torch.tensor(python_values, dtype=torch.float32, device="cpu"),
        iterations=args.iterations,
        backend="cpu",
    )
    results.append({"label": "Python list -> CPU tensor", "median_ms": cpu_median})

    if accelerator.backend == "cuda":
        direct_cuda = benchmark_operation(
            lambda: torch.tensor(python_values, dtype=torch.float32, device="cuda"),
            iterations=args.iterations,
            backend="cuda",
        )
        cpu_then_cuda = benchmark_operation(
            lambda: torch.tensor(python_values, dtype=torch.float32, device="cpu").to("cuda"),
            iterations=args.iterations,
            backend="cuda",
        )
        results.append({"label": "Python list -> CUDA tensor", "median_ms": direct_cuda})
        results.append({"label": "Python list -> CPU tensor -> CUDA", "median_ms": cpu_then_cuda})

    summary = {
        "elements": args.elements,
        "iterations": args.iterations,
        "accelerator": accelerator.__dict__,
        "results": results,
    }

    output_json = Path(args.output_json)
    output_svg = Path(args.output_svg)
    ensure_parent(output_json)
    ensure_parent(output_svg)
    output_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    labels = [str(item["label"]) for item in results]
    values = [float(item["median_ms"]) for item in results]
    subtitle = (
        f"{accelerator.device_name or 'CPU only'} | torch {accelerator.torch_version} | "
        f"{args.elements:,} float32 values | median of {args.iterations} runs"
    )
    output_svg.write_text(
        build_svg("PyTorch Tensor Conversion Benchmark", subtitle, labels, values),
        encoding="utf-8",
    )

    print(f"Wrote benchmark JSON to {output_json}")
    print(f"Wrote benchmark SVG to {output_svg}")
    for result in results:
        print(f"{result['label']}: {result['median_ms']:.2f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
