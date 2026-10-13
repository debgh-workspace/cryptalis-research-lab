"""Deterministic analysis of the retained A/A receipt; never runs admissions."""
import argparse
import hashlib
import json
import statistics
from pathlib import Path


def analyze(receipt):
    raw = receipt.read_bytes()
    data = json.loads(raw)
    families = {}
    for family in ("point", "equality", "in2", "public_label"):
        pairs = [p for p in data["pairs"] if p["family"] == family]
        records = [r for r in data["records"] if r["family"] == family]
        medians = {
            slot: statistics.median(
                r["elapsed_ms"]["wall_ns"] * 1000 / r["calls"]
                for r in records if r["slot"] == slot
            )
            for slot in ("A", "B")
        }
        families[family] = {
            "median_microseconds_per_admission": medians,
            "B_minus_A_marginal_median_percent": 100 * (medians["B"] - medians["A"]) / medians["A"],
            "median_B_minus_A_paired_percent": statistics.median(p["B_minus_A_percent"] for p in pairs),
            "B_faster_pairs": sum(p["B_minus_A_percent"] < 0 for p in pairs),
            "material_pairs": sum(p["material"] for p in pairs),
            "pair_count": len(pairs),
        }
    by_generation = {}
    for generation in (0, 1, 2):
        spans = [s for s in data["gc_spans"] if s["generation"] == generation]
        by_generation[str(generation)] = {
            "count": len(spans),
            "total_wall_ms": sum(s["elapsed_ms"]["wall_ns"] for s in spans),
            "maximum_wall_ms": max((s["elapsed_ms"]["wall_ns"] for s in spans), default=0),
            "collected": sum(s["collected"] for s in spans),
            "uncollectable": sum(s["uncollectable"] for s in spans),
        }
    return {
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "classification": data["classification"],
        "failure": data["failure"],
        "total_cells": len(data["records"]),
        "total_timed_admissions": sum(r["calls"] for r in data["records"]),
        "total_pairs": len(data["pairs"]),
        "families": families,
        "all_material_pairs": [p for p in data["pairs"] if p["material"]],
        "wall_dominant_pairs": sum(p["wall_dominant"] for p in data["pairs"]),
        "clock_disagreements": data["clock_disagreements"],
        "maximum_cell_wall_minus_thread_absolute_ms": max(abs(r["elapsed_ms"]["wall_ns"] - r["elapsed_ms"]["thread_ns"]) for r in data["records"]),
        "maximum_cell_wall_minus_raw_absolute_ms": max(abs(r["elapsed_ms"]["wall_ns"] - r["elapsed_ms"]["raw_ns"]) for r in data["records"]),
        "gc_by_generation": by_generation,
        "generation_2_spans": [s for s in data["gc_spans"] if s["generation"] == 2],
        "limits": [
            "All pairs and GC spans retained; no subtraction, correction or exclusion.",
            "Paired medians and differences of marginal medians are different estimands and may have different signs.",
            "CPU duration tracking wall duration does not identify the cause of variation or establish equal instruction counts.",
            "Telemetry and retained observation objects can alter allocation and GC behavior.",
            "No contemporaneous system-load or hardware-frequency sample was collected.",
            "A/A observations do not explain the earlier C5 failure or change its gate result.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(analyze(args.receipt), indent=2) + "\n")
