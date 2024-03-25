from pydantic import BaseModel

class PredictionRequest_SASRec(BaseModel):
    user_seq : list = []
    item_seq : list = []
    # [userseq],[item_seq]

class PredictionRequest_TFIDF(BaseModel):
    user : str # hashed_ip
    item : str # product_title

class PredictionResponse_SASRec(BaseModel):
    sasrec_result: list =[]
    
class PredictionResponse_TFIDF(BaseModel):
    tfidf_result: float