from page_analyzer import app
from flask import Flask


def test_app_is_active():
    assert app
    assert isinstance(app, Flask)
