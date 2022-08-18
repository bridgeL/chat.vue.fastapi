from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from user import User
from event import json2event

app = FastAPI()

# 静态HTML文件


@app.get("/")
def get():
    return FileResponse("dist/" + "index.html")


@app.get("/{file:path}")
def get(file):
    return FileResponse("dist/" + file)


# ws


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user = User(ws=websocket)

    while True:
        try:
            data = await websocket.receive_json()
        except:
            user.disconnect()
            break
        event = json2event(data)
        # 可能会需要做一些判断，一些事件不需要传递给user
        await user.handle_event(event)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="app:app", host="0.0.0.0", port=5000, reload=True)
