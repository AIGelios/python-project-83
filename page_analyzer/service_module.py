from datetime import datetime
from flask import flash


def get_current_timestamp():
    return datetime.now()
