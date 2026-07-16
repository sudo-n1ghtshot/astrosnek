import os
import json

from Astro_converter import convert_arw_to_fits
from Astro_counter import count_sharp_stars
from Astro_viewer import inspect_and_plot_fits

# =============================
# Project Directory Setup
# =============================
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
RAW_DIR = os.path.join(
    BASE_DIR,
    "RAW"
)
FITS_DIR = os.path.join(
    BASE_DIR,
    "FITS_converted"
)
STACKED_DIR = os.path.join(
    BASE_DIR,
    "FITS_stacked"
)
RESULTS_DIR = os.path.join(
    BASE_DIR,
    "Analysis_results"
)
CONFIG_FILE = os.path.join(
    BASE_DIR,
    "config.json"
)

print("\n=============================")
print("ASTRO PIPELINE DIRECTORIES")
print("=============================")
print(f"BASE:    {BASE_DIR}")
print(f"RAW:     {RAW_DIR}")
print(f"FITS:    {FITS_DIR}")
print(f"STACKED: {STACKED_DIR}")
print(f"RESULTS: {RESULTS_DIR}")
print("=============================\n")

# =============================
# Create Required Directories
# =============================
REQUIRED_DIRS = [
    RAW_DIR,
    FITS_DIR,
    STACKED_DIR,
    RESULTS_DIR
]
directories_created = False

for directory in REQUIRED_DIRS:
    if not os.path.exists(directory):
        os.makedirs(directory)
        directories_created = True
        print(
            f"Created directory: {directory}"
        )

if directories_created:
    print("\n=============================")
    print("INITIAL SETUP COMPLETE")
    print("=============================")
    print(
        "Please place your ARW files into:"
    )
    print(
        RAW_DIR
    )
    print(
        "\nPlease run run_pipeline.py again."
    )
    input(
        "\nPress ENTER to exit..."
    )
    exit()

# =============================
# Configuration Handling
# =============================
def load_or_create_config():
    """
    Loads existing configuration.
    Creates one on first run.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        print("\nLoaded configuration:")
        print(
            f"Camera: {config['camera']}"
        )
        print(
            f"Lens: {config['lens']}"
        )
        return config

    print("\n=============================")
    print("ASTRO PIPELINE FIRST RUN SETUP")
    print("=============================")

    camera = input(
        "Camera model: "
    )
    lens = input(
        "Lens name: "
    )
    print("\nViewer Mode")
    print("1 - Open every frame")
    print("2 - Open best frame only")
    print("3 - No viewer")
    viewer_mode = input(
        "Selection: "
    )
    config = {
        "camera": camera,
        "lens": lens,
        "viewer_mode": int(viewer_mode)
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(
            config,
            f,
            indent=4
        )
    print(
        f"\nConfiguration saved:"
        f"\n{CONFIG_FILE}"
    )
    return config

# =============================
# RAW File Discovery
# =============================
def find_raw_files():
    """
    Finds ARW files in RAW folder.
    """
    raw_files = []

    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith(".arw"):
            raw_files.append(filename)
    raw_files.sort()
    print(
        f"\nFound {len(raw_files)} RAW files."
    )
    return raw_files

# =============================
# Wait For RAW Files
# =============================
def wait_for_raw_files():
    """
    Waits until RAW folder contains images.
    """
    while True:
        raw_files = find_raw_files()
        if len(raw_files) > 0:
            return raw_files

        print("\n=============================")
        print("NO RAW FILES FOUND")
        print("=============================")
        print(
            "Copy ARW files into:"
        )
        print(
            RAW_DIR
        )
        input(
            "\nPress ENTER after files are added..."
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
if __name__ == "__main__":
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