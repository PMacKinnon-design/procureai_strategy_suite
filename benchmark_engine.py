import pandas as pd

def compare_with_benchmarks(metrics_df):
    benchmarks = pd.read_csv("benchmark_data.csv")

    # Add normalized keys for reliable merging
    metrics_df["_metric_key"] = metrics_df["Metric"].str.strip().str.lower()
    benchmarks["_metric_key"] = benchmarks["Metric"].str.strip().str.lower()

    # Merge on normalized keys
    comparison = pd.merge(
        metrics_df,
        benchmarks[["_metric_key", "Benchmark"]],
        on="_metric_key",
        how="inner"
    )

    # Drop the helper key and compute difference
    comparison = comparison.drop(columns=["_metric_key"])
    comparison["Difference"] = comparison["Value"] - comparison["Benchmark"]
    return comparison
