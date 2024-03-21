from fastapi import APIRouter, HTTPException, status
from schemas import PredictionRequest_SASRec, PredictionRequest_TFIDF, PredictionResponse_base

router = APIRouter()

@router.post("/predict/sasrec") #main에서 fastapi실행시 동작하도록 코드 구성
def predict(request: PredictionRequest_SASRec) -> PredictionResponse_base:
    #post func for tfidf
    pass

@router.post("/predict/tfidf") #필요할때 올라오도록 코드 구성
def predict(request: PredictionRequest_TFIDF) -> PredictionResponse_base:
    #post func for tfidf
    pass