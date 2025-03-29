from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import entries, drafts, templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(entries.router)
app.include_router(drafts.router)
app.include_router(templates.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8888, reload=True)
