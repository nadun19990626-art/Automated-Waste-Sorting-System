"""
Configuration file for the Automated Waste Sorting System.

This file contains the main system parameters, camera settings,
waste classification categories, and PLC communication settings.
"""

# ============================================================
# SYSTEM INFORMATION
# ============================================================

SYSTEM_NAME = "Automated Waste Sorting System"
SYSTEM_VERSION = "1.0"


# ============================================================
# CAMERA CONFIGURATION
# ============================================================

# Camera device index
# 0 = first/default camera
CAMERA_INDEX = 0

# Camera resolution
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


# ============================================================
# IMAGE PROCESSING CONFIGURATION
# ============================================================

# Time interval between processing cycles (seconds)
PROCESSING_DELAY = 1.0

# Directory used to save captured images
CAPTURE_DIRECTORY = "captures"


# ============================================================
# WASTE CLASSIFICATION
# ============================================================

# Waste categories used by the sorting system

WASTE_PLASTIC = "Plastic"
WASTE_METAL = "Metal"
WASTE_PAPER = "Paper"
WASTE_OTHER = "Other"

# List of supported waste categories

WASTE_CATEGORIES = [
    WASTE_PLASTIC,
    WASTE_METAL,
    WASTE_PAPER,
    WASTE_OTHER
]


# ============================================================
# PLC CONFIGURATION
# ============================================================

# PLC model
PLC_MODEL = "Siemens S7-200 CPU 224"

# PLC communication status
PLC_ENABLED = True

# PLC connection parameters
#
# These values will be updated when the actual
# Raspberry Pi-to-PLC communication method is finalized.

PLC_IP_ADDRESS = "192.168.0.1"
PLC_PORT = 102


# ============================================================
# ROBOTIC ARM CONFIGURATION
# ============================================================

# Robotic arm model
ROBOT_MODEL = "Epson T6-602S"

# Number of robotic arms
NUMBER_OF_ROBOTS = 2


# ============================================================
# VACUUM SYSTEM
# ============================================================

VACUUM_SYSTEM_ENABLED = True


# ============================================================
# CONVEYOR SYSTEM
# ============================================================

CONVEYOR_ENABLED = True


# ============================================================
# SENSOR CONFIGURATION
# ============================================================

# Object detection sensor
OBJECT_SENSOR_ENABLED = True


# ============================================================
# DEBUGGING
# ============================================================

DEBUG_MODE = True
