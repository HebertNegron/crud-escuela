import string
import random
from fastapi.responses import JSONResponse
from fastapi import status

def get_random_string(length) -> str:
    letters: str = string.ascii_lowercase + string.digits
    result_str: str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def success_response(message: str = "Success") -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": message}
    )