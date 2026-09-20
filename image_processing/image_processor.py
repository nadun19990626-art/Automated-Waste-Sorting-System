#!/usr/bin/env python3

"""
Image Processing Module
Automated Waste Sorting System

This module handles image acquisition preprocessing and
preparation of waste images for classification.

The processed image is passed to the waste classification
module for determining the waste category.
"""

import cv2
import logging
import numpy as np


logger = logging.getLogger(__name__)


class ImageProcessor:
    """
    Image processing class for the automated waste
    sorting system.
    """

    def __init__(self):
        """Initialize the image processor."""

        logger.info("Initializing image processor...")

        self.processing_width = 640
        self.processing_height = 480

        logger.info("Image processor initialized successfully.")

    # ---------------------------------------------------------
    # Main Image Processing Function
    # ---------------------------------------------------------

    def process(self, image):
        """
        Process the captured waste image.

        Parameters:
            image: Image captured from the camera.

        Returns:
            Processed image.
        """

        if image is None:

            logger.warning(
                "No image received for processing."
            )

            return None

        try:

            # Resize image
            resized_image = self.resize_image(image)

            # Convert image to grayscale
            grayscale_image = self.convert_to_grayscale(
                resized_image
            )

            # Reduce image noise
            filtered_image = self.reduce_noise(
                grayscale_image
            )

            logger.info(
                "Image processing completed successfully."
            )

            return filtered_image

        except Exception as error:

            logger.error(
                f"Image processing failed: {error}"
            )

            return None

    # ---------------------------------------------------------
    # Image Resizing
    # ---------------------------------------------------------

    def resize_image(self, image):
        """
        Resize the input image to the required processing
        resolution.
        """

        resized = cv2.resize(
            image,
            (
                self.processing_width,
                self.processing_height
            )
        )

        return resized

    # ---------------------------------------------------------
    # Grayscale Conversion
    # ---------------------------------------------------------

    def convert_to_grayscale(self, image):
        """
        Convert a colour image into grayscale.
        """

        grayscale = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        return grayscale

    # ---------------------------------------------------------
    # Noise Reduction
    # ---------------------------------------------------------

    def reduce_noise(self, image):
        """
        Reduce image noise using Gaussian filtering.
        """

        filtered = cv2.GaussianBlur(
            image,
            (5, 5),
            0
        )

        return filtered

    # ---------------------------------------------------------
    # Edge Detection
    # ---------------------------------------------------------

    def detect_edges(self, image):
        """
        Detect edges in the processed image.

        This function can be used during the development
        of the waste-object detection algorithm.
        """

        edges = cv2.Canny(
            image,
            50,
            150
        )

        return edges

    # ---------------------------------------------------------
    # Object Region Detection
    # ---------------------------------------------------------

    def detect_object_region(self, image):
        """
        Identify the main object region in the image.

        This function provides a basic foundation for
        object detection and can be expanded according
        to the final classification method.
        """

        if image is None:

            return None

        try:

            # Threshold image
            _, threshold = cv2.threshold(
                image,
                0,
                255,
                cv2.THRESH_BINARY +
                cv2.THRESH_OTSU
            )

            # Find contours
            contours, _ = cv2.findContours(
                threshold,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            if not contours:

                logger.warning(
                    "No object detected in image."
                )

                return None

            # Select largest contour
            largest_contour = max(
                contours,
                key=cv2.contourArea
            )

            area = cv2.contourArea(
                largest_contour
            )

            logger.info(
                f"Detected object area: {area:.2f}"
            )

            return largest_contour

        except Exception as error:

            logger.error(
                f"Object detection failed: {error}"
            )

            return None

    # ---------------------------------------------------------
    # Get Image Features
    # ---------------------------------------------------------

    def extract_basic_features(self, image):
        """
        Extract basic image features that can be used
        by the classification module.
        """

        if image is None:

            return None

        try:

            height, width = image.shape[:2]

            features = {
                "width": width,
                "height": height,
                "mean_intensity": float(
                    np.mean(image)
                ),
                "standard_deviation": float(
                    np.std(image)
                )
            }

            return features

        except Exception as error:

            logger.error(
                f"Feature extraction failed: {error}"
            )

            return None
