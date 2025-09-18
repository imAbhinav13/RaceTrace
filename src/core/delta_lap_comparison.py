import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

def lap_delta(driver1_df:pd.DataFrame,driver2_df:pd.DataFrame)-> pd.DataFrame:
    
    # Done to make sure Time is in seconds
    for df in [driver1_df, driver2_df]:
        if pd.api.types.is_timedelta64_dtype(df["Time"]):
            df["Time"] = df["Time"].dt.total_seconds()

    # Merge compare lap onto base lap by nearest Distance
    merged = pd.merge_asof(
        driver1_df.sort_values("Distance"),
        driver2_df.sort_values("Distance"),
        on="Distance",
        suffixes=("_base", "_compare")
    )

    # Compute delta
    merged["Delta"] = merged["Time_compare"] - merged["Time_base"]

    return merged[["Distance", "Time_base", "Time_compare", "Delta"]].rename(
    columns={"Time_base": "Driver1", "Time_compare": "Driver2"}
    )