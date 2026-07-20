import os
import json

from astrosnek.converter import convert_arw_to_fits
from astrosnek.counter import count_sharp_stars
from astrosnek.viewer import inspect_and_plot_fits
from astrosnek.config import (
    BASE_DIR,
    RAW_DIR,
    FITS_DIR,
    STACKED_DIR,
    RESULTS_DIR,
    ensure_directories,
    load_or_create_config,
    wait_for_raw_files,
)
# =============================
# Save Analysis Result
# =============================
def save_analysis_result(result):
    filename = os.path.splitext(
        os.path.basename(result["file"])
    )[0] + ".json"
    filepath = os.path.join(
        RESULTS_DIR,
        filename
    )
    with open(filepath, "w") as f:
        json.dump(
            result,
            f,
            indent=4
        )

    print(
        f"Saved analysis: {filepath}"
    )
# =============================
# Single Frame Pipeline
# =============================
def test_single_frame_pipeline(
        arw_filename,
        lens_name,
        viewer_mode):
    base, _ = os.path.splitext(
        arw_filename
    )
    raw_file = os.path.join(
        RAW_DIR,
        arw_filename
    )
    fits_file = os.path.join(
        FITS_DIR,
        base + ".fits"
    )
    print(
        f"\nSTARTING PIPELINE FOR: {arw_filename}"
    )

    if os.path.exists(fits_file):
        print(
            "FITS exists, skipping conversion."
        )
    
    else:
        convert_arw_to_fits(
            raw_file,
            fits_file,
            lens_name
        )
    analysis = count_sharp_stars(
        fits_file
    )

    result = {
        "file": fits_file,
        "lens": lens_name,
        **analysis
    }
    save_analysis_result(
        result
    )
    if viewer_mode == 1:
        inspect_and_plot_fits(
            fits_file
        )
    return result

# =============================
# Main Program
# =============================
def main():
    ensure_directories()
    print("\n=============================")
    print("ASTRO PIPELINE DIRECTORIES")
    print("=============================")
    print(f"BASE:    {BASE_DIR}")
    print(f"RAW:     {RAW_DIR}")
    print(f"FITS:    {FITS_DIR}")
    print(f"STACKED: {STACKED_DIR}")
    print(f"RESULTS: {RESULTS_DIR}")
    print("=============================\n")
    
    config = load_or_create_config()
    raw_files = wait_for_raw_files()
    results = []
    
    for filename in raw_files:
        result = test_single_frame_pipeline(
            filename,
            config["lens"],
            config["viewer_mode"]
        )
        results.append(
            result
        )
    if results:
        best_frame = max(
            results,
            key=lambda x: x["quality_score"]
        )
        print("\n=============================")
        print("PIPELINE COMPLETE")
        print("=============================")
        print(
            f"Best Frame: {best_frame['file']}"
        )
        print(
            f"Stars detected: {best_frame['stars_detected']}"
        )
        print(
            f"Quality score: {best_frame['quality_score']:.3f}"
        )
        print("=============================")

        if config["viewer_mode"] == 2:
            inspect_and_plot_fits(
                best_frame["file"]
            )

if __name__ == "__main__":
    main()