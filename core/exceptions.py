# --- App specific errors ---


class StudereError(Exception):
    """Base class for all of our app's errors."""

    pass


# --- Repository Errors ---


class RepositoryError(StudereError):
    """Base class for repository exceptions."""

    pass


# --- Service Errors ---


class ServiceError(StudereError):
    """Base class for service exceptions."""

    pass


class NotFoundError(ServiceError):
    pass


class ValidationError(ServiceError):
    """Raised when input data fails validation."""

    pass


class OpenAIAPIError(ServiceError):
    pass


class OpenAIInvalidFormatError(ServiceError):
    pass


class PermissionError(ServiceError):
    """Raised when a user lacks the required permissions."""

    pass


class ConflictError(ServiceError):
    """Raised when there is a conflict, such as duplicate data."""

    pass


# --- Authentication and Authorization ---
class AuthenticationError(StudereError):
    """Base class for authentication-related errors."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when user credentials are invalid."""

    pass


class TokenExpiredError(AuthenticationError):
    """Raised when an authentication token has expired."""

    pass


class AuthorizationError(StudereError):
    """Raised when a user tries to access something they are not authorized to."""

    pass


# --- Business Logic Specific ---
class StudySessionError(StudereError):
    """Base class for study session-related errors."""

    pass


class ActiveSessionExistsError(StudySessionError):
    """Raised when a user tries to start a new session while one is already active."""

    pass


class SessionAlreadyPausedError(StudySessionError):
    """Raised when a session is already paused."""

    pass


class SessionAlreadyFinishedError(StudySessionError):
    """Raised when a session is already finished."""

    pass


class SessionNotPausedError(StudySessionError):
    """Raised when trying to unpause a session that is not paused."""

    pass


class PauseInactiveSessionError(StudySessionError):
    """Raised when trying to unpause a session that is not active."""

    pass


# --- External API and Integration Exceptions ---


class ExternalAPIError(StudereError):
    """Base class for errors related to external APIs or integrations."""

    pass


class APIConnectionError(ExternalAPIError):
    """Raised when there is a connection issue with an external API."""

    pass


class APITimeoutError(ExternalAPIError):
    """Raised when an external API request times out."""

    pass


class APIDataError(ExternalAPIError):
    """Raised when external API returns unexpected or invalid data."""

    pass


# --- General Utility Exceptions ---
class ConfigurationError(StudereError):
    """Raised for misconfigurations in the application."""

    pass


class RateLimitExceededError(StudereError):
    """Raised when a user exceeds a rate limit."""

    pass


class OperationNotAllowedError(StudereError):
    """Raised when an operation is not allowed in the current context."""

    pass
