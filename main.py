from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 服务启动方法
if __name__ == '__main__':
    import Model
    import Business
    import ExperiencePage
    uvicorn.run('main:app', host='0.0.0.0', port=8888)
