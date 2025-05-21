import pandas as pd

def compare_with_benchmarks(metrics_df):
    benchmarks = pd.read_csv("benchmark_data.csv")

    # Normalize metric names for exact match
    metrics_df["Metric"] = metrics_df["Metric"].str.strip().str.lower()
    benchmarks["Metric"] = benchmarks["Metric"].str.strip().str.lower()

    comparison = pd.merge(metrics_df, benchmarks, on="Metric", how="inner")
    comparison["Difference"] = comparison["Value"] - comparison["Benchmark"]
    return comparison
