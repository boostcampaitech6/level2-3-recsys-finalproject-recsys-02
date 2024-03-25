import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def main():
    
    # 데이터 로드 
    df = pd.read_csv('/Users/daeheehan/final/level2-3-recsys-finalproject-recsys-02/data/spec.csv')
    df = df[['user', 'item']]

    # 데이터 전처리
    interaction_counts = df['item'].value_counts()
    item_with_5_or_more_interactions = interaction_counts[interaction_counts >= 5].index
    df = df[df['item'].isin(item_with_5_or_more_interactions)]

    # 아이템-사용자 행렬 생성 및 코사인 유사도 계산
    item_user_matrix = df.pivot_table(index='item', columns='user', aggfunc=len, fill_value=0)
    item_similarity_df = pd.DataFrame(cosine_similarity(item_user_matrix), index=item_user_matrix.index, columns=item_user_matrix.index)

    # 아이템 간 유사도 행렬을 pickle 파일로 저장
    with open('item_similarity.pkl', 'wb') as f:
        pickle.dump(item_similarity_df, f)

if __name__ == "__main__":
    main()
