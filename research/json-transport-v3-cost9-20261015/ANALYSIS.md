# Completed native transport cost diagnostic: descriptive analysis

## Result

The exact ordered grid is complete: **1,620 records; 324 prespecified warmups excluded; all 1,296 measurements retained**. All nine cases, all six orders, every iteration and every position match the protocol exactly. No timing trimming, favorable-order selection, retry, or diagnostic rerun was performed by this analysis.

At 143 and 286 rows, native has lower mean full-fetch wall time and client process CPU than either JSON envelope in every one of the six order blocks, for every payload size. This is a descriptive result of this one synthetic diagnostic. One-row results and JSON-versus-JSONB ordering are mixed. These findings do not resolve the known per-OID custom-loader incompatibility and authorize no product-code promotion.

## What was checked

Only the three pinned files listed below were consumed. Each was admitted as an ordinary, finite regular file before reading; path components, byte length, SHA256 and stable descriptor metadata were checked. JSON rejects duplicate keys and nonfinite constants. Each record has the exact schema, positive integer timings, expected OIDs and text formats, and true full-fetch/close and GC flags.

Grid order: rows 1,143,286; nested payload bytes 0,74,1024; nested blocks 0..5; iterations 0..9; then positions 0..2 in that block's variant order. Iterations 0 and 1 are the only warmups. Each case contains 180 records: 36 warmups and 144 measurements, or 48 measured records per variant. Each block contains eight retained measured triplets. Full-fetch/close flags attest the producer's recorded checks; this data analysis does not independently reobserve cursor or connection state.

The block orders, preserved in full, are:
- 0: native > jsonb > json
- 1: native > json > jsonb
- 2: jsonb > native > json
- 3: jsonb > json > native
- 4: json > native > jsonb
- 5: json > jsonb > native

## Pairing and estimand

For each case, block and measured iteration, pair the three variants' records. For each of JSONB-native, JSON-native and JSON-JSONB, compute left minus right for the eight matched iterations within each block. The primary case delta is the arithmetic mean of the six block-mean paired deltas, giving every order equal weight. Because each block has eight pairs, this also equals the mean of all 48 paired differences. Positive means the left variant took more time. No cross-size pooled score is used.

The percentage is 100 × the equal-block mean paired delta / the equal-block mean right-variant time. It is a ratio of descriptive means, not the mean of per-sample percentage changes. Block ranges and signs below retain order sensitivity. CSV files provide all 432 paired triplets (all 1,296 measured records' timing values), all 324 block/comparison/metric summaries, and all 54 case/comparison/metric summaries. Integer paired differences and block sums preserve reproducible arithmetic; JSON/CSV summary means use Python standard-library arithmetic. Display tables round to three decimal places in microseconds and one decimal place in percent.

## Timing boundaries and limits

Wall time covers cursor creation, execute, complete ordered fetch, OID/format capture, and cursor close. It includes server waiting/execution and transport plus client work; it is not isolated server construction time. Client process CPU is client CPU only, not server CPU. Connection establishment, synthetic-input/query creation, post-fetch value assertions and safe JSONL writing are outside the interval. Native's additional output columns are part of this declared comparison. The native result shape is different; any product-side shape reconstruction or adapter work required by a derivative is not measured here. All variants use prepare=False and the protocol's common connection policy; GC remains enabled.

This is one run with fixed case/block order and serial adjacent triplets, not independently randomized or repeated runs. Six permutations balance variant position but do not remove temporal drift or establish population uncertainty. Individual samples can differ from block-mean direction; all are kept. No confidence interval, significance claim, win threshold, product performance pass, authenticated-read latency, server-CPU estimate, wire-byte total, index/storage qualification or 3/8 ms application-budget conclusion is supported. The known custom per-OID loader divergence remains unresolved; all broader product gates remain outside this analysis.

This artifact is a data-grid and descriptive-cost analysis, not the independent terminal closure audit. It does not inspect runtime status, tests, raw phase bodies, installed/live cells, environment, credentials, cache or Git; it does not import product/dependency code, rerun the diagnostic, contact a database or change product source. Root-reported completion is not revalidated here.

## Full-fetch wall: means and paired changes

All times below are microseconds. Each variant mean retains 48 measurements, with all six orders equally weighted.

| Rows | Bytes | Native mean | JSONB mean | JSON mean | JSONB-native Δ (%) | JSON-native Δ (%) | JSON-JSONB Δ (%) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 143.294 | 146.849 | 135.088 | +3.555 (+2.5%) | -8.206 (-5.7%) | -11.761 (-8.0%) |
| 1 | 74 | 123.222 | 129.615 | 128.583 | +6.392 (+5.2%) | +5.361 (+4.4%) | -1.032 (-0.8%) |
| 1 | 1024 | 167.968 | 223.359 | 229.529 | +55.391 (+33.0%) | +61.561 (+36.7%) | +6.170 (+2.8%) |
| 143 | 0 | 351.770 | 650.996 | 612.955 | +299.226 (+85.1%) | +261.186 (+74.2%) | -38.040 (-5.8%) |
| 143 | 74 | 395.938 | 720.581 | 664.626 | +324.643 (+82.0%) | +268.688 (+67.9%) | -55.955 (-7.8%) |
| 143 | 1024 | 1060.101 | 2208.845 | 1863.072 | +1148.744 (+108.4%) | +802.971 (+75.7%) | -345.773 (-15.7%) |
| 286 | 0 | 489.292 | 1069.027 | 980.772 | +579.735 (+118.5%) | +491.480 (+100.4%) | -88.255 (-8.3%) |
| 286 | 74 | 599.707 | 1339.493 | 1350.033 | +739.786 (+123.4%) | +750.326 (+125.1%) | +10.540 (+0.8%) |
| 286 | 1024 | 2351.860 | 4673.280 | 4098.198 | +2321.420 (+98.7%) | +1746.338 (+74.3%) | -575.082 (-12.3%) |

### Full-fetch wall: six-block ranges

Each cell is minimum to maximum block-mean paired delta in microseconds, followed by positive-block count out of six. The full CSV also includes medians and all per-block values.

| Rows | Bytes | JSONB-native range; positive | JSON-native range; positive | JSON-JSONB range; positive |
|---:|---:|---:|---:|---:|
| 1 | 0 | -31.165 to +19.401; 5/6 | -25.236 to +11.954; 3/6 | -30.927 to +7.816; 1/6 |
| 1 | 74 | +0.890 to +12.385; 6/6 | -7.868 to +19.699; 5/6 | -11.358 to +10.631; 2/6 |
| 1 | 1024 | +6.905 to +259.671; 6/6 | +7.436 to +125.001; 6/6 | -252.235 to +116.259; 4/6 |
| 143 | 0 | +279.788 to +330.203; 6/6 | +212.832 to +319.914; 6/6 | -67.206 to -8.588; 0/6 |
| 143 | 74 | +306.582 to +355.530; 6/6 | +233.523 to +384.426; 6/6 | -112.996 to +77.844; 1/6 |
| 143 | 1024 | +971.525 to +1476.120; 6/6 | +682.987 to +1021.854; 6/6 | -627.000 to -215.895; 0/6 |
| 286 | 0 | +487.800 to +674.178; 6/6 | +436.253 to +595.186; 6/6 | -237.925 to +107.386; 1/6 |
| 286 | 74 | +661.897 to +847.168; 6/6 | +600.491 to +975.201; 6/6 | -243.199 to +313.303; 2/6 |
| 286 | 1024 | +1529.012 to +2777.866; 6/6 | +1497.717 to +2210.776; 6/6 | -1264.465 to +17.889; 1/6 |

## Client process CPU: means and paired changes

All times below are microseconds. Each variant mean retains 48 measurements, with all six orders equally weighted.

| Rows | Bytes | Native mean | JSONB mean | JSON mean | JSONB-native Δ (%) | JSON-native Δ (%) | JSON-JSONB Δ (%) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 63.854 | 72.664 | 65.390 | +8.809 (+13.8%) | +1.536 (+2.4%) | -7.274 (-10.0%) |
| 1 | 74 | 62.719 | 61.875 | 63.252 | -0.844 (-1.3%) | +0.534 (+0.9%) | +1.377 (+2.2%) |
| 1 | 1024 | 79.689 | 82.864 | 90.857 | +3.175 (+4.0%) | +11.167 (+14.0%) | +7.992 (+9.6%) |
| 143 | 0 | 178.304 | 381.833 | 375.121 | +203.529 (+114.1%) | +196.817 (+110.4%) | -6.712 (-1.8%) |
| 143 | 74 | 199.804 | 402.633 | 414.089 | +202.829 (+101.5%) | +214.285 (+107.2%) | +11.456 (+2.8%) |
| 143 | 1024 | 520.223 | 977.693 | 932.637 | +457.470 (+87.9%) | +412.414 (+79.3%) | -45.055 (-4.6%) |
| 286 | 0 | 235.871 | 665.356 | 609.588 | +429.485 (+182.1%) | +373.717 (+158.4%) | -55.768 (-8.4%) |
| 286 | 74 | 296.325 | 747.114 | 832.013 | +450.789 (+152.1%) | +535.688 (+180.8%) | +84.899 (+11.4%) |
| 286 | 1024 | 1050.641 | 2082.816 | 2119.308 | +1032.175 (+98.2%) | +1068.667 (+101.7%) | +36.492 (+1.8%) |

### Client process CPU: six-block ranges

Each cell is minimum to maximum block-mean paired delta in microseconds, followed by positive-block count out of six. The full CSV also includes medians and all per-block values.

| Rows | Bytes | JSONB-native range; positive | JSON-native range; positive | JSON-JSONB range; positive |
|---:|---:|---:|---:|---:|
| 1 | 0 | -6.244 to +32.617; 5/6 | -5.592 to +7.521; 4/6 | -34.975 to +0.652; 3/6 |
| 1 | 74 | -11.100 to +7.435; 2/6 | -10.735 to +7.993; 4/6 | -7.580 to +5.847; 5/6 |
| 1 | 1024 | -20.762 to +33.161; 3/6 | -20.613 to +33.752; 5/6 | -20.793 to +26.249; 5/6 |
| 143 | 0 | +163.448 to +243.889; 6/6 | +161.444 to +241.646; 6/6 | -38.035 to +38.553; 2/6 |
| 143 | 74 | +176.835 to +223.384; 6/6 | +157.395 to +306.570; 6/6 | -28.131 to +83.186; 3/6 |
| 143 | 1024 | +375.128 to +532.028; 6/6 | +350.789 to +529.327; 6/6 | -138.661 to +64.828; 2/6 |
| 286 | 0 | +362.418 to +507.540; 6/6 | +325.585 to +444.821; 6/6 | -181.954 to +11.652; 1/6 |
| 286 | 74 | +383.954 to +549.168; 6/6 | +389.259 to +742.864; 6/6 | -144.736 to +358.910; 4/6 |
| 286 | 1024 | +919.235 to +1278.061; 6/6 | +808.444 to +1471.002; 6/6 | -181.279 to +424.152; 2/6 |

## Interpretation worth retaining

- In the six multirow cases, native's lower mean cost is consistent across all six blocks for both metrics against both envelopes. This is 144 positive block-mean paired deltas for the envelope-minus-native comparisons (6 cases × 6 blocks × 2 envelopes × 2 metrics). It does not say every individual measurement is faster.
- At 286 rows × 1,024 bytes, mean wall time is native 2.352 ms, JSON 4.098 ms and JSONB 4.673 ms; paired mean deltas versus native are +1.746 ms (+74.3%) for JSON and +2.321 ms (+98.7%) for JSONB. Client CPU means are native 1.051 ms, JSON 2.119 ms and JSONB 2.083 ms.
- One-row CPU changes are small and vary in sign across blocks. JSONB-native at one row × 74 bytes averages -0.844 µs client CPU, while its wall delta is +6.392 µs. At one row × zero bytes, JSON-native wall averages -8.206 µs with three positive and three negative blocks. No universal native advantage is claimed.
- JSON-versus-JSONB is not uniform. At 286 × 74, JSON wall averages +10.540 µs versus JSONB despite only two of six blocks being positive; the median block-mean delta is negative. At 286 × 1,024, JSON wall averages -575.082 µs versus JSONB, but client CPU averages +36.492 µs, with mixed block signs. Preserve these metric/order differences rather than selecting a favorable result.
- At one row × 1,024, JSONB-native wall block means span roughly +7 to +260 µs. The largest block is retained and materially affects the overall +55.391 µs mean. The complete raw samples and paired output are retained without trimming.

## Does JSON justify a product derivative investigation?

JSON has a narrow investigation lead: its wall block means are below JSONB in all six orders at 143 × 0 and 143 × 1,024, and its overall wall mean is lower in five of six multirow cases. That is enough to retain JSON as a candidate for a scoped feasibility investigation if a product decision requires one. It is not enough to select, implement or promote a derivative on performance grounds: no case has a client-CPU JSON advantage consistent across all six block means, wall ordering reverses at 286 × 74, and the known per-OID custom-loader incompatibility remains unresolved. The much more consistent native diagnostic result likewise does not price the extra product-side shape/adapter work. No new implementation or run is recommended as an automatic consequence of these data.

### Exact JSON-minus-JSONB paired block means

The following values include every block. Units are microseconds, printed to six decimal places; a mean of eight integer-nanosecond paired differences is an exact multiple of 0.000125 µs, so this display preserves the exact mean. Positive means JSON took more time. Block numbers use the fixed orders listed above.

#### Full-fetch wall

| Rows | Bytes | Block 0 | Block 1 | Block 2 | Block 3 | Block 4 | Block 5 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | -30.926750 | +7.816250 | -4.162250 | -29.386750 | -7.447250 | -6.459500 |
| 1 | 74 | -8.758125 | +10.630625 | +4.505375 | -0.351500 | -0.857500 | -11.358125 |
| 1 | 1024 | +71.580000 | +108.611625 | +116.259125 | -252.235000 | +15.153125 | -22.349000 |
| 143 | 0 | -8.588125 | -67.206375 | -10.289125 | -36.248125 | -59.085500 | -46.825000 |
| 143 | 74 | -81.979500 | -51.501000 | +77.844000 | -88.810125 | -112.995500 | -78.289875 |
| 143 | 1024 | -327.412625 | -396.898250 | -290.836750 | -215.895375 | -627.000000 | -216.597750 |
| 286 | 0 | -142.699375 | -65.179125 | -70.419500 | -120.695875 | +107.386250 | -237.924875 |
| 286 | 74 | +138.531000 | -73.929625 | -243.199125 | -67.906000 | -3.560000 | +313.303500 |
| 286 | 1024 | -1145.927750 | -567.089500 | -473.756000 | +17.888875 | -17.145500 | -1264.464750 |

#### Client process CPU

| Rows | Bytes | Block 0 | Block 1 | Block 2 | Block 3 | Block 4 | Block 5 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | -34.974625 | +0.651875 | +0.005875 | -7.767875 | +0.010875 | -1.568750 |
| 1 | 74 | +0.365375 | +5.847250 | +4.878250 | +2.388375 | +2.364875 | -7.580000 |
| 1 | 1024 | +20.903500 | +0.149125 | +26.249375 | +13.405125 | +8.041000 | -20.793375 |
| 143 | 0 | +38.552875 | -2.004750 | -21.353125 | +2.862625 | -38.035375 | -20.295125 |
| 143 | 74 | +32.681000 | +15.302500 | +83.186000 | -20.769750 | -13.530000 | -28.131125 |
| 143 | 1024 | +64.828125 | +21.431375 | -100.740625 | -82.930125 | -138.661000 | -34.260000 |
| 286 | 0 | -100.793375 | -2.591625 | -22.048500 | -38.869375 | +11.652250 | -181.954500 |
| 286 | 74 | +272.161750 | -11.645500 | -144.735750 | +4.138875 | +30.563375 | +358.909875 |
| 286 | 1024 | -181.279375 | +192.940875 | +424.151750 | -1.567500 | -72.697250 | -142.596250 |

## Exact input identities

- protocol: `experiments/json-transport-native-probe-v3-cost9-20261015/PROTOCOL.md`
  - 9896 bytes; SHA256 `e1e9fbfcfa248689e80107d0cf3aadc3af42d4d55452f23fba248c2c683556ff`
- source_review: `reviewer-notes/json-transport-native-probe-v3-cost9-independent-20261015/REVIEW.md`
  - 9461 bytes; SHA256 `cec14cef3605b26d8f348ba38e287a7059311e1668cbb638bf6c11d8b65b725a`
- observations: `evidence/json-transport-native-probe-v3-cost9-sa21-20261015/cost-observations.jsonl`
  - 484264 bytes; SHA256 `763f3ee2c883d57efa9fb3b6b8556656208196dc6725f04981dffc6944b6e241`

## Reproduction and artifacts

From the repository root, run only the offline standard-library analyzer:

```sh
python3 -B reviewer-notes/json-transport-cost-analysis-20261015/analyze_cost.py
```

It reads only the three pinned input files above and writes only to this analysis directory. It cannot launch a test or database operation. A changed input identity fails rather than silently producing a new result. This command reproduces the data analysis; it is not a diagnostic rerun.

- `analyze_cost.py`: complete standard-library source.
- `input-hashes.json`: pinned input byte lengths and SHA256 digests.
- `paired-measurements.csv`: 432 paired triplets with all measured timing values and paired deltas.
- `block-comparisons.csv`: 324 paired descriptive summaries with all six block orders.
- `case-comparisons.csv`: 54 equal-block case summaries.
- `results.json`: validation, input identities and full summary data.
- `analysis.stdout` / `analysis.stderr`: original offline analyzer execution output.
- `SHA256SUMS.txt`: artifact integrity manifest; the manifest's own digest is reported separately.
