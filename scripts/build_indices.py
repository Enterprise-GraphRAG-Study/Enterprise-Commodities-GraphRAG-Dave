"""Build JSON index artifacts from the enriched commodity graph dataset."""

from __future__ import annotations

import argparse
import sys
from importlib import import_module
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for index generation."""
    parser = argparse.ArgumentParser(description="Build retrieval-oriented JSON indices from the graph dataset.")
    parser.add_argument(
        "--input",
        default="ontology/model/phase1_enriched.yaml",
        help="Path to the graph YAML file to index.",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/index",
        help="Directory where generated index JSON files will be written.",
    )
    return parser.parse_args()


def main() -> int:
    """Load the graph dataset, build indices, and write them to disk."""
    args = parse_args()
    data_loader = import_module("src.data_loader")
    indexer = import_module("src.indexer")

    dataset = data_loader.load_local_graph_dataset(args.input)
    bundle = indexer.build_indices(dataset)
    indexer.write_index_bundle(bundle, args.output_dir)

    print(f"Wrote index artifacts to {args.output_dir}")
    print(f"Relationship count: {bundle.graph_summary['relationship_count']}")
    print(f"Indexed nodes: {len(bundle.node_index)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
