import json
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class CustomMiddleWare(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        response = await call_next(request)

        content_type = response.headers.get("Content-Type")
        if content_type == "application/json":
            response_body = [section async for section in response.body_iterator]
            resp_str = response_body[0].decode()
            resp_dict = json.loads(resp_str)

            data = {}
            if "openapi" not in resp_dict:
                data["data"] = resp_dict
                data["meta"] = {"total_time": round(time.time() - start_time, 2)}

            return JSONResponse(
                content=data,
                status_code=response.status_code,
                media_type=response.media_type,
            )

        return response
