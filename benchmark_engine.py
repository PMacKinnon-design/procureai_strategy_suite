import pandas as pd

def compare_with_benchmarks(metrics_df):
    benchmarks = pd.read_csv("benchmark_data.csv")
    metrics_df["_metric_key"] = metrics_df["Metric"].str.strip().str.lower()
    benchmarks["_metric_key"] = benchmarks["Metric"].str.strip().str.lower()
    comparison = pd.merge(metrics_df, benchmarks[["_metric_key", "Benchmark"]], on="_metric_key", how="inner")
    comparison.drop(columns=["_metric_key"], inplace=True)
    comparison["Difference"] = comparison["Value"] - comparison["Benchmark"]
    return comparison
