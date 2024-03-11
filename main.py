from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# add acceptable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        # "http://purple-archive.netlify.app",
        # "https://purple-archive.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# exception handler to dump what's wrong
@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONResponse(
        content={},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}
