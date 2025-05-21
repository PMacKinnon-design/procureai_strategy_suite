import pandas as pd
def compare_with_benchmarks(metrics_df):
    benchmarks = pd.read_csv("benchmark_data.csv")
    comparison = metrics_df.merge(benchmarks, on="Metric", how="left")
    comparison["Difference"] = comparison["Value"] - comparison["Benchmark"]
    return comparison
