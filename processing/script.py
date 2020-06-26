import numpy as np
import rasterio as rio
import random, string
import matplotlib.pyplot as plt


class Data:

    def __init__(self, band_gre, band_nir, band_red, band_reg):

        self.band_gre = rio.open(band_gre)
        self.band_nir = rio.open(band_nir)
        self.band_red = rio.open(band_red)
        self.band_reg = rio.open(band_reg)
        self.gre_float = 0
        self.nir_float = 0
        self.red_float = 0
        self.reg_float = 0

    def init_data(self):

        self.gre_float = self.band_gre.read(1).astype('float64')
        self.nir_float = self.band_nir.read(1).astype('float64')
        self.red_float = self.band_red.read(1).astype('float64')
        self.reg_float = self.band_reg.read(1).astype('float64')

    def calculate_ndvi(self):

        self.init_data();

        ndvi = np.where(
            (self.nir_float + self.red_float) == 0.,
            0,
            (self.nir_float - self.red_float) / (self.nir_float + self.red_float))

        min = np.min(ndvi)
        max = np.max(ndvi)

        img_height = self.band_red.height
        img_width = self.band_red.width

        path = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        half_path = 'processed_shots/NDVI/' + path + '_ndvi.jpg'
        full_path = 'farm/media/processed_shots/NDVI/' + path + '_ndvi.jpg'

        plt.imsave(full_path, ndvi, cmap='RdYlGn')

        return half_path

    def calculate_ndre(self):

        self.init_data();

        ndre = ((self.nir_float - self.reg_float) / (self.nir_float + self.reg_float))

        min = np.min(ndre)
        max = np.max(ndre)

        path = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        half_path = 'processed_shots/NDRE/' + path + '_ndre.jpg'
        full_path = 'farm/media/processed_shots/NDRE/' + path + '_ndre.jpg'

        plt.imsave(full_path, ndre, cmap='RdYlGn')

        return half_path

    def calculate_grvi(self):

        self.init_data();

        grvi = np.where(
            (self.nir_float + self.gre_float) == 0.,
            0,
            (self.nir_float / self.gre_float))

        path = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        half_path = 'processed_shots/GRVI/' + path + '_grvi.jpg'
        full_path = 'farm/media/processed_shots/GRVI/' + path + '_grvi.jpg'

        plt.imsave(full_path, grvi, cmap='RdYlGn')

        return half_path

    def calculate_gci(self):

        self.init_data();

        gci = ((self.nir_float / self.gre_float) - 1)

        path = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        half_path = 'processed_shots/GCI/' + path + '_GCI.jpg'
        full_path = 'farm/media/processed_shots/GCI/' + path + '_GCI.jpg'

        plt.imsave(full_path, gci, cmap='RdYlGn')

        return half_path


# def calculate_ndvi(red, nir):
#     ndvi = np.where(
#         (nir+red)==0.,
#         0,
#         (nir-red)/(nir+red))
#
#     min = np.min(ndvi)
#     max = np.max(ndvi)
#
#     ndviImage = rio.open('output/ndvi.tif',
#                          'w',
#                          driver='Gtiff',
#                          width=img_width,
#                          height=img_height,
#                          count=1, crs=band_red.crs,
#                          transform=band_red.transform,
#                          dtype='float64')
#
#     ndviImage.write(ndvi, 1)
#     ndviImage.close()
#
#     ndvi = rio.open('output/ndvi.tif')
#     plt.imshow(ndvi.read(1), vmin=min, vmax=max, cmap='RdYlGn')
#     plt.colorbar()
#     plt.show()



#
# def calculate_grvi(gre, nir):
#     grvi = np.where(
#             (nir + gre) == 0.,
#             0,
#             (nir / gre))
#
#     min = np.min(grvi)
#     max = np.max(grvi)
#
#     grviImage = rio.open('output/grvi.tif',
#                          'w',
#                          driver='Gtiff',
#                          width=img_width,
#                          height=img_height,
#                          count=1, crs=band_red.crs,
#                          transform=band_red.transform,
#                          dtype='float64')
#
#     grviImage.write(grvi, 1)
#     grviImage.close()
#
#     grvi = rio.open('output/grvi.tif')
#     plt.imshow(grvi.read(1), vmin=min, vmax=max, cmap='RdYlGn')
#     plt.colorbar()
#     plt.show()
#
# def calculate_gci(gre, nir):
#     gci = ((nir / gre) - 1)
#
#     min = np.min(gci)
#     max = np.max(gci)
#
#     gciImage = rio.open('output/gci.tif',
#                          'w',
#                          driver='Gtiff',
#                          width=img_width,
#                          height=img_height,
#                          count=1, crs=band_red.crs,
#                          transform=band_red.transform,
#                          dtype='float64')
#
#     gciImage.write(gci, 1)
#     gciImage.close()
#
#     gci = rio.open('output/gci.tif')
#     plt.imshow(gci.read(1), vmin=min, vmax=max, cmap='RdYlGn')
#     plt.colorbar()
#     plt.show()
#
# def calculate_ndre(reg, nir):
#     ndre = ((nir - reg) / (nir + reg))
#
#     min = np.min(ndre)
#     max = np.max(ndre)
#
#     ndreImage = rio.open('output/ndre.tif',
#                          'w',
#                          driver='Gtiff',
#                          width=img_width,
#                          height=img_height,
#                          count=1, crs=band_red.crs,
#                          transform=band_red.transform,
#                          dtype='float64')
#
#     ndreImage.write(ndre, 1)
#     ndreImage.close()
#
#     ndre = rio.open('output/ndre.tif')
#     plt.imshow(ndre.read(1), vmin=min, vmax=max, cmap='RdYlGn')
#     plt.colorbar()
#     plt.show()


# calculate_ndvi(red, nir)
# calculate_ndre(reg, nir)
# calculate_gci(gre, nir)
# calculate_grvi(gre, nir)