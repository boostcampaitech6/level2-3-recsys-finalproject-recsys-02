import pandas as pd
import pickle
import sys  # 커맨드라인 인자 처리를 위한 모듈

def load_similarity_matrix(path: str) -> pd.DataFrame:
    """유사도 행렬 불러오기"""
    with open(path, 'rb') as f:
        similarity_matrix = pickle.load(f)
    return similarity_matrix

def IBCF(item_similarity_df: pd.DataFrame, item: str, topn: int = 5) -> pd.DataFrame:
    """아이템 기반 협업 필터링 함수"""
    topn = topn + 1  # 입력한 아이템 제외
    if item in item_similarity_df.index:
        sim_item_df = item_similarity_df[item].sort_values(ascending=False).reset_index().rename(columns={'index':'item',item:'similarity'})
        print('입력한 아이템 id:', item)
        return sim_item_df[1:topn]
    else:
        print('아이템 id를 다시 확인해주세요')
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python inference.py <item_id> <topn>")
        sys.exit(1)

    item_id = str(sys.argv[1])
    topn = int(sys.argv[2])

    path = './'  # 데이터 경로 설정
    item_similarity_df = load_similarity_matrix(path + 'item_similarity.pkl')
    recommended_items = IBCF(item_similarity_df, item_id, topn)
    
    for item in recommended_items['item'].tolist():
        print(f'{item}')