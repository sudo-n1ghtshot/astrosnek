import os
import json

RESULTS_DIR = r"\\10.0.0.28\Dumpster\Python\Astro\Analysis-results"

def load_results():
    """
    Loads all JSON analysis files from the results folder.
    """
    results = []
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(
                RESULTS_DIR,
                filename
            )
            with open(filepath, "r") as f:
                data = json.load(f)
            results.append(data)
    return results
def print_report(results):
    """
    Prints a ranked quality report.
    """
    if not results:
        print("No analysis files found.")
        return
    # Rank by quality score
    results.sort(
        key=lambda x: x["quality_score"],
        reverse=True
    )
    print("\n=============================")
    print("ASTRO FRAME QUALITY REPORT")
    print("=============================\n")
    print(
        f"{'Rank':<6}"
        f"{'Frame':<18}"
        f"{'Stars':<10}"
        f"{'Noise':<12}"
        f"{'Sharp':<12}"
        f"{'Score':<12}"
    )
    print("-" * 70)

    for index, frame in enumerate(results, start=1):
        filename = os.path.basename(
            frame["file"]
        )
        print(
            f"{index:<6}"
            f"{filename:<18}"
            f"{frame['stars_detected']:<10}"
            f"{frame['background_noise']:<12.2f}"
            f"{frame['median_sharpness']:<12.3f}"
            f"{frame['quality_score']:<12.3f}"
        )
    # Best frame summary
    best = results[0]

    print("\n=============================")
    print("BEST FRAME")
    print("=============================")
    print(
        f"File: {best['file']}"
    )
    print(
        f"Stars detected: {best['stars_detected']}"
    )
    print(
        f"Noise floor: {best['background_noise']:.2f}"
    )
    print(
        f"Sharpness: {best['median_sharpness']:.3f}"
    )
    print(
        f"Quality score: {best['quality_score']:.3f}"
    )
    print("=============================")

if __name__ == "__main__":
    results = load_results()
    print_report(results)