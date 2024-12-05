from functools import wraps
import sentry_sdk
from positron_common.build_env import build_env

def track_command_usage(command_name):
    """Decorator to track usage of commands in Sentry with arguments."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Capture command usage event with arguments
            sentry_sdk.capture_event({
                "message": f"Command Run: {command_name}",
                "level": "info",
                "tags": {"command": command_name},
                "extra": {
                    "arguments": args,
                    "keyword_arguments": kwargs
                }
            })
            # Execute the command function
            return func(*args, **kwargs)
        return wrapper
    return decorator

def setup():
  """Should be run as early in the app lifecycle as possible"""
  # TODO: turn off in local dev mode.
  sentry_sdk.init(
    dsn="https://76683e3eb4abf2e208a27d252ab023bb@o4508017904910336.ingest.us.sentry.io/4508017906089984",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    environment=build_env.value
  )

setup()