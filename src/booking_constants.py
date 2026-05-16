"""
This file stores shared constant values used by the booking feature.
Keeping these values in one place avoids embedded constants and improves
readability.
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
