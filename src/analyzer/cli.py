"""Command-line interface for analyzer."""

import argparse

from .io import ensure_table, read_table, write_table
from .logic import enrich_table


DEFAULT_INPUT_PATH = "data/raw/sales_sample.csv"
DEFAULT_OUTPUT_PATH = "output/enriched.csv"


def enrich(input_path=DEFAULT_INPUT_PATH, output_path=DEFAULT_OUTPUT_PATH):
    ensure_table(
        input_path,
        {"units": [10], "price": [100], "discount": [0.1], "region": ["US"]},
    )

    data = enrich_table(read_table(input_path))
    write_table(data, output_path)
    print(f"Enriched data successfully saved to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()
    enrich(args.input, args.output)


if __name__ == "__main__":
    main()
