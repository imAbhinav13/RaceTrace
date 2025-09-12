#Extract telemetry (speed, throttle, brake, gear, rpm, drs) for a session.
# FastF1 provides laps and telemetry, but we create our own functions as it makes usage easier and in our required format.
#Functions to extract laps and telemetry data for a given session and driver.

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.core.align import resample_by_distance

#Return all laps of a given driver in the session.
def get_laps(session, driver_code:str):

    #extracting all the unique drivers from the laps happened in the session. (driver did atleast 1 lap) 
    valid_drivers=session.laps.Driver.unique()
    
    if driver_code not in valid_drivers:
        raise ValueError(f" Driver {driver_code} not found in this session.")

    #filtering laps only for that specific driver_code  
    driver_laps= session.laps[(session.laps.Driver==driver_code)]    
    if driver_laps.empty:
         raise ValueError(f"No laps found for driver {driver_code}")
    
    return driver_laps

#Return the fastest lap object of a given driver.
def fastest_lap(session,driver_code:str):
    
    driver_laps=get_laps(session, driver_code)

    fastest_lap=driver_laps.pick_fastest() #.LapTime canbe added at last to only get fastes time  #inbuilt fn of pick_fastest
    return fastest_lap


#Return resampled telemetry for all laps of a driver.
def get_telemetry_all_laps(session,driver_code:str): #for all laps

    driver_laps = get_laps(session, driver_code)
    all_telemetry = []

    for lap_number, lap in driver_laps.iterlaps():  # iterlaps() gives Lap objects
        lap_telemetry = lap.get_car_data().add_distance()# telemetry for this lap
        lap_telemetry = resample_by_distance(lap_telemetry) # resample along distance
        all_telemetry.append(lap_telemetry)

    return all_telemetry

#Return resampled telemetry for the driver's fastest lap.
def get_telemetry_fastest_lap(session,driver_code:str):
    
    driver_fastest_lap=fastest_lap(session,driver_code)
    fastest_lap_telemetry=driver_fastest_lap.get_car_data().add_distance()
    fastest_lap_telemetry=resample_by_distance(fastest_lap_telemetry)
    
    return fastest_lap_telemetry