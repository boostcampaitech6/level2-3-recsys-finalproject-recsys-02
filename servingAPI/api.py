from fastapi import APIRouter, HTTPException, status, Depends
from schemas import PredictionRequest_SASRec, PredictionRequest_TFIDF, PredictionResponse_SASRec, PredictionResponse_TFIDF
from utils.inference import tfidf_inference, seq_prepare, test
from utils.dependencies import get_tfidf_dependencies, get_model
router = APIRouter()

@router.post("/predict/sasrec") #main에서 fastapi실행시 동작하도록 코드 구성
def predict(request: PredictionRequest_SASRec, model=Depends(get_model)) -> PredictionResponse_SASRec:
    #post func for tfidf
    data = request.dict()
    user_seq, item_seq = data['user_seq'], data['item_seq']
    pred = test(model, user_seq, item_seq)
    response = PredictionResponse_SASRec(sasrec_result = pred)

    return response
    

@router.post("/predict/tfidf") #필요할때 올라오도록 코드 구성
def predict(request: PredictionRequest_TFIDF) -> PredictionResponse_TFIDF:
    #post func for tfidf
    
    dtm_user, user_idx, vectorizer = get_tfidf_dependencies()
    result = tfidf_inference(request.user, request.item, dtm_user, user_idx, vectorizer)
    return PredictionResponse_TFIDF(tfidf_result=result)