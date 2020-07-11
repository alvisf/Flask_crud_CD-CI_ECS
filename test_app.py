from flask import Flask
from app import app


def test_base_route():
    client = app.test_client()
    url = "/"
    response = client.get(url)
    assert response.status_code == 404


def test_something():
    assert True
