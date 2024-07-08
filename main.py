import os

from fastapi import FastAPI, Request

app = FastAPI()

REQUEST_FILE = "api_requests/requests.txt"


def check_file():
    if not os.path.isfile(REQUEST_FILE):
        with open(REQUEST_FILE, "w"):
            pass


async def write_request(request: Request):
    if await request.body():
        body = await request.json()
    else:
        body = None
    with open(REQUEST_FILE, "a") as f:
        f.write(f"{request.method} - FROM :: {request.client} TO :: {request.url}\n")
        f.write(f"HEADERS :: \n{request.headers}\n")
        f.write(f"BODY :: \n{body}\n")
        f.write("\n\n")
        f.write("=" * 15)
        f.write("\n\n")


@app.get("/webhook")
async def get_webhook(request: Request):
    check_file()
    await write_request(request)
    return {"status": "success"}


@app.post("/webhook")
async def post_webhook(request: Request):
    check_file()
    await write_request(request)
    return {"status": "success"}


@app.get("/hello")
async def test_alive():
    return "Hello from fast-http-server"
