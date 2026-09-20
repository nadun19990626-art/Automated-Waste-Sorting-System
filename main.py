#!/usr/bin/env python3

"""
Automated Waste Sorting System
Main control script for Raspberry Pi based waste classification
and automated robotic sorting.

Hardware:
- Raspberry Pi
- Camera
- Object detection sensor
- Siemens S7-200 CPU 224 PLC
- Epson T6-602S robotic arms
- Vacuum suction system
- Conveyor system
- Waste collection bins

Author: Nadun
Version: 1.0
"""

import cv2
import time
import os
import threading
import logging
from datetime import datetime

from configuration.config import *
from image_processing.image_processor import ImageProcessor
from image_processing.classification import WasteClassifier
from plc_control.plc_communication import PLCCommunication


# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("waste_sorting.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Main Waste Sorting System
# ---------------------------------------------------------

class WasteSortingSystem:

    def __init__(self):
        """Initialize the automated waste sorting system."""

        logger.info("Initializing Automated Waste Sorting System...")

        self.running = False
        self.processing_lock = threading.Lock()

        self.setup_camera()
        self.setup_sensor()

        self.image_processor = ImageProcessor()
        self.classifier = WasteClassifier()
        self.plc_comm = PLCCommunication()

        logger.info("System initialization completed.")

    # -----------------------------------------------------
    # Camera Setup
    # -----------------------------------------------------

    def setup_camera(self):
        """Initialize the camera used for waste inspection."""

        try:

            self.camera = cv2.VideoCapture(CAMERA_INDEX)

            self.camera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                CAMERA_WIDTH
            )

            self.camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                CAMERA_HEIGHT
            )

            if not self.camera.isOpened():
                raise Exception("Camera could not be opened.")

            logger.info("Camera initialized successfully.")

        except Exception as error:

            logger.error(
                f"Camera initialization failed: {error}"
            )

            raise

    # -----------------------------------------------------
    # Sensor Setup
    # -----------------------------------------------------

    def setup_sensor(self):
        """Initialize the waste detection sensor."""

        logger.info(
            "Waste detection sensor initialized."
        )

        # Actual GPIO sensor configuration
        # will be implemented according to the
        # final hardware connection.

    # -----------------------------------------------------
    # Capture Image
    # -----------------------------------------------------

    def capture_image(self):
        """Capture an image of the waste material."""

        try:

            ret, frame = self.camera.read()

            if not ret:

                logger.error(
                    "Failed to capture image from camera."
                )

                return None

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = (
                f"captures/waste_{timestamp}.jpg"
            )

            cv2.imwrite(filename, frame)

            logger.info(
                f"Waste image captured: {filename}"
            )

            return frame

        except Exception as error:

            logger.error(
                f"Image capture error: {error}"
            )

            return None

    # -----------------------------------------------------
    # Waste Processing
    # -----------------------------------------------------

    def process_waste(self):
        """Process and classify detected waste."""

        if not self.processing_lock.acquire(
            blocking=False
        ):

            logger.warning(
                "Previous waste item is still being processed."
            )

            return

        try:

            logger.info(
                "Waste material detected."
            )

            # Capture image
            image = self.capture_image()

            if image is None:
                return

            # Image processing
            processed_image = (
                self.image_processor.process(image)
            )

            # Waste classification
            waste_type = (
                self.classifier.classify(
                    processed_image
                )
            )

            logger.info(
                f"Waste classified as: {waste_type}"
            )

            # Send classification to PLC
            self.send_sorting_command(
                waste_type
            )

            # Record processing information
            self.log_processing_result(
                waste_type
            )

        except Exception as error:

            logger.error(
                f"Waste processing failed: {error}"
            )

        finally:

            self.processing_lock.release()

    # -----------------------------------------------------
    # PLC Sorting Command
    # -----------------------------------------------------

    def send_sorting_command(self, waste_type):
        """
        Send the waste classification to the PLC.

        The PLC uses the classification signal to
        control the appropriate robotic sorting sequence.
        """

        try:

            logger.info(
                f"Sending classification to PLC: "
                f"{waste_type}"
            )

            self.plc_comm.send_classification(
                waste_type
            )

            logger.info(
                "Classification sent successfully."
            )

        except Exception as error:

            logger.error(
                f"PLC communication failed: {error}"
            )

    # -----------------------------------------------------
    # Processing Statistics
    # -----------------------------------------------------

    def log_processing_result(self, waste_type):
        """Save waste classification information."""

        try:

            with open(
                "processing_stats.csv",
                "a"
            ) as file:

                timestamp = datetime.now().isoformat()

                file.write(
                    f"{timestamp},{waste_type}\n"
                )

        except Exception as error:

            logger.error(
                f"Failed to save processing data: "
                f"{error}"
            )

    # -----------------------------------------------------
    # Start System
    # -----------------------------------------------------

    def start_system(self):
        """Start the automated waste sorting system."""

        logger.info(
            "Starting Automated Waste Sorting System..."
        )

        self.running = True

        try:

            # Establish PLC communication
            self.plc_comm.connect()

            logger.info(
                "System ready."
            )

            logger.info(
                "Waiting for waste material..."
            )

            while self.running:

                # -------------------------------------------------
                # Temporary detection method
                # -------------------------------------------------
                #
                # The final version will trigger this function
                # using the conveyor/object detection sensor.
                #
                # -------------------------------------------------

                self.process_waste()

                # Delay between detection cycles
                time.sleep(
                    PROCESSING_DELAY
                )

        except KeyboardInterrupt:

            logger.info(
                "Shutdown requested by user."
            )

        except Exception as error:

            logger.error(
                f"System error: {error}"
            )

        finally:

            self.shutdown()

    # -----------------------------------------------------
    # Shutdown
    # -----------------------------------------------------

    def shutdown(self):
        """Safely shut down the system."""

        logger.info(
            "Shutting down Automated Waste Sorting System..."
        )

        self.running = False

        # Release camera
        if hasattr(self, "camera"):

            self.camera.release()

        # Close PLC communication
        self.plc_comm.disconnect()

        cv2.destroyAllWindows()

        logger.info(
            "System shutdown completed."
        )


# ---------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------

def main():
    """Main program entry point."""

    try:

        # Create image capture directory
        os.makedirs(
            "captures",
            exist_ok=True
        )

        # Create and start system
        sorting_system = WasteSortingSystem()

        sorting_system.start_system()

    except Exception as error:

        logger.error(
            f"Failed to start system: {error}"
        )


# ---------------------------------------------------------
# Program Execution
# ---------------------------------------------------------

if __name__ == "__main__":

    main()
