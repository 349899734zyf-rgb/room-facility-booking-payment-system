import subprocess
import sys
import os

def run_integration_test():
    # Path to students.csv in the root directory
    student_file_path = r"d:\5136\project 2\students.csv"
    if os.path.exists(student_file_path):
        print(f"Removing existing {student_file_path} to ensure clean state...")
        os.remove(student_file_path)

    # Define inputs for the interactive CLI
    inputs = [
        "1",  # Login
        "admin1@monash.edu",  # Admin Email
        "Password123456",  # Admin Password
        "1",  # Room Management
        "1",  # Add New Room
        "Study Pod 2",  # Room Name
        "Building B",  # Building
        "3",  # Capacity
        "10.0",  # Price
        "08:00-17:00",  # Opening hours
        "6",  # Update time slots
        "RM0001",  # Room ID
        "1",  # Choose AVAILABLE (1)
        "10:00-12:00",  # Time slot to add
        "3",  # Return to Admin menu
        "5",  # Admin Logout
        "1",  # Login
        "student1@student.monash.edu",  # Student Email
        "Password123",  # Student Password
        "1",  # Search & Book Room
        "Building B",  # Enter building
        "2026-05-06 10:00",  # Start time
        "2026-05-06 12:00",  # End time
        "1",  # Capacity
        "RM0001",  # Select RM0001 to book
        "2",  # Do not rent equipment
        # --- Direct Checkout Flow ---
        "1",  # Choose payment method: Balance
        "",  # Promo code: None
        "1",  # Confirm payment: Yes
        "2",  # Finish checkout
        # --- Verify Slot Consumption by searching again ---
        "1",  # Search & Book Room
        "Building B",  # Enter building
        "2026-05-06 10:00",  # Start time
        "2026-05-06 12:00",  # End time
        "1",  # Capacity
        "CANCEL",  # Cancel out of search flow because slot is consumed
        "7",  # Student Logout
        "3"   # Exit
    ]

    input_data = "\n".join(inputs) + "\n"
    
    # Run the main.py script
    cmd = [sys.executable, "src/main.py"]
    print(f"Running command: {' '.join(cmd)}")
    
    # Run from the project root directory
    cwd = r"d:\5136\project 2"
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
        text=True
    )
    
    stdout, stderr = process.communicate(input=input_data, timeout=10)
    
    print("--- STDOUT ---")
    print(stdout)
    
    if stderr:
        print("--- STDERR ---")
        print(stderr)
        
    print(f"Process exited with code: {process.returncode}")
    
    # Assertions to verify the booking succeeded and slot is consumed
    assert "Login Successful!" in stdout, "Admin or Student login failed"
    assert "Room added successfully" in stdout, "Room creation failed"
    assert "RM0001" in stdout, "New room RM0001 not listed/found"
    assert "Room reserved!" in stdout, "Booking reservation failed"
    assert "Booking confirmed" in stdout, "Payment checkout failed"
    assert "No rooms are available during the selected time period." in stdout, "Slot consumption check failed: room was still available!"
    print("\nSUCCESS: All integration checks passed! The newly added room was successfully booked, and the slot was correctly consumed.")

if __name__ == "__main__":
    run_integration_test()
