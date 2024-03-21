from pydantic import BaseModel

class PredictionRequest_SASRec(BaseModel):
    user_seq : list
    item_seq : list
    # [userseq],[item_seq]

class PredictionRequest_TFIDF(BaseModel):
    user : str
    item : str
    # [userseq],[item_seq]

class PredictionResponse_base(BaseModel):
    result: list 
    #[item_percentage_list]