#!/usr/bin/env python3
"""Read three pinned inert files; validate and describe the completed cost grid.

No product/dependency imports, test collection/execution, subprocesses, database,
network, environment, Git, installed-file, cache, raw-phase, or live-cell access.
All output is confined to the directory containing this script.
"""
import csv
import hashlib
import io
import itertools
import json
import os
from pathlib import Path
import stat
import statistics


OUT = Path(__file__).absolute().parent
BASE = OUT.parent.parent
INPUTS = {
    "protocol": (
        "experiments/json-transport-native-probe-v3-cost9-20261015/PROTOCOL.md",
        9896,
        "e1e9fbfcfa248689e80107d0cf3aadc3af42d4d55452f23fba248c2c683556ff",
    ),
    "source_review": (
        "reviewer-notes/json-transport-native-probe-v3-cost9-independent-20261015/REVIEW.md",
        9461,
        "cec14cef3605b26d8f348ba38e287a7059311e1668cbb638bf6c11d8b65b725a",
    ),
    "observations": (
        "evidence/json-transport-native-probe-v3-cost9-sa21-20261015/cost-observations.jsonl",
        484264,
        "763f3ee2c883d57efa9fb3b6b8556656208196dc6725f04981dffc6944b6e241",
    ),
}
VARIANTS = ("native", "jsonb", "json")
ORDERS = tuple(itertools.permutations(VARIANTS))
CASES = tuple(itertools.product((1, 143, 286), (0, 74, 1024)))
METRICS = ("wall_ns", "client_process_cpu_ns")
PAIRS = (("jsonb", "native"), ("json", "native"), ("json", "jsonb"))
OIDS = {"native": [23, 17, 20, 2950], "jsonb": [23, 3802], "json": [23, 114]}
KEYS = {
    "block", "client_process_cpu_ns", "complete_fetch_closed", "formats",
    "gc_enabled", "iteration", "oids", "order", "payload_bytes", "position",
    "rows", "variant", "wall_ns", "warmup",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_admitted(rel, expected_size, expected_hash):
    path = BASE / rel
    for directory in reversed(path.parents):
        mode = directory.lstat().st_mode
        require(stat.S_ISDIR(mode) and not stat.S_ISLNK(mode), "nonordinary ancestor")
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "input is not an ordinary regular file")
    require(before.st_size == expected_size <= 1_048_576, "input size changed")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        opened = os.fstat(stream.fileno())
        require((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
                "input identity changed during admission")
        data = stream.read(expected_size + 1)
        after = os.fstat(stream.fileno())
    require(len(data) == expected_size, "input size changed during read")
    require((opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) ==
            (after.st_size, after.st_mtime_ns, after.st_ctime_ns), "input changed during read")
    require(hashlib.sha256(data).hexdigest() == expected_hash, "input hash mismatch")
    return data


def object_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("nonfinite JSON number: " + value)


def write_text(name, value):
    target = OUT / name
    if target.exists() or target.is_symlink():
        require(stat.S_ISREG(target.lstat().st_mode), "nonordinary output target")
    target.write_text(value, encoding="utf-8")


def write_json(name, value):
    write_text(name, json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def write_csv(name, records):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(records[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    write_text(name, buffer.getvalue())


data = {name: read_admitted(*spec) for name, spec in INPUTS.items()}
lines = data["observations"].splitlines()
require(len(lines) == 1620 and all(lines), "expected exactly 1620 nonblank records")
records = [json.loads(line, object_pairs_hook=object_no_duplicates,
                      parse_constant=reject_constant) for line in lines]
expected = [
    (rows, payload, block, list(order), iteration, position, variant, iteration < 2)
    for rows, payload in CASES
    for block, order in enumerate(ORDERS)
    for iteration in range(10)
    for position, variant in enumerate(order)
]
identity_keys = ("rows", "payload_bytes", "block", "order", "iteration", "position", "variant", "warmup")
for index, (record, identity) in enumerate(zip(records, expected), start=1):
    require(type(record) is dict and set(record) == KEYS, f"schema at line {index}")
    require(tuple(record[key] for key in identity_keys) == identity, f"order at line {index}")
    for key in ("rows", "payload_bytes", "block", "iteration", "position") + METRICS:
        require(type(record[key]) is int, f"integer type at line {index}: {key}")
    require(type(record["warmup"]) is bool, f"warmup type at line {index}")
    require(all(record[key] > 0 for key in METRICS), f"nonpositive timing at line {index}")
    require(record["complete_fetch_closed"] is True, f"closure flag at line {index}")
    require(record["gc_enabled"] is True, f"GC flag at line {index}")
    require(record["oids"] == OIDS[record["variant"]], f"OIDs at line {index}")
    require(record["formats"] == [0] * len(record["oids"]), f"formats at line {index}")
    require(all(type(x) is int for x in record["oids"] + record["formats"]),
            f"metadata integer type at line {index}")

warmups = [record for record in records if record["warmup"]]
measured = [record for record in records if not record["warmup"]]
require(len(warmups) == 324 and len(measured) == 1296, "warmup/measurement counts")
by_key = {(r["rows"], r["payload_bytes"], r["block"], r["iteration"], r["variant"]): r
          for r in measured}
require(len(by_key) == 1296, "duplicate measurements")

paired = []
blocks = []
for rows, payload in CASES:
    for block, order in enumerate(ORDERS):
        for iteration in range(2, 10):
            item = {"rows": rows, "payload_bytes": payload, "block": block,
                    "order": ">".join(order), "iteration": iteration}
            for metric in METRICS:
                for variant in VARIANTS:
                    item[variant + "_" + metric] = by_key[(rows, payload, block, iteration, variant)][metric]
                for left, right in PAIRS:
                    item[left + "_minus_" + right + "_" + metric] = item[left + "_" + metric] - item[right + "_" + metric]
            paired.append(item)
        for metric in METRICS:
            samples = {variant: [by_key[(rows, payload, block, iteration, variant)][metric]
                                 for iteration in range(2, 10)] for variant in VARIANTS}
            for left, right in PAIRS:
                deltas = [a - b for a, b in zip(samples[left], samples[right])]
                left_mean = statistics.mean(samples[left])
                right_mean = statistics.mean(samples[right])
                blocks.append({
                    "rows": rows, "payload_bytes": payload, "block": block,
                    "order": ">".join(order), "metric": metric,
                    "comparison": left + "-" + right, "left": left, "right": right,
                    "pairs": 8, "left_sum_ns": sum(samples[left]), "right_sum_ns": sum(samples[right]),
                    "paired_delta_sum_ns": sum(deltas),
                    "left_mean_ns": left_mean, "right_mean_ns": right_mean,
                    "paired_delta_mean_ns": statistics.mean(deltas),
                    "paired_delta_median_ns": statistics.median(deltas),
                    "paired_delta_min_ns": min(deltas), "paired_delta_max_ns": max(deltas),
                    "mean_delta_percent_of_right_mean": 100 * statistics.mean(deltas) / right_mean,
                    "negative_pairs": sum(delta < 0 for delta in deltas),
                    "zero_pairs": sum(delta == 0 for delta in deltas),
                    "positive_pairs": sum(delta > 0 for delta in deltas),
                })

summaries = []
for rows, payload in CASES:
    for metric in METRICS:
        for left, right in PAIRS:
            selected = [b for b in blocks if (b["rows"], b["payload_bytes"], b["metric"], b["left"], b["right"]) ==
                        (rows, payload, metric, left, right)]
            require([b["block"] for b in selected] == list(range(6)), "lost or reordered blocks")
            deltas = [b["paired_delta_mean_ns"] for b in selected]
            right_mean = statistics.mean(b["right_mean_ns"] for b in selected)
            summaries.append({
                "rows": rows, "payload_bytes": payload, "metric": metric,
                "comparison": left + "-" + right, "left": left, "right": right,
                "blocks": 6, "pairs_per_block": 8, "total_pairs": 48,
                "left_mean_ns": statistics.mean(b["left_mean_ns"] for b in selected),
                "right_mean_ns": right_mean,
                "equal_block_mean_delta_ns": statistics.mean(deltas),
                "mean_delta_percent_of_right_mean": 100 * statistics.mean(deltas) / right_mean,
                "median_block_mean_delta_ns": statistics.median(deltas),
                "minimum_block_mean_delta_ns": min(deltas), "maximum_block_mean_delta_ns": max(deltas),
                "negative_blocks": sum(delta < 0 for delta in deltas),
                "zero_blocks": sum(delta == 0 for delta in deltas),
                "positive_blocks": sum(delta > 0 for delta in deltas),
            })
require(len(paired) == 432 and len(blocks) == 324 and len(summaries) == 54, "output-grid count")
require(all(s["positive_blocks"] == 6 for s in summaries
            if s["rows"] > 1 and s["right"] == "native"), "multirow summary claim")

input_hashes = {name: {"path": spec[0], "bytes": spec[1], "sha256": spec[2]}
                for name, spec in INPUTS.items()}
validation = {
    "verdict": "COMPLETE_ORDERED_COST_GRID_VALIDATED_DESCRIPTIVE_ONLY",
    "records": 1620, "warmups_validated_and_excluded": 324, "measurements_retained": 1296,
    "cases": 9, "blocks_per_case": 6, "triplets_per_block": 10,
    "warmup_triplets_per_block": 2, "measured_triplets_per_block": 8,
    "records_per_case": 180, "warmups_per_case": 36, "measurements_per_case": 144,
    "measurements_per_variant_per_case": 48, "paired_measured_triplets": 432,
    "orders": [list(order) for order in ORDERS],
    "exact_record_order": True, "exact_schema": True, "exact_oids_and_text_formats": True,
    "all_close_and_gc_flags_true": True, "positive_integer_timings": True,
    "trimmed_records": 0, "selected_orders": "all six", "excluded_measured_records": 0,
    "terminal_audit_independently_performed_here": False,
}
write_json("input-hashes.json", input_hashes)
write_csv("paired-measurements.csv", paired)
write_csv("block-comparisons.csv", blocks)
write_csv("case-comparisons.csv", summaries)
write_json("results.json", {"inputs": input_hashes, "validation": validation,
                            "block_comparisons": blocks, "case_comparisons": summaries})

def lookup(rows, payload, metric, comparison):
    return next(s for s in summaries if (s["rows"], s["payload_bytes"], s["metric"], s["comparison"]) ==
                (rows, payload, metric, comparison))


report = [
    "# Completed native transport cost diagnostic: descriptive analysis",
    "",
    "## Result",
    "",
    "The exact ordered grid is complete: **1,620 records; 324 prespecified warmups excluded; all 1,296 measurements retained**. All nine cases, all six orders, every iteration and every position match the protocol exactly. No timing trimming, favorable-order selection, retry, or diagnostic rerun was performed by this analysis.",
    "",
    "At 143 and 286 rows, native has lower mean full-fetch wall time and client process CPU than either JSON envelope in every one of the six order blocks, for every payload size. This is a descriptive result of this one synthetic diagnostic. One-row results and JSON-versus-JSONB ordering are mixed. These findings do not resolve the known per-OID custom-loader incompatibility and authorize no product-code promotion.",
    "",
    "## What was checked",
    "",
    "Only the three pinned files listed below were consumed. Each was admitted as an ordinary, finite regular file before reading; path components, byte length, SHA256 and stable descriptor metadata were checked. JSON rejects duplicate keys and nonfinite constants. Each record has the exact schema, positive integer timings, expected OIDs and text formats, and true full-fetch/close and GC flags.",
    "",
    "Grid order: rows 1,143,286; nested payload bytes 0,74,1024; nested blocks 0..5; iterations 0..9; then positions 0..2 in that block's variant order. Iterations 0 and 1 are the only warmups. Each case contains 180 records: 36 warmups and 144 measurements, or 48 measured records per variant. Each block contains eight retained measured triplets. Full-fetch/close flags attest the producer's recorded checks; this data analysis does not independently reobserve cursor or connection state.",
    "",
    "The block orders, preserved in full, are:",
]
report += [f"- {i}: {' > '.join(order)}" for i, order in enumerate(ORDERS)]
report += [
    "",
    "## Pairing and estimand",
    "",
    "For each case, block and measured iteration, pair the three variants' records. For each of JSONB-native, JSON-native and JSON-JSONB, compute left minus right for the eight matched iterations within each block. The primary case delta is the arithmetic mean of the six block-mean paired deltas, giving every order equal weight. Because each block has eight pairs, this also equals the mean of all 48 paired differences. Positive means the left variant took more time. No cross-size pooled score is used.",
    "",
    "The percentage is 100 × the equal-block mean paired delta / the equal-block mean right-variant time. It is a ratio of descriptive means, not the mean of per-sample percentage changes. Block ranges and signs below retain order sensitivity. CSV files provide all 432 paired triplets (all 1,296 measured records' timing values), all 324 block/comparison/metric summaries, and all 54 case/comparison/metric summaries. Integer paired differences and block sums preserve reproducible arithmetic; JSON/CSV summary means use Python standard-library arithmetic. Display tables round to three decimal places in microseconds and one decimal place in percent.",
    "",
    "## Timing boundaries and limits",
    "",
    "Wall time covers cursor creation, execute, complete ordered fetch, OID/format capture, and cursor close. It includes server waiting/execution and transport plus client work; it is not isolated server construction time. Client process CPU is client CPU only, not server CPU. Connection establishment, synthetic-input/query creation, post-fetch value assertions and safe JSONL writing are outside the interval. Native's additional output columns are part of this declared comparison. The native result shape is different; any product-side shape reconstruction or adapter work required by a derivative is not measured here. All variants use prepare=False and the protocol's common connection policy; GC remains enabled.",
    "",
    "This is one run with fixed case/block order and serial adjacent triplets, not independently randomized or repeated runs. Six permutations balance variant position but do not remove temporal drift or establish population uncertainty. Individual samples can differ from block-mean direction; all are kept. No confidence interval, significance claim, win threshold, product performance pass, authenticated-read latency, server-CPU estimate, wire-byte total, index/storage qualification or 3/8 ms application-budget conclusion is supported. The known custom per-OID loader divergence remains unresolved; all broader product gates remain outside this analysis.",
    "",
    "This artifact is a data-grid and descriptive-cost analysis, not the independent terminal closure audit. It does not inspect runtime status, tests, raw phase bodies, installed/live cells, environment, credentials, cache or Git; it does not import product/dependency code, rerun the diagnostic, contact a database or change product source. Root-reported completion is not revalidated here.",
]
for metric, title in (("wall_ns", "Full-fetch wall"), ("client_process_cpu_ns", "Client process CPU")):
    report += ["", f"## {title}: means and paired changes", "",
               "All times below are microseconds. Each variant mean retains 48 measurements, with all six orders equally weighted.", "",
               "| Rows | Bytes | Native mean | JSONB mean | JSON mean | JSONB-native Δ (%) | JSON-native Δ (%) | JSON-JSONB Δ (%) |",
               "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for rows, payload in CASES:
        bn = lookup(rows, payload, metric, "jsonb-native")
        jn = lookup(rows, payload, metric, "json-native")
        jb = lookup(rows, payload, metric, "json-jsonb")
        def change(item):
            return f"{item['equal_block_mean_delta_ns']/1000:+.3f} ({item['mean_delta_percent_of_right_mean']:+.1f}%)"
        report.append(f"| {rows} | {payload} | {bn['right_mean_ns']/1000:.3f} | {bn['left_mean_ns']/1000:.3f} | {jn['left_mean_ns']/1000:.3f} | {change(bn)} | {change(jn)} | {change(jb)} |")
    report += ["", f"### {title}: six-block ranges", "",
               "Each cell is minimum to maximum block-mean paired delta in microseconds, followed by positive-block count out of six. The full CSV also includes medians and all per-block values.", "",
               "| Rows | Bytes | JSONB-native range; positive | JSON-native range; positive | JSON-JSONB range; positive |",
               "|---:|---:|---:|---:|---:|"]
    for rows, payload in CASES:
        cells = []
        for left, right in PAIRS:
            item = lookup(rows, payload, metric, left + "-" + right)
            cells.append(f"{item['minimum_block_mean_delta_ns']/1000:+.3f} to {item['maximum_block_mean_delta_ns']/1000:+.3f}; {item['positive_blocks']}/6")
        report.append(f"| {rows} | {payload} | " + " | ".join(cells) + " |")
report += [
    "", "## Interpretation worth retaining", "",
    "- In the six multirow cases, native's lower mean cost is consistent across all six blocks for both metrics against both envelopes. This is 144 positive block-mean paired deltas for the envelope-minus-native comparisons (6 cases × 6 blocks × 2 envelopes × 2 metrics). It does not say every individual measurement is faster.",
    "- At 286 rows × 1,024 bytes, mean wall time is native 2.352 ms, JSON 4.098 ms and JSONB 4.673 ms; paired mean deltas versus native are +1.746 ms (+74.3%) for JSON and +2.321 ms (+98.7%) for JSONB. Client CPU means are native 1.051 ms, JSON 2.119 ms and JSONB 2.083 ms.",
    "- One-row CPU changes are small and vary in sign across blocks. JSONB-native at one row × 74 bytes averages -0.844 µs client CPU, while its wall delta is +6.392 µs. At one row × zero bytes, JSON-native wall averages -8.206 µs with three positive and three negative blocks. No universal native advantage is claimed.",
    "- JSON-versus-JSONB is not uniform. At 286 × 74, JSON wall averages +10.540 µs versus JSONB despite only two of six blocks being positive; the median block-mean delta is negative. At 286 × 1,024, JSON wall averages -575.082 µs versus JSONB, but client CPU averages +36.492 µs, with mixed block signs. Preserve these metric/order differences rather than selecting a favorable result.",
    "- At one row × 1,024, JSONB-native wall block means span roughly +7 to +260 µs. The largest block is retained and materially affects the overall +55.391 µs mean. The complete raw samples and paired output are retained without trimming.",
    "", "## Does JSON justify a product derivative investigation?", "",
    "JSON has a narrow investigation lead: its wall block means are below JSONB in all six orders at 143 × 0 and 143 × 1,024, and its overall wall mean is lower in five of six multirow cases. That is enough to retain JSON as a candidate for a scoped feasibility investigation if a product decision requires one. It is not enough to select, implement or promote a derivative on performance grounds: no case has a client-CPU JSON advantage consistent across all six block means, wall ordering reverses at 286 × 74, and the known per-OID custom-loader incompatibility remains unresolved. The much more consistent native diagnostic result likewise does not price the extra product-side shape/adapter work. No new implementation or run is recommended as an automatic consequence of these data.",
    "",
    "### Exact JSON-minus-JSONB paired block means", "",
    "The following values include every block. Units are microseconds, printed to six decimal places; a mean of eight integer-nanosecond paired differences is an exact multiple of 0.000125 µs, so this display preserves the exact mean. Positive means JSON took more time. Block numbers use the fixed orders listed above.",
]
for metric, title in (("wall_ns", "Full-fetch wall"), ("client_process_cpu_ns", "Client process CPU")):
    report += ["", f"#### {title}", "",
               "| Rows | Bytes | Block 0 | Block 1 | Block 2 | Block 3 | Block 4 | Block 5 |",
               "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for rows, payload in CASES:
        selected = [b for b in blocks if (b["rows"], b["payload_bytes"], b["metric"], b["comparison"]) ==
                    (rows, payload, metric, "json-jsonb")]
        report.append(f"| {rows} | {payload} | " + " | ".join(
            f"{b['paired_delta_mean_ns']/1000:+.6f}" for b in selected) + " |")
report += ["", "## Exact input identities", ""]
for name, item in input_hashes.items():
    report += [f"- {name}: `{item['path']}`", f"  - {item['bytes']} bytes; SHA256 `{item['sha256']}`"]
report += [
    "", "## Reproduction and artifacts", "",
    "From the repository root, run only the offline standard-library analyzer:",
    "", "```sh", "python3 -B reviewer-notes/json-transport-cost-analysis-20261015/analyze_cost.py", "```", "",
    "It reads only the three pinned input files above and writes only to this analysis directory. It cannot launch a test or database operation. A changed input identity fails rather than silently producing a new result. This command reproduces the data analysis; it is not a diagnostic rerun.",
    "",
    "- `analyze_cost.py`: complete standard-library source.",
    "- `input-hashes.json`: pinned input byte lengths and SHA256 digests.",
    "- `paired-measurements.csv`: 432 paired triplets with all measured timing values and paired deltas.",
    "- `block-comparisons.csv`: 324 paired descriptive summaries with all six block orders.",
    "- `case-comparisons.csv`: 54 equal-block case summaries.",
    "- `results.json`: validation, input identities and full summary data.",
    "- `analysis.stdout` / `analysis.stderr`: original offline analyzer execution output.",
    "- `SHA256SUMS.txt`: artifact integrity manifest; the manifest's own digest is reported separately.",
    "",
]
write_text("ANALYSIS.md", "\n".join(report))
print(json.dumps(validation, sort_keys=True))
print("Wrote ANALYSIS.md, input-hashes.json, paired-measurements.csv, block-comparisons.csv, case-comparisons.csv, results.json")
