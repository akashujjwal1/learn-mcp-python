from fastapi import FastAPI, Response
from http import HTTPStatus

app = FastAPI()

@app.get("/error/{code}")
async def error_endpoint(code: int):
    try:
        status = HTTPStatus(code)
    except ValueError:
        return Response(content=f"Invalid status code: {code}", status_code=400)

    body = {"error": True, "status": status.value, "reason": status.phrase}
    return Response(content=__import__("json").dumps(body), media_type="application/json", status_code=status.value)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
