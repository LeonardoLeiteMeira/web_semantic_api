import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"Status":"Ok"}

app.include_router(user_router, prefix="/user")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )
