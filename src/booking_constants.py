"""
Module: booking_constants.py
Layer: Configuration (cross-cutting)
User Stories: All

Centralised business rule constants shared across Entity, Controller,
and Boundary layers. Any change to a business rule (e.g. refund rate,
booking limit, ban threshold) should only happen in this file.
"""

TIME_FORMAT = "%Y-%m-%d %H:%M"
DISPLAY_TIME_FORMAT = "%Y-%m-%d %H:%M"
END_TIME_DISPLAY_FORMAT = "%H:%M"

SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60
MINIMUM_BOOKING_MINUTES = 60
BOOKING_INCREMENT_MINUTES = 30
LATE_CANCELLATION_MINUTES = 30

DEFAULT_EQUIPMENT_DEPOSIT = 50.0
BOOKING_ID_PREFIX = "BK"
BOOKING_ID_DIGITS = 4

BOOKING_STATUS_CONFIRMED = "confirmed"
BOOKING_STATUS_CANCELLED = "cancelled"

PAYMENT_METHOD_BALANCE = "balance"
PAYMENT_METHOD_DEAL_PACKAGE = "deal_package"

CANCELLATION_REGULAR = "regular_cancellation"
CANCELLATION_LATE = "late_cancellation"
CANCELLATION_STOPPED = "cancellation_stopped"

REASON_INVALID_INPUT = "invalid_input"
REASON_NO_ROOMS = "no_rooms"
REASON_ROOMS_FOUND = "rooms_found"
REASON_BANNED = "banned"
REASON_BOOKING_LIMIT_REACHED = "booking_limit_reached"
REASON_INVALID_DURATION = "invalid_duration"
REASON_ROOM_UNAVAILABLE = "room_unavailable"
REASON_INSUFFICIENT_BALANCE = "insufficient_balance"
REASON_INSUFFICIENT_DEAL_HOURS = "insufficient_deal_hours"
REASON_DEAL_PACKAGE_EQUIPMENT_RESTRICTED = "deal_package_equipment_restricted"
REASON_INVALID_PAYMENT_METHOD = "invalid_payment_method"
REASON_BOOKING_CREATED = "booking_created"
REASON_BOOKING_NOT_FOUND = "booking_not_found"

# Room type classification
ROOM_TYPE_SMALL = "Small"
ROOM_TYPE_MEDIUM = "Medium"
ROOM_TYPE_LARGE = "Large"

# Price boundaries (per hour) for automatic room type inference
SMALL_ROOM_MAX_PRICE = 10.0      # price <= 10.0 -> Small
MEDIUM_ROOM_MAX_PRICE = 40.0     # 10.0 < price <= 40.0 -> Medium
                                 # price > 40.0 -> Large

# Capacity limits per room type
SMALL_ROOM_MAX_CAPACITY = 2
MEDIUM_ROOM_MAX_CAPACITY = 6
LARGE_ROOM_MAX_CAPACITY = 100

# Equipment rental fee used in predicted income calculation
EQUIPMENT_RENTAL_FEE = 10.0

# Room ID generation
ROOM_ID_PREFIX = "RM"
ROOM_ID_DIGITS = 4

# Cancel command keyword
CANCEL_COMMAND = "CANCEL"

# Late cancellation refund rates (percentage of room price)
SMALL_LATE_CANCEL_REFUND_RATE = 0.5
MEDIUM_LATE_CANCEL_REFUND_RATE = 0.5
LARGE_LATE_CANCEL_REFUND_RATE = 0.3

# No-show refund rates
SMALL_NO_SHOW_REFUND_RATE = 0.2

# Late cancellation time windows
SMALL_LATE_CANCEL_WINDOW_MINUTES = 30
MEDIUM_LATE_CANCEL_WINDOW_HOURS = 3
LARGE_LATE_CANCEL_WINDOW_HOURS = 4

# Advance booking requirements
MEDIUM_ADVANCE_BOOKING_HOURS = 3
LARGE_ADVANCE_BOOKING_HOURS = 24

# Minimum booking duration for Medium/Large rooms
MEDIUM_LARGE_MIN_BOOKING_MINUTES = 120

# Student limits
MAX_ACTIVE_BOOKINGS = 3
BAN_THRESHOLD = 3

# Advance booking rejection reason
REASON_ADVANCE_BOOKING_NOT_MET = "advance_booking_requirement_not_met"

# No-show status
BOOKING_STATUS_NO_SHOW = "no_show"
