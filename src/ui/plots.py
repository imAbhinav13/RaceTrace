import numpy as np
import plotly.graph_objects as go

def build_comparison_figure(driver_dfs, delta_df=None):
    
    
    fig = go.Figure()

    for driver_name, df in driver_dfs.items():
        # Ensure Delta aligns with the driver DataFrame
        if delta_df is not None and len(delta_df) == len(df):
            delta = delta_df["Delta"].values
        else:
            delta = np.zeros(len(df))
        
        customdata = np.stack([
            df.get("Throttle", np.zeros(len(df))),
            df.get("Brake", np.zeros(len(df))),
            df.get("nGear", np.zeros(len(df))),
            df.get("DRS", np.zeros(len(df))),
            delta
        ], axis=-1)

        fig.add_trace(go.Scatter(
            x=df["Distance"],
            y=df["Speed"],
            mode='lines',
            name=f"{driver_name} Speed",
            customdata=customdata,
            hovertemplate=(
                f"<b>{driver_name}</b><br>" +
                "Distance: %{x:.2f} m<br>" +
                "Speed: %{y:.2f} km/h<br>" +
                "Throttle: %{customdata[0]:.1f}%  " +
                "Brake: %{customdata[1]:.1f}%<br>" +
                "Gear: %{customdata[2]}  " +
                "DRS: %{customdata[3]}<br>" +
                "Delta: %{customdata[4]:.3f} s<extra></extra>"
            )
        ))

    fig.update_layout(
        title="Driver Lap Comparison",
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)",
        hovermode="x unified",
        hoverlabel=dict(
            font_size=12,
            bgcolor="white",
            bordercolor="black"
        ),
        width=1200,
        height=600
    )

    fig.show()