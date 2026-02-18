import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def pressure_to_altitude(pressure_hpa):
    return 44330 * (1 - (pressure_hpa / 1013.25)**0.1903)



# 1️⃣ Vertical Profile
def plot_vertical_profile(levels, probability):

    altitude = pressure_to_altitude(levels)

    fig, ax = plt.subplots(figsize=(5,7))

    ax.plot(probability, altitude, marker="o")

    ax.set_xlabel("Turbulence Probability")
    ax.set_ylabel("Altitude (m)")
    ax.set_title("Vertical Turbulence Profile")

    ax.grid(True)

    st.pyplot(fig)


# 2️⃣ Route Distance Plot
def plot_route_probability(route, cruise_index, turbulence_matrix):

    fig, ax = plt.subplots(figsize=(8,4))

    distance = route["distance"]
    cruise_prob = turbulence_matrix[cruise_index, :]

    ax.plot(distance, cruise_prob, linewidth=2)

    ax.set_xlabel("Normalized Distance Along Route")
    ax.set_ylabel("Turbulence Probability")
    ax.set_title("Turbulence Along Route at Cruise Level")

    ax.grid(True)

    st.pyplot(fig)


# 3️⃣ Contour Cross-Section
def plot_route_contour(route, altitude_levels, turbulence_matrix):

    fig, ax = plt.subplots(figsize=(10,6))

    X = route["distance"]
    Y = pressure_to_altitude(altitude_levels)


    contour = ax.contourf(X, Y, turbulence_matrix, levels=20)

    fig.colorbar(contour, ax=ax, label="Turbulence Probability")

    ax.set_xlabel("Normalized Distance Along Route")
    ax.set_ylabel("Altitude (m)")
    ax.set_title("Turbulence Cross-Section Along Flight Route")

    ax.invert_yaxis()

    st.pyplot(fig)
