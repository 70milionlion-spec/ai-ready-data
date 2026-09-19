"""Input and output operations for analyzer."""

from pathlib import Path

import pandas as pd


def read_table(path):
    """Read a CSV table from *path*."""
    return pd.read_csv(path)


def write_table(data, path):
    """Write a table to CSV at *path*."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    data.to_csv(output_path, index=False)


def ensure_table(path, data):
    """Write *data* to *path* only when the CSV does not exist."""
    input_path = Path(path)
    if not input_path.exists():
        write_table(data, input_path)
