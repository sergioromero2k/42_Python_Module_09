#!/usr/bin/env python3

from pydantic import BaseModel, ValidationError, Field, model_validator
from enum import Enum
from datetime import datetime
from typing import List

"""
Validates space missions and crew requirements using Pydantic nested models.
"""


class Rank(str, Enum):
    # Defining the allowed ranks as an Enum ensures Pydantic
    # Only accepts theses values
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    # Defines the individual data for each crew member
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    # Space Model: handles the core mission data and validation logic
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    # MIssion Validation Rules: Inplementing safety requirements.
    @model_validator(mode='after')
    def validate_mission_safety(self) -> "SpaceMission":
        # Rule 1: Check mission_id
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        # Rule 2: Check for leadership (Captain or Commander)
        # Is ANY member's rank a Caption o r Commander
        has_leader = any(
            m.rank in [Rank.CAPTAIN, Rank.COMMANDER] for m in self.crew)

        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        # Rule 3: Check long-duration experience
        if self.duration_days > 365:
            # Create a list of only the experienced members
            exeprienced_members = [
                m for m in self.crew if m.years_experience >= 5]

            # Move the check INSIDE the if-block
            if len(exeprienced_members) < (len(self.crew) / 2):
                raise ValueError(
                    "Long missions need 50% experienced crew (5+ years)")

        # Rule 4: All crew members must be active
        if not all(m.is_active for m in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    # Sample data for a valid mission setup.
    valid_data = {
        "mission_id": "M2024_TITAN",
        "mission_name": "Solar Observatory Research Mission",
        "destination": "Solar Observatory",
        "launch_date": "2024-03-30T00:00:00",
        "duration_days": 451,
        "crew": [
            {
                "member_id": "CM001",
                "name": "Sarah Williams",
                "rank": "captain",
                "age": 43,
                "specialization": "Mission Command",
                "years_experience": 19,
                "is_active": True,
            },
            {
                "member_id": "CM003",
                "name": "Anna Jones",
                "rank": "cadet",
                "age": 35,
                "specialization": "Communications",
                "years_experience": 15,
                "is_active": True,
            },
        ],
        "mission_status": "planned",
        "budget_millions": 2208.1,
    }

    print("Space Mission Crew Validation")
    print("==========================================")
    print("")

    try:
        # Create valid mission from dictionary
        mission = SpaceMission.model_validate(valid_data)
        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")
        for m in mission.crew:
            print(f"- {m.name} ({m.rank.value}) - {m.specialization}")
    except ValidationError as e:
        print(f"Validation error: {e}")

    print("")
    print("=========================================")
    print("Expected validation error:")

    try:
        # Let's create an invalid mission (Invalid ID: doesn't start with M)
        invalid_data = valid_data.copy()
        invalid_data["crew"] = [
            {
                "member_id": "CM999",
                "name": "Noob Saibot",
                "rank": "cadet",    # No leadership rank
                "age": 20,
                "specialization": "Cleaning",
                "years_experience": 0,
                "is_active": True,
            }
        ]
        SpaceMission.model_validate(invalid_data)
    except ValidationError as e:
        # This gets the specific error me ssage from your validator
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    main()
