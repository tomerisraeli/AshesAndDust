import logging

from matplotlib import pyplot as plt

from DataBase.DBConstants import DBConstants
from main import AshesAndDust
import matplotlib.image as mpimg

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

    app = AshesAndDust("/Users/tomerisraeli/Documents/GitHub/AshesAndDust/configuration.ini")
    app.update_data_base()

    f, axarr = plt.subplots(1, 3, sharex="all", sharey="all")
    dist_to_water_data = app.get_spatial_data(DBConstants.VAR_DTWB)
    elevation_data = app.get_spatial_data(DBConstants.VAR_ELEV)

    axarr[0].imshow(dist_to_water_data.data[0])
    axarr[0].set_title("distance to major water bodies")
    axarr[1].imshow(elevation_data.data[0], vmax=3000, vmin=-500)
    axarr[1].set_title("elevation in meters")

    img = mpimg.imread("israel_sat_img.jpg")
    axarr[2].imshow(img)

    plt.show()
