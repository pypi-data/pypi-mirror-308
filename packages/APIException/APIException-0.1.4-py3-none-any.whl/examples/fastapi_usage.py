from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api_exception.exception import APIException
from custom_enum.enums import ExceptionStatus, BaseExceptionCode
from schemas.response_model import ResponseModel

app = FastAPI()


# Define a custom ExceptionCode class for specific application errors
class CustomExceptionCode(BaseExceptionCode):
    # User Related Errors
    USER_NOT_FOUND = ("USR-404", "User not found.", "The specified user does not exist in the system.")
    # API Key Related Errors
    INVALID_API_KEY = ("API-401", "Invalid API key provided.", "Please provide a valid API key.")
    # Permission Related Errors
    PERMISSION_DENIED = ("PERM-403", "Permission denied.", "You do not have permission to access this resource.")


# Set up an exception handler for APIException
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.http_status_code,
        content=exc.to_response()
    )


@app.get("/user/{user_id}")
async def get_user(user_id: int):
    # Simulate a user not found scenario
    if user_id != 1:  # Assuming only user with ID 1 exists
        raise APIException(
            error_code=CustomExceptionCode.USER_NOT_FOUND,
            http_status_code=404
        )
    return ResponseModel(data={"user_id": user_id, "name": "John Doe"})


@app.get("/apikey")
async def check_api_key(api_key: str):
    # Simulate an invalid API key scenario
    if api_key != "valid_key":
        raise APIException(error_code=CustomExceptionCode.INVALID_API_KEY)
    return ResponseModel(data={"message": "API key is valid"})


@app.get("/restricted")
async def restricted_access():
    # Simulate a permission denied scenario
    raise APIException(
        error_code=CustomExceptionCode.PERMISSION_DENIED,
        http_status_code=403,
        status=ExceptionStatus.FAIL,
        description="You do not have permission to access this resource.",
        message="Permission denied."
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
