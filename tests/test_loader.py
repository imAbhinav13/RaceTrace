import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.data_loader import get_session

session = get_session(2024, "Monaco", "Q")
print("Drivers:", session.drivers)
print("First few laps:\n", session.laps.head())
