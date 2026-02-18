import numpy as np

def get_mock_profile(lat, lon):

    levels = np.linspace(200, 400, 25)
    altitude = 44330 * (1 - (levels / 1013.25)**0.1903)

    # Jet core shifts slightly with latitude
    jet_center = 11000 + 500*np.sin(lat/10)

    turbulence_band = np.exp(-((altitude - jet_center)**2)/(2*(800**2)))

    # Add longitude variation
    horizontal_factor = 1 + 0.3*np.cos(lon/10)

    wind_speed = 40 + 30 * turbulence_band * horizontal_factor

    shear = np.gradient(wind_speed, levels)

    return levels, shear
