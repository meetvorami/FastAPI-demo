from datetime import datetime, timedelta, timezone

import jwt

from config.config import JWTSetting


class Token:
    def __init__(self):
        jwt_setting = JWTSetting()
        self.ACCESS_TOKEN_EXPIRE_MINUTES = jwt_setting.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_MINUTES = jwt_setting.REFRESH_TOKEN_EXPIRE_MINUTES
        self.SECRET_KEY = jwt_setting.SECRET_KEY
        self.ALGORITHM = jwt_setting.ALGORITHM

    def decode_jwt(self, token):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

    def encode_jwt(self, data):
        return jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = self.encode_jwt(to_encode)
        return encoded_jwt

    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = self.encode_jwt(to_encode)
        return encoded_jwt
