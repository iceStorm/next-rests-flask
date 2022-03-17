from flask import render_template


class ErrorHandler:
    Success = 200

    # Client error
    UnAuthenticated = 401
    Forbidden = 403
    NotFound = 404
    TooManyRequests = 429

    # Server error
    InternalServerError = 500

    @staticmethod
    def response(code: int, **kwargs):
        return render_template(f'errors/{code}.html', **kwargs), code


    @staticmethod
    def forbidden(e):
        return ErrorHandler.response(ErrorHandler.Forbidden)

    @staticmethod
    def not_found(e):
        return ErrorHandler.response(ErrorHandler.NotFound)

    @staticmethod
    def too_many_requests(e):
        from flask_limiter.errors import RateLimitExceeded
        from src import logger
        logger.info(f"you catched 429 error: {type(e)}", e)

        if type(e) is RateLimitExceeded:
            logger.error(e.limit.limit)

        return ErrorHandler.response(ErrorHandler.TooManyRequests, description = e.limit.limit)

    @staticmethod
    def server_error(e):
        return ErrorHandler.response(ErrorHandler.InternalServerError)
