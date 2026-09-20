#!/usr/bin/env python3

"""
Waste Classification Module
Automated Waste Sorting System

This module is responsible for determining the category
of waste after image processing.

Current supported categories:
- Plastic
- Metal
- Paper
- Other

The classification method can later be replaced or
extended with a trained machine-learning/deep-learning
model.
"""

import logging
import numpy as np

from configuration.config import (
    WASTE_PLASTIC,
    WASTE_METAL,
    WASTE_PAPER,
    WASTE_OTHER,
    WASTE_CATEGORIES
)


logger = logging.getLogger(__name__)


class WasteClassifier:
    """
    Waste classification class.

    This class provides the interface between the image
    processing module and the waste classification system.
    """

    def __init__(self):
        """Initialize the waste classifier."""

        logger.info(
            "Initializing waste classification system..."
        )

        self.categories = WASTE_CATEGORIES

        logger.info(
            f"Supported waste categories: "
            f"{', '.join(self.categories)}"
        )

    # ---------------------------------------------------------
    # Main Classification Function
    # ---------------------------------------------------------

    def classify(self, image):
        """
        Classify the processed waste image.

        Parameters:
            image: Processed image from ImageProcessor.

        Returns:
            Waste category as a string.
        """

        if image is None:

            logger.warning(
                "No image available for classification."
            )

            return WASTE_OTHER

        try:

            # -------------------------------------------------
            # Placeholder classification method
            # -------------------------------------------------
            #
            # The final project will use the selected
            # image-classification method here.
            #
            # At present, the system returns "Other"
            # until a trained classification model or
            # validated classification algorithm is added.
            # -------------------------------------------------

            classification = self.model_classification(
                image
            )

            logger.info(
                f"Waste classification result: "
                f"{classification}"
            )

            return classification

        except Exception as error:

            logger.error(
                f"Waste classification failed: {error}"
            )

            return WASTE_OTHER

    # ---------------------------------------------------------
    # Model Classification
    # ---------------------------------------------------------

    def model_classification(self, image):
        """
        Perform waste classification.

        This function is currently prepared as an interface
        for the final machine-learning/image-classification
        method.

        Parameters:
            image: Processed image.

        Returns:
            Waste category.
        """

        # -----------------------------------------------------
        # PLACEHOLDER
        # -----------------------------------------------------
        #
        # Replace this section with the final trained model
        # or validated classification algorithm.
        #
        # Example:
        #
        # prediction = self.model.predict(image)
        #
        # -----------------------------------------------------

        return WASTE_OTHER

    # ---------------------------------------------------------
    # Validate Classification
    # ---------------------------------------------------------

    def validate_category(self, category):
        """
        Check whether the classification result is one of
        the supported waste categories.
        """

        if category in self.categories:

            return True

        logger.warning(
            f"Invalid waste category: {category}"
        )

        return False

    # ---------------------------------------------------------
    # Classification Confidence
    # ---------------------------------------------------------

    def get_confidence(self, image):
        """
        Return the classification confidence.

        This is a placeholder for future machine-learning
        model integration.
        """

        # Confidence will be calculated by the final
        # classification model.

        return 0.0
