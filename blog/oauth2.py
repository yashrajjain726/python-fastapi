from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import jwt
from jwt import InvalidTokenError

from blog.schemas import TokenData
from blog.token import ALGORITHM, SECRET_KEY, oauth2_scheme, verify_token


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)