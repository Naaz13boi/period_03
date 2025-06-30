import csv
import math
from collections import defaultdict, Counter

def is_numeric(val):
    """More robust numeric detection"""
    if not val or not val.strip():
        return False
    try:
        float(val.strip())
        return True
    except (ValueError, TypeError):
        return False

def detect_column_types(rows, columns):
    """Improved column type detection using more data"""
    column_types = {}
    sample_size = min(100, len(rows))  # Check up to 100 rows
    
    for col in columns:
        numeric_count = sum(1 for row in rows[:sample_size] 
                          if is_numeric(row.get(col, '')))
        # Consider numeric if >80% of non-empty values are numeric
        total_non_empty = sum(1 for row in rows[:sample_size] 
                            if row.get(col, '').strip())
        column_types[col] = ("numeric" if total_non_empty > 0 and 
                           numeric_count / total_non_empty > 0.8 else "categorical")
    
    return column_types

def compute_stats(values, is_numeric_col=True):
    """Enhanced statistics computation"""
    stats = {}
    non_empty_values = [v for v in values if v.strip()]
    stats["count"] = len(values)
    stats["non_empty_count"] = len(non_empty_values)
    
    if not non_empty_values:
        return stats
    
    if is_numeric_col:
        try:
            numeric_values = [float(v.strip()) for v in non_empty_values]
            stats.update(_compute_numeric_stats(numeric_values))
        except (ValueError, TypeError):
            # Fallback to categorical if conversion fails
            stats.update(_compute_categorical_stats(non_empty_values))
    else:
        stats.update(_compute_categorical_stats(non_empty_values))
    
    return stats

def _compute_numeric_stats(values):
    """Compute comprehensive numeric statistics"""
    if not values:
        return {}
    
    values.sort()  # Sort once for median and percentiles
    n = len(values)
    
    stats = {
        "mean": sum(values) / n,
        "min": values[0],
        "max": values[-1],
        "median": values[n//2] if n % 2 == 1 else (values[n//2-1] + values[n//2]) / 2,
        "q1": values[n//4],
        "q3": values[3*n//4],
    }
    
    # Standard deviation
    mean = stats["mean"]
    variance = sum((x - mean) ** 2 for x in values) / n
    stats["std_dev"] = math.sqrt(variance)
    
    # Mode for numeric data
    counter = Counter(values)
    if counter:
        stats["mode"] = counter.most_common(1)[0]
    
    return stats

def _compute_categorical_stats(values):
    """Compute categorical statistics"""
    counter = Counter(values)
    return {
        "unique_count": len(counter),
        "most_common": counter.most_common(3),  # Top 3 instead of just 1
        "least_common": counter.most_common()[-3:] if len(counter) >= 3 else counter.most_common()
    }

def analyze_data(rows, columns, column_types):
    """Optimized data analysis"""
    results = {}
    
    # Single pass through data to collect all column values
    col_values = defaultdict(list)
    for row in rows:
        for col in columns:
            col_values[col].append(row.get(col, ''))
    
    # Compute stats for each column
    for col in columns:
        is_numeric_col = column_types.get(col) == "numeric"
        results[col] = compute_stats(col_values[col], is_numeric_col)
    
    return results

def group_by_keys(rows, keys):
    """Efficient grouping with better key handling"""
    grouped = defaultdict(list)
    for row in rows:
        # Handle missing keys gracefully
        group_key = tuple(row.get(k, 'NULL') for k in keys)
        grouped[group_key].append(row)
    return grouped

def format_stats_output(title, stats_dict, max_groups=None):
    """Improved output formatting"""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60)
    
    count = 0
    for col, stats in stats_dict.items():
        if max_groups and count >= max_groups:
            print(f"\n... (showing first {max_groups} items)")
            break
            
        print(f"\n📊 Column: {col}")
        print("-" * 40)
        
        for key, value in stats.items():
            if key == "most_common" and isinstance(value, list):
                print(f"  {key}:")
                for item, freq in value:
                    print(f"    '{item}': {freq}")
            elif key == "mode" and isinstance(value, tuple):
                print(f"  {key}: {value[0]} (appears {value[1]} times)")
            elif isinstance(value, float):
                print(f"  {key}: {value:.3f}")
            else:
                print(f"  {key}: {value}")
        count += 1

def validate_file_and_keys(filepath, required_keys):
    """Validate file exists and has required columns"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames or []
            
            missing_keys = [key for key in required_keys if key not in columns]
            if missing_keys:
                print(f"  Warning: Missing required columns: {missing_keys}")
                return columns, False
            return columns, True
    except FileNotFoundError:
        print(f" Error: File '{filepath}' not found")
        return [], False
    except Exception as e:
        print(f" Error reading file: {e}")
        return [], False

def main(filepath):
    """Main analysis function with better error handling"""
    print(f"🔍 Analyzing dataset: {filepath}")
    
    # Validate file and required columns
    required_keys = ["page_id", "ad_id"]
    columns, is_valid = validate_file_and_keys(filepath, required_keys)
    
    if not columns:
        return
    
    # Load data
    try:
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f" Error loading data: {e}")
        return
    
    if not rows:
        print(" No data found in file")
        return
    
    print(f" Loaded {len(rows)} rows with {len(columns)} columns")
    
    # Detect column types
    column_types = detect_column_types(rows, columns)
    print(f" Detected {sum(1 for t in column_types.values() if t == 'numeric')} numeric columns")
    
    # Overall analysis
    overall_stats = analyze_data(rows, columns, column_types)
    format_stats_output("OVERALL DATASET STATISTICS", overall_stats)
    
    # Group by page_id (if column exists)
    if "page_id" in columns:
        page_groups = group_by_keys(rows, ["page_id"])
        print(f"\n🔗 Found {len(page_groups)} unique page_id groups")
        
        # Analyze a sample of groups
        sample_groups = dict(list(page_groups.items())[:3])
        for group_key, group_rows in sample_groups.items():
            group_stats = analyze_data(group_rows, columns, column_types)
            format_stats_output(f"PAGE_ID = {group_key[0]} ({len(group_rows)} rows)", 
                              group_stats, max_groups=5)
    
    # Group by page_id and ad_id (if both exist)
    if all(col in columns for col in ["page_id", "ad_id"]):
        page_ad_groups = group_by_keys(rows, ["page_id", "ad_id"])
        print(f"\n🔗 Found {len(page_ad_groups)} unique (page_id, ad_id) combinations")
        
        # Analyze a sample of groups
        sample_groups = dict(list(page_ad_groups.items())[:2])
        for group_key, group_rows in sample_groups.items():
            group_stats = analyze_data(group_rows, columns, column_types)
            format_stats_output(f"PAGE_ID = {group_key[0]}, AD_ID = {group_key[1]} ({len(group_rows)} rows)", 
                              group_stats, max_groups=5)

if __name__ == "__main__":
    main("D:/Data/period_03/period_03/2024_fb_ads_president_scored_anon.csv")