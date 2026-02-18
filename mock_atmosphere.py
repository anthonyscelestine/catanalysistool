import numpy as np

def get_mock_profile(lat, lon):

    levels = np.linspace(200, 400, 20)  # pressure levels (hPa)

    jet = 20 * np.exp(-((levels - 250)**2)/(2*(20**2)))

    horizontal_variation = 5 * np.sin(lat/5) * np.cos(lon/5)

    wind_speed = 30 + jet + horizontal_variation

    shear = np.gradient(wind_speed, levels)

    return levels, shear
