import numpy as np
import pandas as pd

def generate_route(lat1, lon1, lat2, lon2, steps=60):

    latitudes = np.linspace(lat1, lat2, steps)
    longitudes = np.linspace(lon1, lon2, steps)

    distance = np.linspace(0, 1, steps)

    return pd.DataFrame({
        "lat": latitudes,
        "lon": longitudes,
        "distance": distance
    })
