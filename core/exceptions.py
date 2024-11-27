class DatabaseError(Exception):
    """All database exceptions, ocurring on the repositories."""

    status_code = 500


class NotFoundError(Exception):
    """Raised when resource is not found."""

    status_code = 404


class ValidationError(Exception):
    """Raised when input data fails validation."""

    pass


class OpenAIAPIError(Exception):
    """Raised when OpenAI API fails in a general manner."""

    status_code = 500


class OpenAIInvalidFormatError(Exception):
    """Raised when OpenAI API responds the user query with an invalid format."""

    status_code = 500


class ConflictError(Exception):
    """Raised when there is a conflict, such as duplicate data."""

    pass


class InvalidCredentialsError(Exception):
    """Raised when user credentials are invalid."""

    status_code = 401


class RegisterEmailError(Exception):
    """Raised when registration fails due to email already being in use."""

    status_code = 409


class TokenExpiredError(Exception):
    """Raised when an authentication token has expired."""

    pass


class ActiveSessionExistsError(Exception):
    """Raised when a user tries to start a new session while one is already active."""

    status_code = 409


class SessionAlreadyPausedError(Exception):
    """Raised when a session is already paused."""

    status_code = 409


class SessionAlreadyFinishedError(Exception):
    """Raised when a session is already finished."""

    status_code = 409


class SessionNotPausedError(Exception):
    """Raised when trying to unpause a session that is not paused."""

    status_code = 409


class PauseInactiveSessionError(Exception):
    """Raised when trying to unpause a session that is not active."""

    status_code = 409
