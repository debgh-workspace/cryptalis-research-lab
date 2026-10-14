"""Fixed C9 arithmetic; no data filtering, pooling versions, or retries."""
from statistics import median

WORKLOADS = ('in20-miss-ids', 'in20-hot-ids', 'in20-hot-text', 'equality-hot-text', 'point-text')
VARIANTS = ('native', 'original', 'candidate')
BLOCKS, WARMUPS, MEASURED = 7, 10, 40


def summarize(observations):
    assert len(observations) == 5250
    summary = {'workloads': {}, 'internal_relative_pass': True,
               'absolute_added_p95_pass': True, 'clock_anomalies': []}
    for index, row in enumerate(observations):
        assert row['sequence'] == index and row['status'] == 'ok' and row['row_check'] is True
        for clock, elapsed in row['elapsed_ns'].items():
            if elapsed < 0:
                summary['clock_anomalies'].append({'sequence': index, 'clock': clock, 'elapsed_ns': elapsed})
        disagreement = row['elapsed_ns']['wall'] - row['elapsed_ns']['raw']
        if abs(disagreement) > 1_000_000:
            summary['clock_anomalies'].append({'sequence': index,
                'wall_minus_raw_ns': disagreement, 'threshold_ns': 1_000_000})
    summary['clock_differences'] = {
        'wall_minus_raw_ns': {
            'min': min(r['elapsed_ns']['wall'] - r['elapsed_ns']['raw'] for r in observations),
            'max': max(r['elapsed_ns']['wall'] - r['elapsed_ns']['raw'] for r in observations)}}
    expected_order = []
    for block in range(BLOCKS):
        order = VARIANTS if block % 2 == 0 else VARIANTS[::-1]
        for workload in WORKLOADS:
            for variant in order:
                for sample in range(WARMUPS + MEASURED):
                    expected_order.append((block, workload, variant, sample,
                                           'warmup' if sample < WARMUPS else 'measured'))
    assert [(r['block'], r['workload'], r['variant'], r['sample'], r['phase'])
            for r in observations] == expected_order
    for workload in WORKLOADS:
        entries = {}
        for variant in VARIANTS:
            all_rows = [r for r in observations if r['workload'] == workload and r['variant'] == variant]
            assert len(all_rows) == 350
            measured = [r for r in all_rows if r['phase'] == 'measured']
            assert len(measured) == 280
            block_medians = []
            for block in range(BLOCKS):
                samples = [r['elapsed_ns']['wall'] for r in measured if r['block'] == block]
                assert len(samples) == 40
                block_medians.append(median(samples))
            p95 = sorted(r['elapsed_ns']['wall'] for r in measured)[265]
            entries[variant] = {'block_medians_ns': block_medians,
                                'median_of_block_medians_ns': median(block_medians), 'nearest_rank_p95_ns': p95}
        baseline = entries['original']['median_of_block_medians_ns']
        candidate = entries['candidate']['median_of_block_medians_ns']
        assert baseline > 0
        reduction = 100 * (baseline - candidate) / baseline
        favorable = sum(c < b for c, b in zip(entries['candidate']['block_medians_ns'], entries['original']['block_medians_ns']))
        primary = workload in WORKLOADS[:2]
        relative_pass = reduction >= 5 and favorable >= 6 if primary else candidate / baseline <= 1.10
        delta = entries['candidate']['nearest_rank_p95_ns'] - entries['native']['nearest_rank_p95_ns']
        limit = 3_000_000 if workload == 'equality-hot-text' else 8_000_000 if workload.startswith('in20') else None
        absolute_pass = None if limit is None else delta <= limit
        summary['workloads'][workload] = {'variants': entries, 'primary': primary,
            'reduction_percent': reduction, 'strictly_favorable_blocks': favorable,
            'candidate_original_ratio': candidate / baseline, 'relative_pass': relative_pass,
            'candidate_minus_native_p95_ns': delta, 'absolute_limit_ns': limit,
            'absolute_pass': absolute_pass}
        summary['internal_relative_pass'] &= relative_pass
        if absolute_pass is not None:
            summary['absolute_added_p95_pass'] &= absolute_pass
    summary['product_qualified'] = False
    return summary
