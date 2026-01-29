#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime

"""
Simple example of data validation using Pydantic.
Defines a SpaceStation model and demonstrates valid and invalid inputs.
"""


class SpaceStation(BaseModel):
    """
    * Unique station identifier (3-10 characters)
    * Human-readable station name
    * Number of crew members allowed on board
    * Current power level percentage
    * Current oxygem level percentage
    * Timestamp of the last maintenance operation
    * Whether the station is currently operational
    * Optional notes or comments
    """

    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    # CASE 1: Valid station data
    valid_data = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        # Pydantic will parse this ISO string into a datetime
        "last_maintenance": "2024-01-20T12:00:00",
        "is_operational": True
    }

    try:
        station = SpaceStation(**valid_data)
        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        print(f"Status: {'Operational' if station.is_operational else 'Down'}")
    except ValidationError as e:
        print(f"Unexpected error: {e}")
    print("")
    print("========================================")
    # CASE 2: Invalid station (crew size too large)
    print("Expected validation error:")
    invalid_data = valid_data.copy()
    invalid_data["crew_size"] = 25

    try:
        SpaceStation(**invalid_data)
    except ValidationError as e:
        # Print only the first validation error message
        print(e.errors()[0]["msg"])
        """
        Extracts and prints the human-readable message of the
        first validation error raised by Pydantic.
        """


if __name__ == "__main__":
    main()
