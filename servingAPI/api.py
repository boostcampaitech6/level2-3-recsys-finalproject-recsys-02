from fastapi import APIRouter, HTTPException, status, Depends
from schemas import PredictionRequest_SASRec, PredictionRequest_TFIDF, PredictionRequest_IBCF, PredictionResponse_SASRec, PredictionResponse_TFIDF, PredictionResponse_IBCF
from utils.inference import tfidf_inference, seq_prepare, test, ibcf_inference
from utils.dependencies import get_model, get_similarity_matrix
router = APIRouter()

@router.post("/predict/sasrec")
def predict(request: PredictionRequest_SASRec, model=Depends(get_model)) -> PredictionResponse_SASRec:
    #post func for tfidf
    data = request.dict()
    user_seq, item_seq = data['user_seq'], data['item_seq']
    pred = test(model, user_seq, item_seq)
    response = PredictionResponse_SASRec(sasrec_result = pred)

    return response
    

@router.post("/predict/tfidf")
def predict(request: PredictionRequest_TFIDF) -> PredictionResponse_TFIDF:
    #post func for tfidf
    
    # dtm_user, user_idx, vectorizer = get_tfidf_dependencies()
    result = tfidf_inference(request.user, request.item)
    return PredictionResponse_TFIDF(tfidf_result=result)


@router.post("/predict/ibcf")
def predict(request: PredictionRequest_IBCF) -> PredictionResponse_IBCF:
    #post func for ibcf
    
    item_similarity_df = get_similarity_matrix()
    recommends = ibcf_inference(item_similarity_df, request.item, request.topn)
    return PredictionResponse_IBCF(item_list=recommends['item'].tolist(), ibcf_result=recommends['similarity'].tolist())