import numpy as np
from astropy.io import fits

def median_stack_images(fits_path_list, output_path):
    """
    Stacks a list of aligned FITS arrays using a 
    median filter to maximize signal-to-noise ratio
    """
    if not fits_path_list:
        print("[STACKING ERROR] Image list is empty.")
        return
    
    print(f"Beginning integration of {len(fits_path_list)} frames.")

    # 1. Load the first image to get dimensions and base header metadata
    with fits.open(fits_path_list[0]) as hdul:
        base_header = hdul.header
        img_shape = hdul.data.shape

    # 2. Initialize an empty 3D array (cube) to hold all individual files
    image_cube = np.zeros((len(fits_path_list), img_shape[0], img_shape[1]), dtype=np.float64)

    # 3. Populat data cube
    for idx, path in enumerate(fits_path_list):
        with fits.open(path) as hdul:
            image_cube[idx, :, :,] = hdul.data

    # 4. Execute the median stack across the 3D depth axis
    # Median is preferred over mean as it automatically deletes satellite trails
    stacked_data = np.median(image_cube, axis=0)

    # 5. Update header info and save the clean integrated master image
    base_header['STACKED'] = (len(fits_path_list), 'Total frames integrated')
    new_hdu = fits.PrimaryHDU(data=stacked_data, header=base_header)
    new_hdu.writeto(output_path, overwrite=True)

    print(f"===========================================")
    print(f"[SUCCESS] Final Stack Complete.")
    print(f"Master file saved at: {output_path}")
    print(f"===========================================")