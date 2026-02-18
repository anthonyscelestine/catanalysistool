import plotly.graph_objects as go

def plot_flight_map(lat1, lon1, lat2, lon2):

    fig = go.Figure()

    # Departure Marker
    fig.add_trace(go.Scattermapbox(
        lat=[lat1],
        lon=[lon1],
        mode='markers+text',
        marker=dict(size=12, color='blue'),
        text=["Departure"],
        textposition="top right"
    ))

    # Arrival Marker
    fig.add_trace(go.Scattermapbox(
        lat=[lat2],
        lon=[lon2],
        mode='markers+text',
        marker=dict(size=12, color='green'),
        text=["Arrival"],
        textposition="top right"
    ))

    # Route Line
    fig.add_trace(go.Scattermapbox(
        lat=[lat1, lat2],
        lon=[lon1, lon2],
        mode='lines',
        line=dict(width=3, color='red')
    ))

    fig.update_layout(
    mapbox=dict(
        style="carto-positron-nolabels",
        zoom=4,
        center=dict(
            lat=(lat1 + lat2) / 2,
            lon=(lon1 + lon2) / 2
        )
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)


    return fig
