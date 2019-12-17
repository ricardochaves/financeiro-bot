from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    """
    Formats the logging output to fit a json-like format. Adds
    the 'severity' field instead of 'levelname' for Stackdriver
    logging purposees.
    """

    def __init__(self, format: str, *args, **kwargs):
        """
        Initializes the JsonFormatter with the desired format.
        """
        jsonlogger.JsonFormatter.__init__(self, fmt=format, *args, **kwargs)

    def process_log_record(self, log_record: dict) -> dict:
        """
        Override of the jsonlogger.JsonFormatter method. Adds Stackdriver's
        severity field.
        """
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]

        return log_record
