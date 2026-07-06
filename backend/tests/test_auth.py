import pytest
from fastapi import HTTPException
from jose import jwt
from unittest.mock import MagicMock

import auth

def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        auth.get_current_user(token="invalid.jwt.token", db=None)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials — please log in again"

def test_get_current_user_missing_sub():
    token = jwt.encode({"role": "admin"}, auth.SECRET_KEY, algorithm=auth.ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        auth.get_current_user(token=token, db=None)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials — please log in again"

def test_get_current_user_user_not_found():
    token = jwt.encode({"sub": "nonexistent_user"}, auth.SECRET_KEY, algorithm=auth.ALGORITHM)

    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        auth.get_current_user(token=token, db=mock_db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials — please log in again"
