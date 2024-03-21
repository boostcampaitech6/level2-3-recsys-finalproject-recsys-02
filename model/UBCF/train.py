import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def main():
    # 데이터 로드
    df = pd.read_csv('/Users/daeheehan/final/level2-3-recsys-finalproject-recsys-02/data/spec.csv')
    df = df[['user', 'item']]

    # 데이터 전처리 5번 이상 상호작용한 사용자 필터링
    interaction_counts = df['user'].value_counts()
    users_with_5_or_more_interactions = interaction_counts[interaction_counts >= 5].index
    df = df[df['user'].isin(users_with_5_or_more_interactions)]

    # 사용자-아이템 행렬 생성
    user_item_matrix = df.pivot_table(index='user', columns='item', aggfunc=len, fill_value=0)

    # 사용자 간 유사도 계산
    user_similarity_df = pd.DataFrame(cosine_similarity(user_item_matrix), index=user_item_matrix.index, columns=user_item_matrix.index)

    # 유사도 행렬 저장
    with open('user_similarity_df.pkl', 'wb') as f:
        pickle.dump(user_similarity_df, f)

    print("Training complete and user similarity matrix saved.")

if __name__ == "__main__":
    main()
