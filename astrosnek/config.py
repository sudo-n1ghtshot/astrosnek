import os
import json


# =============================
# Project Directory Setup
# =============================
PACKAGE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
BASE_DIR = os.path.dirname(PACKAGE_DIR)

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

def ensure_directories():
    directories_created = False
    for directory in REQUIRED_DIRS:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
            directories_created = True

    if directories_created:
        print("\n=============================")
        print("INITIAL SETUP COMPLETE")
        print("=============================")
        print(
            "Add your .ARW files into RAW folder"
        )
        print(
            "\nPlease re-run:"
        )
        print(
            "docker compose run --rm astrosnek"
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

