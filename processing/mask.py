import os
import cv2
import copy
import numpy as np
import rasterio as rio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import urllib, base64, io

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Mask:

    def __init__(self, band_nir, band_red):
        self.band_nir = rio.open(os.path.join(BASE_DIR, band_nir))
        self.band_red = rio.open(os.path.join(BASE_DIR, band_red))
        self.nir = self.band_nir.read(1).astype('float64')
        self.red = self.band_red.read(1).astype('float64')
        self.ndvi = np.divide((self.nir-self.red), (self.nir+self.red))
        self.blur = ''

    def blur_data(self):
        self.blur = cv2.GaussianBlur(self.ndvi, (5, 5), 0)

    def green_threshold(self):
        self.blur_data()

        self.blur[self.ndvi > -0.39] = np.nan

        plt.imshow(self.blur, cmap="RdYlGn")
        # plt.colorbar()

        fig = plt.gcf()
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        string = base64.b64encode(buffer.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(string)

        plt.clf()

        return {'title': '', 'uri': uri,
                'desc': 'Indicates the unhealthy, barren, and pesticide required areas of the farm. '
                                                 'The red is the indicator of the absence of green.'}

    def red_threshold(self):
        self.blur_data()

        self.blur[self.ndvi < -0.15] = np.nan

        plt.imshow(self.blur, cmap="RdYlGn")
        # plt.colorbar()

        fig = plt.gcf()
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        string = base64.b64encode(buffer.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(string)

        plt.clf()

        return {'title': '', 'uri': uri, 'desc': 'Shows the green in the field with lighter and darker patches that may require water and futher care.'}

