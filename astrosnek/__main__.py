import argparse
from astrosnek.pipeline import Pipeline
from astrosnek.config import (
    BASE_DIR,
    RAW_DIR,
    FITS_DIR,
    STACKED_DIR,
    RESULTS_DIR,
    ensure_directories,
    load_or_create_config,
)

def main():
    args = parse_arguments()
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
    if args.viewer is not None:
        viewer_modes = {
            "every": 1,
            "best": 2,
            "none": 3,
        }
        config["viewer_mode"] = viewer_modes[args.viewer]
    Pipeline(config).run()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Astrosnek astronomical image pipeline"
    )

    parser.add_argument(
        "--viewer",
        choices=["every", "best", "none"],
        help="Viewer mode for this run."
    )

    return parser.parse_args()

if __name__ == "__main__":
    main()