import sys
import json

sys.path.insert(0, "app")
from lambda_function import lambda_handler


def test_status_code():
    result = lambda_handler({}, None)
    assert result["statusCode"] == 200


def test_body_has_message():
    result = lambda_handler({}, None)
    body = json.loads(result["body"])
    assert "message" in body
    assert "version" in body
