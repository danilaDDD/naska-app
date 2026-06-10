import time
from flask import Flask, request, g, jsonify
from loggers import logger


def register_middleware(app: Flask) -> None:
    @app.before_request
    def before():
        g.start = time.perf_counter()

    @app.after_request
    def after(response):
        if response.status_code >= 400:
            ms = (time.perf_counter() - g.start) * 1000
            logger.error("%s %s %d %.1fms", request.method, request.path, response.status_code, ms)
        return response

    @app.errorhandler(RuntimeError)
    def handle_runtime_error(e: RuntimeError):
        logger.error("RuntimeError: %s", e, exc_info=True)
        return jsonify({"error": str(e)}), 500