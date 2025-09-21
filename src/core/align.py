import numpy as np
import pandas as pd
import warnings



def resample_by_distance(df: pd.DataFrame, n_points: int = 800) -> pd.DataFrame:
    
    if 'Distance' not in df.columns:        #Check if Distance exists--> X-axis of Distance traveled (in meters). -->If missing → stop and raise error.
        raise ValueError("Telemetry dataframe must have a 'Distance' column")
    
    distance_new = np.linspace(df['Distance'].min(), df['Distance'].max(), n_points)
    df_resampled = pd.DataFrame({'Distance': distance_new})

    for col in df.columns:
        if col == "Distance":
            continue

        # Special handling for Time column
        if col == "Time":
            # Convert to seconds if timedelta
            if pd.api.types.is_timedelta64_dtype(df[col]):
                df_col = df[col].dt.total_seconds()
            else:
                df_col = df[col]
            df_resampled[col] = np.interp(distance_new, df['Distance'], df_col)
            continue

        # Special handling for Brake (boolean to float 0/1) 
        if col == "Brake":
            try:
                df_col = df[col].astype(float)   # Convert True/False tp 1.0/0.0
                df_resampled[col] = np.interp(distance_new, df['Distance'], df_col)
            except Exception as e:
                warnings.warn(f"Could not process 'Brake': {e}")
            continue


        if np.issubdtype(df[col].dtype, np.number):
            
            try:
                df_resampled[col] = np.interp(distance_new, df['Distance'], df[col]) # doing interpolation = estimating values between known data points.
                                                                                    #np.interp(x_new, x_old, y_old) bacailly cal new 

                # special case for gear → round + int
                if col == "nGear":
                    df_resampled[col] = df_resampled[col].round().astype(int)
                                                                                  
            except Exception as e:
                warnings.warn(f"Could not interpolate column '{col}': {e}")
        else:
            warnings.warn(f"Skipping non-numeric column '{col}'")

    # Explicit fallback: if Brake/Throttle missing
    for col in ["Throttle", "Brake"]:   
        if col not in df.columns:
            warnings.warn(f"Missing column '{col}', continuing without it")

    return df_resampled
