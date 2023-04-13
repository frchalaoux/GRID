def read_jpg(filename):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 1e+9
    return np.array(Image.open(filename)).astype(np.uint8)


def read_tiff(filename, bands=None, xBSize=5000, yBSize=5000):
    '''import'''
    import gdal
    from tqdm import tqdm_gui
    '''program'''
    ds = gdal.Open(filename)
    gdal.UseExceptions()
    nrow = ds.RasterYSize
    ncol = ds.RasterXSize
    if bands is None:
        bands = range(ds.RasterCount)
    data = np.zeros((nrow, ncol, len(bands)))
    for b in bands:
        band = ds.GetRasterBand(b+1)
        for i in tqdm_gui(range(0, nrow, yBSize), desc="Channel %d/%d" % (b, len(bands)-1), leave=False):
            numRows = yBSize if i + yBSize < nrow else nrow - i
            for j in range(0, ncol, xBSize):
                numCols = xBSize if j + xBSize < ncol else ncol - j
                data[i:(i+numRows), j:(j+numCols),
                     b] = band.ReadAsArray(j, i, numCols, numRows)
    return data.astype(np.uint8)


def write_tiff(array, outname):
    driver = gdal.GetDriverByName("GTiff")
    out_info = driver.Create(
        f"{outname}.tif",
        array.shape[1],
        array.shape[0],
        array.shape[2],
        gdal.GDT_Byte,
    )
    for i in range(array.shape[2]):
        out_info.GetRasterBand(i+1).WriteArray(array[:, :, i])
