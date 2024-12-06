import logging


class Log(object):
    configured: bool = False

    @staticmethod
    def configure() -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s::%(levelname)s::%(name)s::%(funcName)s::%(lineno)d::%(message)s",
        )
        Log.configured = True

    @staticmethod
    def get_logger_function():

        # Return the function "getLogger" from the logging package.
        # This is needed because the logger needs to be initialized in the module to work properly
        return getattr(logging, "getLogger")


# This will always run on import!!!
# This way logging is always setup if the module is imported.
if not Log.configured:
    Log.configure()
