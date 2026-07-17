import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import LogStretch, PercentileInterval
from astropy.visualization.mpl_normalize import ImageNormalize

def inspect_and_plot_fits(fits_path):
    """
    Applies a scientific log stretch to linear pixel data
    and plots the image visually.
    """
    with fits.open(fits_path) as hdul:
        data = hdul[0].data.astype(float)
        header = hdul[0].header.copy()

    # Clip extreme pixels for better display
    interval = PercentileInterval(99.5)
    vmin, vmax = interval.get_limits(data)

    # Apply logarithmic stretch
    norm = ImageNormalize(
        data,
        vmin=vmin,
        vmax=vmax,
        stretch=LogStretch()
    )

    plt.figure(figsize=(10, 8))
    plt.imshow(data, cmap="gray", origin="lower", norm=norm)
    plt.colorbar(label="Pixel Value (Intensity)")
    plt.title(f"Astro View: {header.get('LENS', 'Unknown Lens')} | {fits_path}")
    plt.xlabel("X Pixels")
    plt.ylabel("Y Pixels")

    print("Star map window opened. Close plot window to resume terminal.")
    plt.show(block=False)      # Show without blocking the script
    plt.pause(3)               # Wait 3 seconds

    # If the window is still open, close it automatically
    if plt.fignum_exists(plt.gcf().number):
        plt.close()