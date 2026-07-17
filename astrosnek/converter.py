import rawpy
from astropy.io import fits

def convert_arw_to_fits(arw_path, fits_path, lens_name="Unknown"):
    """
    Unpacks a single raw Sony camera file and saves it into 
    astronomical FITS format.
    """
    # 1. Read raw from sensor
    with rawpy.imread(arw_path) as raw:
        # Extract the raw bayer data array directly as floating points
        raw_image = raw.raw_image.astype('float32')

    # 2. Create a standard primary HDU (Header Data Unit) for Astropy
    hdu = fits.PrimaryHDU(raw_image)

    # 3. Populate the FITS Header metadata for data logging
    hdu.header['TELESCOP'] = 'State Tripod'
    hdu.header['INSTRUME'] = 'Sony a7s'
    hdu.header['LENS'] = (lens_name, 'Manual lens')
    hdu.header['COMMENT'] = 'First field test data from July 4th'

    # 4. Write clean FITS file to drive
    hdu.writeto(fits_path, overwrite=True)
    print(f"Successfully converted {arw_path} to FITS: {fits_path}")

    # Uncomment below to test
    # if __name__ == "__main__":
    #   convert_arw_to_fits("input.ARW", "output.fits", "SLR Magic 35mm")