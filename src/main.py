from datetime import datetime
from entity_classes import Student, Room
from controller_classes import BookingController


def main():
    """
    Entry point of the booking system.
    """
    print("=== Booking System Test ===")

    # Initialize controller
    controller = BookingController()

    # Create a sample student
    student = Student(
        "test@student.monash.edu",
        "Password1",
        "Yan",
        "Student",
        "0412345678",
        "S001"
    )

    # Create a sample room
    room = Room("R001", "Study Room 1", "Building A", 4, 15.0, "09:00-18:00")

    # Set available time slots for the room
    room.set_available_time_slots([
        "2026-05-06 10:00-2026-05-06 12:00"
    ])

    # Add room to controller
    controller.get_rooms().append(room)

    # --- Book 1: Filter rooms by criteria ---
    building = input("Enter building: ")
    start_time_str = input("Enter start time (YYYY-MM-DD HH:MM): ")
    end_time_str = input("Enter end time (YYYY-MM-DD HH:MM): ")

    rooms = controller.search_rooms(building, start_time_str, end_time_str)

    if not rooms:
        print("No available rooms found.")
        return

    print("\nAvailable rooms:")
    for i, room in enumerate(rooms):
        print(f"{i + 1}. {room.get_room_name()}")

    # --- Book 5: Create a new booking draft ---
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

    print("\nBooking Summary:")
    print("Room:", selected_room.get_room_name())
    print("Building:", selected_room.get_building())
    print("Start time:", start_time_str)
    print("End time:", end_time_str)

    # --- Book 9: Select an available room ---
    choice = int(input("\nSelect a room number: ")) - 1
    selected_room = rooms[choice]

    print("\nSelected room:")
    print(selected_room.get_room_name())

    # --- Book 15: Make booking ---
    confirm = input("\nConfirm booking? (y/n): ")

    if confirm.lower() == "y":
        booking = controller.create_booking(
            student,
            selected_room,
            start_time,
            end_time,
            False
        )

        if booking:
            print("Booking created successfully:", booking.get_booking_id())
        else:
            print("Booking failed.")
    else:
        print("Booking cancelled.")


if __name__ == "__main__":
    main()






