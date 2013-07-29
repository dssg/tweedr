import time


def add_duration_header(app):
    def call(environ, start_response):
        started = time.time()

        def wrapped_start_response(status, headers):
            duration = time.time() - started
            return start_response(status, headers + [('X-Duration', str(duration))])

        return app(environ, wrapped_start_response)

    return call
