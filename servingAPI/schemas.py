from pydantic import BaseModel

class PredictionRequest_SASRec(BaseModel):
    user_seq : list = []
    item_seq : list = []
    # [userseq],[item_seq]

class PredictionRequest_TFIDF(BaseModel):
    user : str # hashed_ip
    item : str # product_title

class PredictionRequest_IBCF(BaseModel):
    item : str # hashed_ip
    topn : int = 10 # product_title

class PredictionResponse_SASRec(BaseModel):
    sasrec_result: list =[]
    
class PredictionResponse_TFIDF(BaseModel):
    tfidf_result: float
    
class PredictionResponse_IBCF(BaseModel):
    item_list: list =[]
    ibcf_result: list =[]