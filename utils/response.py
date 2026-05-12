from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message='success', data = None):
    content = {
        "code": "200",
        "message": message,
        "data": data
    }

    # 把任何的 Fastapi、Pydantic、ORM对象都正常响应--->code、message、data
    return JSONResponse(content = jsonable_encoder(content))