import csv
import math
from collections import defaultdict, Counter

def is_numeric(val):
    try:
        float(val)
        return True
    except:
        return False

def compute_stats(values):
    stats = {}
    count = len(values)
    stats["count"] = count
    if count == 0:
        return stats
    try:
        values_float = list(map(float, values))
        stats["mean"] = sum(values_float) / count
        stats["min"] = min(values_float)
        stats["max"] = max(values_float)
        mean = stats["mean"]
        stats["std_dev"] = math.sqrt(sum((x - mean) ** 2 for x in values_float) / count)
    except:
        counter = Counter(values)
        stats["unique_count"] = len(counter)
        stats["most_common"] = counter.most_common(1)[0]
    return stats

def analyze(rows, columns, column_types):
    results = {}
    col_values = defaultdict(list)
    for row in rows:
        for col in columns:
            val = row[col].strip()
            if val:
                col_values[col].append(val)

    for col in columns:
        results[col] = compute_stats(col_values[col])

    return results

def group_by(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        group_key = tuple(row[k] for k in keys)
        grouped[group_key].append(row)
    return grouped

def print_summary(title, stats_dict):
    print(f"\n--- {title} ---")
    for col, stats in stats_dict.items():
        print(f"\nColumn: {col}")
        for k, v in stats.items():
            print(f"  {k}: {v}")

def main(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames

    # Detect column types using first two rows
    sample_rows = rows[:2]
    column_types = {
        col: "numeric" if all(is_numeric(row[col]) for row in sample_rows) else "non-numeric"
        for col in columns
    }

    # Full dataset analysis
    full_stats = analyze(rows, columns, column_types)
    print_summary("Overall Stats", full_stats)

    # Group by page_id
    page_groups = group_by(rows, ["page_id"])
    print("\n===== Grouped by page_id =====")
    for key, group_rows in list(page_groups.items())[:5]:  # limit to 5 groups
        stats = analyze(group_rows, columns, column_types)
        print_summary(f"Group: page_id = {key}", stats)

    # Group by page_id and ad_id
    page_ad_groups = group_by(rows, ["page_id", "ad_id"])
    print("\n===== Grouped by page_id and ad_id =====")
    for key, group_rows in list(page_ad_groups.items())[:5]:  # limit to 5 groups
        stats = analyze(group_rows, columns, column_types)
        print_summary(f"Group: page_id, ad_id = {key}", stats)

if __name__ == "__main__":
    main("D:/Data/period_03/period_03/2024_fb_ads_president_scored_anon.csv")  # Change path if needed
