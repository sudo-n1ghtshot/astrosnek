import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.visualization import LogStretch, PercentileInterval
from astropy.visualization.mpl_normalize import ImageNormalize

def inspect_and_plot_fits(
    fits_path,
    output_path=None,
    show=True
):
    """
    Display and/or save a scientific visualization
    of a FITS image using a logarithmic stretch.
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
    plt.imshow(
        data,
        cmap="gray",
        origin="lower",
        norm=norm
    )
    plt.colorbar(
        label="Pixel Value (Intensity)"
    )
    plt.title(
        f"Astro View: "
        f"{header.get('LENS', 'Unknown Lens')} | "
        f"{fits_path}"
    )
    plt.xlabel("X Pixels")
    plt.ylabel("Y Pixels")
    # Save the visualization if requested
    if output_path:
        plt.savefig(
            output_path,
            dpi=150,
            bbox_inches="tight"
        )
        print(f"Saved viewer image: {output_path}")
    # Display interactively if requested
    if show:
        print(
            "Star map window opened. "
            "Close plot window to resume terminal."
        )
        plt.show(block=False)
        plt.pause(3)
    plt.close()