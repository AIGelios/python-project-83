from datetime import datetime
from flask import flash, get_flashed_messages


def get_current_timestamp():
    return datetime.now()


def error_alert(message):
    flash(message, 'alert-danger')


def done_alert(message):
    flash(message, 'alert-success')


def info_alert(message):
    flash(message, 'alert-info')


def get_alerts():
    return get_flashed_messages(with_categories=True)
