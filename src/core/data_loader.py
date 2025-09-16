import os
import fastf1

def enable_cache(cache_dir="data/cache"): 
    # Ensure the folder exists
    os.makedirs(cache_dir, exist_ok=True)   
    fastf1.Cache.enable_cache(cache_dir)    

def get_session(year, gp,session_type):     
    enable_cache()                        
    session = fastf1.get_session(year, gp, session_type) 
    session.load()
    return session

    