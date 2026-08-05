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
    Pipeline(config).run()

if __name__ == "__main__":
    main()