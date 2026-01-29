#!/usr/bin/env python3

from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime

"""
Alien Contact Log Validation Module
This module defines models and validation rules for extraterrestrial
contact reports using Pydantic v2.
"""


class ContactType(Enum):
    # Enumeration of authorized alien contact types.

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """
    Model representing an alien contact report with specific business rules.
    Attributes:
        contact_id: Unique identifier starting with 'AC'.
        timestamp: Time of the event.
        location: Geographic location of contact.
        contact_type: Method of contact (Enum).
        signal_strength: 0-10 scale.
        duration_minutes: Duration (max 24h).
        witness_count: Number of witnesses (1-100).
        message_received: Optional message content.
        is_verified: Verification status.
    """

    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self):
        """
        Validates complex business rules after individual field validation.
        Note: In Pydantic v2 mode='after', the first argument is 'self'.
        """
        # Rule 1: ID Prefix (Fixed typo: .startswith instead of .startwith)
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        # Rule 2: Physical contact must be verified
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        # Rule 3: Telepathic contact requirements
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")

        # Rule 4: Strong signals require messages
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")

        return self


def print_contact_report(contact: AlienContact) -> None:
    # Displays contact information in a formatted way.
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    msg = (
        f"'{contact.message_received}'"
        if contact.message_received else "None")
    print(f"Message: {msg}")


def main() -> None:
    print("Alien Contact Log Validation")
    print("========================================")

    # CASE 1: Valid contact
    valid_data = {
        "contact_id": "AC_2024_001",
        "timestamp": "2024-01-20T14:30:00",
        "location": "Area 51, Nevada",
        "contact_type": "radio",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli",
        "is_verified": True,
    }

    try:
        contact = AlienContact(**valid_data)
        print_contact_report(contact)
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("\n========================================")

    # CASE 2: Invalid contact (Telepathic with < 3 witnesses)
    print("Expected validation error:")
    invalid_data = valid_data.copy()
    invalid_data["contact_id"] = "AC_2024_002"
    invalid_data["contact_type"] = "telepathic"
    invalid_data["witness_count"] = 1  # This violates the rule

    try:
        AlienContact(**invalid_data)
    except ValidationError as e:
        # Prints the specific business rule error message
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
