import streamlit as st
import numpy as np
import plotly.graph_objects as go

from src.route import generate_route
from src.mock_atmosphere import get_mock_profile
from src.turbulence import shear_to_probability
from src.visualization import (
    plot_vertical_profile,
    plot_route_probability,
    plot_route_contour
)

# -------------------------------------
# Page Config
# -------------------------------------
st.set_page_config(layout="wide")
st.title("Clear-Air Turbulence Analysis Dashboard")

st.markdown(
    "This tool analyzes potential clear-air turbulence "
    "along a user-defined flight route."
)

# -------------------------------------
# User Inputs
# -------------------------------------
col1, col2 = st.columns(2)

with col1:
    lat1 = st.number_input("Departure Latitude", value=13.0)
    lon1 = st.number_input("Departure Longitude", value=80.0)

with col2:
    lat2 = st.number_input("Arrival Latitude", value=19.0)
    lon2 = st.number_input("Arrival Longitude", value=72.0)


# -------------------------------------
# Flight Map Visualization
# -------------------------------------
def plot_flight_map(lat1, lon1, lat2, lon2):

    fig = go.Figure()

    # Departure marker
    fig.add_trace(go.Scattermapbox(
        lat=[lat1],
        lon=[lon1],
        mode='markers+text',
        marker=dict(size=12, color='blue'),
        text=["Departure"],
        textposition="top right"
    ))

    # Arrival marker
    fig.add_trace(go.Scattermapbox(
        lat=[lat2],
        lon=[lon2],
        mode='markers+text',
        marker=dict(size=12, color='green'),
        text=["Arrival"],
        textposition="top right"
    ))

    # Route line
    fig.add_trace(go.Scattermapbox(
        lat=[lat1, lat2],
        lon=[lon1, lon2],
        mode='lines',
        line=dict(width=3, color='red')
    ))

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            zoom=4,
            center=dict(
                lat=(lat1 + lat2) / 2,
                lon=(lon1 + lon2) / 2
            )
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig


st.subheader("Flight Route Overview")
map_fig = plot_flight_map(lat1, lon1, lat2, lon2)
st.plotly_chart(map_fig, use_container_width=True)


# -------------------------------------
# Turbulence Analysis
# -------------------------------------
if st.button("Analyze Turbulence"):

    route = generate_route(lat1, lon1, lat2, lon2)

    altitude_levels = None
    turbulence_matrix = []

    for _, row in route.iterrows():

        levels, shear = get_mock_profile(row["lat"], row["lon"])
        prob = shear_to_probability(shear)

        turbulence_matrix.append(prob)

        if altitude_levels is None:
            altitude_levels = levels

    turbulence_matrix = np.array(turbulence_matrix).T

    # ---------------------------------
    # Pressure to Altitude Conversion
    # ---------------------------------
    def pressure_to_altitude(pressure_hpa):
        return 44330 * (1 - (pressure_hpa / 1013.25)**0.1903)

    altitudes = pressure_to_altitude(altitude_levels)

    # ---------------------------------
    # Recommended Cruise Altitude
    # ---------------------------------
    mean_turbulence = turbulence_matrix.mean(axis=1)

    optimal_index = np.argmin(mean_turbulence)
    recommended_altitude = altitudes[optimal_index]
    recommended_probability = mean_turbulence[optimal_index]

    st.subheader("Recommended Cruise Altitude")

    st.success(
        f"Recommended altitude for minimum turbulence: "
        f"{recommended_altitude:.0f} meters "
        f"(Mean turbulence probability: {recommended_probability:.2f})"
    )

    st.markdown("---")

    # ---------------------------------
    # Plots
    # ---------------------------------

    colA, colB = st.columns(2)

    # 1️⃣ Vertical Profile (Mid Route)
    with colA:
        mid_index = len(route) // 2
        plot_vertical_profile(
            altitude_levels,
            turbulence_matrix[:, mid_index]
        )

    # 2️⃣ Route Probability at Cruise Level
    with colB:
        cruise_index = len(altitude_levels) // 2
        plot_route_probability(
            route,
            cruise_index,
            turbulence_matrix
        )

    # 3️⃣ Full Contour Cross Section
    st.subheader("Turbulence Cross-Section")
    plot_route_contour(
        route,
        altitude_levels,
        turbulence_matrix
    )
