"""Hotel room reservation and booking management module."""

import hashlib
import os
import secrets

ROOM_INVENTORY = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}


def book_room(room_num, guest_name, booking_log=None):
    """Book a room for a guest. Return True if the booking succeeded."""
    if booking_log is None:
        booking_log = []
    if room_num not in ROOM_INVENTORY or ROOM_INVENTORY[room_num]["is_booked"]:
        return False
    ROOM_INVENTORY[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Release a room. Return False if the room does not exist."""
    if room_num not in ROOM_INVENTORY:
        return False
    ROOM_INVENTORY[room_num]["is_booked"] = False
    return True


def check_room_status(room_num):
    """Return True if the room exists and is not booked."""
    if ROOM_INVENTORY.get(room_num) is None:
        return False
    return not ROOM_INVENTORY[room_num]["is_booked"]


def compute_seasonal_rate(room_num, multiplier):
    """Return the room's base price scaled by a positive multiplier."""
    if multiplier <= 0:
        raise ValueError("Rate multiplier must be positive")
    base_price = ROOM_INVENTORY[room_num]["price"]
    return base_price * multiplier


def generate_guest_hash(guest_id):
    """Return a SHA-256 hash of the guest ID."""
    return hashlib.sha256(guest_id.encode()).hexdigest()


def generate_booking_ref():
    """Return a random 4-digit booking reference."""
    return secrets.randbelow(9000) + 1000


def export_room_ledger(filename="hotel_ledger.txt"):
    """Write the room inventory to a text file."""
    with open(filename, "w", encoding="utf-8") as ledger:
        ledger.write(str(ROOM_INVENTORY))
    print("Hotel ledger exported to:", filename)


def main():
    """Run a short demo of the booking system."""
    hotel_secret_key = os.environ.get("HOTEL_SECRET_KEY")
    booking_log = []
    print("Booked 101:", book_room("101", "Emma Watson", booking_log))
    print("Booking log:", booking_log)
    print("Cancelled 102:", cancel_booking("102"))
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", 1.25))
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()
    print("Secret key configured:", hotel_secret_key is not None)


if __name__ == "__main__":
    main()
