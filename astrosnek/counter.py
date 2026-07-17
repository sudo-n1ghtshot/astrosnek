import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder

def count_sharp_stars(fits_path):
    """
    Calculates image quality metrics:
    - star count
    - background noise
    - median star sharpness
    - median star brightness
    """
    with fits.open(fits_path) as hdul:
        data = hdul[0].data.astype(np.float64)
    # Calculate background noise floor
    mean, median, std = sigma_clipped_stats(
        data,
        sigma=3.0
    )
    # Find stars
    daofind = DAOStarFinder(
        fwhm=3.0,
        threshold=5.0 * std
    )
    sources = daofind(data - median)

    if sources is None:
        print(f"[ANALYSIS] {fits_path}: 0 stars detected.")
        return {
            "stars_detected": 0,
            "background_noise": float(std),
            "median_sharpness": 0,
            "median_brightness": 0,
            "quality_score": 0
        }

    star_count = len(sources)

    # DAOStarFinder measurements
    sharpness = np.median(
        sources["sharpness"]
    )
    brightness = np.median(
        sources["flux"]
    )

    # Simple quality metric
    # rewards stars, penalizes noise
    quality_score = (
        star_count * sharpness
    ) / std

    print("\n=============================")
    print(f"FILE: {fits_path}")
    print(f"Stars Detected: {star_count}")
    print(f"Noise Floor: {std:.2f}")
    print(f"Median Sharpness: {sharpness:.3f}")
    print(f"Median Brightness: {brightness:.2f}")
    print(f"Quality Score: {quality_score:.3f}")
    print("=============================")

    return {
        "stars_detected": star_count,
        "background_noise": float(std),
        "median_sharpness": float(sharpness),
        "median_brightness": float(brightness),
        "quality_score": float(quality_score)
    }