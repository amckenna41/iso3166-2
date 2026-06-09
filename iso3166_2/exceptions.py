"""Custom exceptions for the iso3166-2 package."""

from typing import Optional


class ISO3166Error(Exception):
    """Base exception for iso3166-2 domain-specific errors."""


class DataFileError(OSError, ISO3166Error):
    """Raised when the bundled or custom data file cannot be loaded."""


class InvalidCountryCode(ValueError, ISO3166Error):
    """Raised when an ISO 3166-1 country code is invalid."""


class InvalidSubdivisionCode(ValueError, ISO3166Error):
    """Raised when an ISO 3166-2 subdivision code format is invalid."""


class CountryDataUnavailable(ValueError, ISO3166Error):
    """Raised when a valid country code is requested but not loaded in the current object."""


class SubdivisionNotFound(ValueError, ISO3166Error):
    """Raised when a subdivision code lookup fails."""


class InvalidAttributeError(ValueError, ISO3166Error):
    """Raised when an invalid attribute key is provided."""


class InvalidSearchInput(ValueError, ISO3166Error):
    """Raised when search/reverse-lookup inputs are invalid."""
