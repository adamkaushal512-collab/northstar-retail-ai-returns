class IntegrationError(Exception):
    """Base exception for enterprise integration failures."""


class UpstreamUnavailable(IntegrationError):
    """An upstream enterprise system is unavailable."""


class UpstreamTimeout(IntegrationError):
    """An upstream request exceeded its timeout."""


class InvalidUpstreamResponse(IntegrationError):
    """An upstream system returned invalid evidence."""
