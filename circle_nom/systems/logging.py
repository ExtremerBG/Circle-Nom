import logging
import inspect
import sys

class _ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[94m",
        logging.INFO: "\033[92m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
        logging.CRITICAL: "\033[95m",
    }
    RESET = "\033[0m"

    def format(self, record):
        time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        color = self.COLORS.get(record.levelno, self.RESET)
        levelname = f"{color}{record.levelname}{self.RESET}"
        logger_name = record.name
        function = getattr(record, "function", "unknown")
        msg = record.getMessage()
        return f"[{time}][{logger_name} / {levelname}]: [{function}] {msg}"

class _SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "function"):
            record.function = "unknown"
        return super().format(record)

class _FunctionLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if extra is None:
            extra = {}
            
        frame = inspect.currentframe()
        for _ in range(2):
            if frame is not None:
                frame = frame.f_back

        function_name = frame.f_code.co_name if frame else "unknown"
        extra["function"] = function_name

        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

def get_logger(name: str = __name__, logfile: str = "cn.log") -> logging.Logger:
    """
    Returns a configured logger instance with colorized console output and file logging.

    This is the primary interface for obtaining a logger across the application.
    It wraps the built-in `logging.getLogger` with additional formatting features:
    - Console output with log level–based coloring
    - File logging with timestamped entries
    - Automatic inclusion of the caller function name in each log record

    Args:
        name (str): The name of the logger, typically `__name__`. Used to identify log origin.
        logfile (str): Path to the file where logs will be saved. Defaults to 'app.log'.

    Returns:
        logging.Logger: A logger object configured with color-coded console handler
                        and file handler using consistent formatting.

    Example:
        logger = get_logger(name = __name__)
        logger.info("Token validation started")

    Log Format:
        [YYYY-MM-DD HH:MM:SS] [logger_name / LEVEL]: [function_name] Message
    """
    logging.setLoggerClass(_FunctionLogger)
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(_ColorFormatter())
        logger.addHandler(ch)

        # File handler
        fh = logging.FileHandler(logfile)
        fh.setFormatter(_SafeFormatter(
            "[%(asctime)s] [%(name)s / %(levelname)s]: [%(function)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(fh)

    return logger
