from collections import defaultdict


def aggregate_patterns(patterns):

    grouped = defaultdict(set)

    for p in patterns:

        pattern = p.get("pattern")
        description = p.get("description")

        if not pattern or not description:
            continue

        # normalize pattern name
        pattern_key = pattern.strip().lower()

        grouped[pattern_key].add(description)

    aggregated = []

    for pattern, reasons in grouped.items():

        aggregated.append({
            "pattern": pattern,
            "reasons": list(reasons)
        })

    return aggregated