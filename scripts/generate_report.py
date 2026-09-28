import json
import pandas as pd
from pathlib import Path
from tabulate import tabulate

def main():
    output_dir = Path("data/outputs")
    
    all_results = []
    if not output_dir.exists():
        print("No output data found. Run benchmark first.")
        return
        
    for result_file in output_dir.glob("*_results.json"):
        with open(result_file, "r") as f:
            data = json.load(f)
            all_results.extend(data)
            
    if not all_results:
        print("No valid result data found.")
        return
        
    df = pd.DataFrame(all_results)
    
    # Calculate average TTFA by provider
    if "ttfa" in df.columns:
        summary = df[df["success"] == True].groupby("provider")["ttfa"].mean().reset_index()
        summary = summary.sort_values("ttfa")
        print("\n=== TTS Benchmark Report ===")
        print(tabulate(summary, headers=["Provider", "Average TTFA (s)"], tablefmt="github", showindex=False))
    
if __name__ == "__main__":
    main()
