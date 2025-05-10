from datetime import datetime
import inspect

def console_message(level: str, contents: str) -> str:
    """
    Generate, print and return a formatted message with a timestamp and the current caller's name.
    Args:
        level (str): The log level (e.g. 'WARN', 'ERROR').
        contents (str): The message contents.
        
    Returns:
        str: The formatted message.
    """
    frame = inspect.currentframe().f_back # get caller's name
    name = frame.f_code.co_name
    message = f"[{datetime.now().strftime("%H:%M:%S")}] [{level} / {name}]: {contents}"
    print(message)
    return message