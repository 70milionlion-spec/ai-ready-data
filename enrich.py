"""Backward-compatible entry point for the analyzer command-line interface."""

from src.analyzer.cli import enrich, main

__all__ = ["enrich", "main"]


if __name__ == "__main__":
  main()
