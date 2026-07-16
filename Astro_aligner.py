import numpy as np
from astropy.io import fits
from scipy.ndimage import shift
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder

def align_target_to_reference(ref_path, target_path, output_path):
    """
    Finds the bright star offset between two images and mathmatically
    shifts the target image array to align perfectly with the reference
    """
    # 1. Load image arrays
    with fits.open(ref_path) as h_ref:
        ref_data = h_ref.data.astype(np.float64)
    with fits.open(target_path) as h_tar:
        tar_data = h_tar.data.astype(np.float64)
        tar_header = h_tar.header

    # 2. Extract background stats and locate stars in both frame
    _, _, ref_std = sigma_clipped_stats(ref_data, sigma=3.0)
    _, _, ref_std = sigma_clipped_stats(ref_data, sigma=3.0)

    finder = DAOStarFinder(fwhm=3.0, threshold=10.0 * ref_std)
    ref_srcs = finder(ref_data)
    tar_srcs = finder(tar_data)

    if ref_srcs is None or tar_srcs is None:
        print("[ALIGNMENT ERROR] could not find enough anchor stars.")
        return False
    
    # 3. Use the brightest detected star to calculate the pixel drift offset
    ref_x, ref_y = ref_srcs['xcentroid'][0], ref_srcs['ycentroid'][0]
    tar_x, tar_y = tar_srcs['xcentroid'][0], tar_srcs['ycentroid'][0]

    shift_x = ref_x - tar_x
    shift_y = ref_y - tar_y

    # 4. Mathematically shift the pixel grid using Scipy
    aligned_data = shift(tar_data, shif=[shift_y, shift_x], cval=0.0)

    # 5. Save the aligned file
    new_hdu = fits.PrimaryHDU(data=aligned_data,header=tar_header)
    new_hdu.writeto(output_path, overwrite=True)
    print(f"[ALIGNED] Shifted {target_path} by X: {shift_x:.1f}, Y: {shift_y:.1f}")
    return True
