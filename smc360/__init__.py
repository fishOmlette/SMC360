"""
SMC360 - Social Media Data Connector

A unified toolkit for extracting, parsing, and managing social media data at scale.
"""

__version__ = "1.0.0"
__author__ = "Mohammed Adil Farooq"
__email__ = "adil.farooq@blend360.com"

from smc360.lib import SocialMediaConnector

# Backward compatibility alias
socialMediaConnector = SocialMediaConnector

__all__ = [
    "SocialMediaConnector",
    "socialMediaConnector",
    "__version__",
]
