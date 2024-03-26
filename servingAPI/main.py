
from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger
from api import router
from utils.dependencies import load_df_grouped, load_model, load_dict, load_similarity_matrix

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load File for TF-IDF Serving
    logger.info("Loading TF-IDF Dependency Files")
    load_df_grouped()
     
    logger.info("Loading item2idx dict")
    load_dict() 
    # Load Sasrec model trained
    logger.info("Loading model")
    # model.py에 존재. 역할을 분리해야 할 수도 있음 => 새로운 파일을 만들고, 거기서 load_model 구현
    load_model()
    
    logger.info("Loading similarity matrix")
    load_similarity_matrix()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/")
def root():
    return "Welcome to crwlnoti Recsys API"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
