from datetime import datetime, timedelta
from functools import wraps

from fastapi import Request
from fastapi.responses import Response

from reach_commons.app_logging.logger import get_reach_logger

logger = get_reach_logger()


def deprecated_warning(added_date: datetime, deprecation_period_days: int = 180):
    """
    Decorator to indicate that an endpoint is deprecated in FastAPI.

    - Adds a "Warning" header to the response during the deprecation period.
    - Uses HTTP status 409 ("Gone") after the deprecation period ends.
    - Uses HTTP status 301 ("Moved Permanently") if a replacement URL is provided.

    Args:
        added_date (datetime): The date when the deprecation was announced.
        deprecation_period_days (int): Number of days before the endpoint is removed (default: 180).
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, response: Response, *args, **kwargs):
            removal_date = added_date + timedelta(days=deprecation_period_days)
            removal_date_str = removal_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
            current_date = datetime.utcnow()

            path = request.url.path if request else "Unknown Path"
            method = request.method if request else "Unknown Method"

            warning_message = f'299 "{method} {path}" is deprecated and will be removed on [{removal_date_str}]"'

            response.headers["Deprecation-Warning"] = warning_message

            if current_date < removal_date:
                logger.warning(
                    f"Deprecated endpoint accessed: {method} {path}. "
                    f"Deprecation period ends on {removal_date_str}."
                )

            elif current_date >= removal_date:
                logger.error(
                    f"Access to removed endpoint: {method} {path}. "
                    f"Removal date was {removal_date_str}."
                )

            return await func(request, response, *args, **kwargs)

        return wrapper

    return decorator
