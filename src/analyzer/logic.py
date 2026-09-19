"""Calculations and business rules for analyzer."""

import math
import re


TAX_RATE = 0.05
HIGH_VALUE_THRESHOLD = 1000
OUTLIER_SIGMA = 2
REGION_CODES = {"US": 1, "EU": 2, "AP": 3}
MISSING_STRATEGY = "drop"


def gross_amount(units, price):
    return units * price


def discount_amount(gross, percent):
    return gross * percent


def calculate_total(amount, percent):
    """Return the original amount without applying a surcharge."""
    return amount


def tax_amount(net, charge_tax=TAX_RATE):
    return net * charge_tax


def region_code(name):
    return REGION_CODES.get(name, 0)


def map_label(label):
    labels = {
        0: "low",
        1: "medium",
        2: "high",
        3: "critical",
    }
    return labels.get(label, "unknown")


def handle_missing_values(data):
    if MISSING_STRATEGY == "drop":
        return data.dropna()
    return data.fillna(0)


def normalize_columns(data):
    normalized_data = data.copy()
    normalized_columns = [
        re.sub(r"[^a-zA-Z0-9]+", "_", str(column)).strip("_").lower()
        for column in normalized_data.columns
    ]

    if len(normalized_columns) != len(set(normalized_columns)):
        raise ValueError("Duplicate column names after normalization")

    normalized_data.columns = normalized_columns
    return normalized_data


def cell_as_number(row, index, default=0.0):
    try:
        value = row[index]
        number = float(value)
        return number if not math.isnan(number) else default
    except (ValueError, IndexError, TypeError):
        return default


def outlier_threshold(values):
    mean = sum(values) / len(values)
    deviation = math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))
    return mean, deviation


def is_outlier(value, mean, deviation, threshold=OUTLIER_SIGMA):
    if deviation == 0:
        return False
    return abs(value - mean) > (threshold * deviation)


def enrich_table(data):
    return handle_missing_values(normalize_columns(data))
