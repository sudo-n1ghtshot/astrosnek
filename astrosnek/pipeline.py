import os
import json

from astrosnek.logger import get_logger
from astrosnek.converter import convert_arw_to_fits
from astrosnek.counter import count_sharp_stars
from astrosnek.viewer import inspect_and_plot_fits
from astrosnek.config import (
    RAW_DIR,
    FITS_DIR,
    RESULTS_DIR,
    VIEWER_DIR,
    wait_for_raw_files,
)

class Pipeline:
    def __init__(self, config):
        self.config = config
        self.logger = get_logger()

    def save_analysis_result(self, result):
        filename = (
            os.path.splitext(
                os.path.basename(result["file"])
            )[0]
            + ".json"
        )
        filepath = os.path.join(
            RESULTS_DIR,
            filename
        )
        with open(filepath, "w") as f:
            json.dump(result, f, indent=4)
        self.logger.info(
            f"Saved analysis: {filepath}"
        )

    def process_frame(self, arw_filename):
        base, _ = os.path.splitext(arw_filename)
        raw_file = os.path.join(
            RAW_DIR,
            arw_filename
        )
        fits_file = os.path.join(
            FITS_DIR,
            base + ".fits"
        )
        self.logger.info(
            f"Starting pipeline for: {arw_filename}"
        )
        
        if os.path.exists(fits_file):
            self.logger.info(
                "FITS exists, skipping conversion."
            )
        else:
            convert_arw_to_fits(
                raw_file,
                fits_file,
                self.config["lens"]
            )
        analysis = count_sharp_stars(fits_file)
        result = {
            "file": fits_file,
            "lens": self.config["lens"],
            **analysis
        }
        self.save_analysis_result(result)
        if self.config["viewer_mode"] == 1:
            viewer_file = os.path.join(
                VIEWER_DIR,
                base + ".png"
            )
            inspect_and_plot_fits(
                fits_file,
                output_path=viewer_file,
                show=True
            )
        return result

    def run(self):
        raw_files = wait_for_raw_files()
        results = []
        for filename in raw_files:
            results.append(
                self.process_frame(filename)
            )
        if not results:
            return
        best_frame = max(
            results,
            key=lambda x: x["quality_score"]
        )
        self.logger.info("Pipeline complete")
        self.logger.info(
            f"Best Frame: {best_frame['file']}"
        )
        self.logger.info(
            f"Stars detected: {best_frame['stars_detected']}"
        )
        self.logger.info(
            f"Quality score: {best_frame['quality_score']:.3f}"
        )
        if self.config["viewer_mode"] == 2:
            inspect_and_plot_fits(best_frame["file"])