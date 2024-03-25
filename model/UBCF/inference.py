import pandas as pd
import pickle
import sys

def load_user_similarity():
    with open('user_similarity_df.pkl', 'rb') as f:
        user_similarity_df = pickle.load(f)
    return user_similarity_df

def Recommend_UBCF(user_similarity_df, df, user):
    '''
    유사 사용자 각각의 상위 10개 아이템(가장 최근 또는 가장 많이 상호작용한 아이템을 가정)을 추출하고, 
    이 중에서 입력 사용자가 아직 상호작용하지 않은 아이템들을 추천 목록으로 선정합니다. 
    여기서 set 연산을 사용하여 중복을 제거하고, | 연산자로 합집합을 구한 후, - 연산자로 차집합을 구하여 이미 상호작용한 아이템을 제외합니다.
    '''
    inter_user = user_similarity_df[str(user)].sort_values(ascending=False)[1:4].index

    items = list((set(df[df['user'] == inter_user[0]]['item'].value_counts().head(10).index) |
                  set(df[df['user'] == inter_user[1]]['item'].value_counts().head(10).index) |
                  set(df[df['user'] == inter_user[2]]['item'].value_counts().head(10).index)) -
                 set(df[df['user'] == user]['item'].values))

    return items

def main(user_id):

    # 데이터 로드
    df = pd.read_csv('/Users/daeheehan/final/level2-3-recsys-finalproject-recsys-02/data/spec.csv')
    df = df[['user', 'item']]

    # 데이터 전처리
    interaction_counts = df['user'].value_counts()
    users_with_5_or_more_interactions = interaction_counts[interaction_counts >= 5].index
    df = df[df['user'].isin(users_with_5_or_more_interactions)]

    # train 된 유사도 행렬 
    user_similarity_df = load_user_similarity()

    # 추천
    recommended_items = Recommend_UBCF(user_similarity_df, df, user_id)
    
    return recommended_items

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inference.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    recommended_items = main(user_id)

    for item in recommended_items:
        print(f'{item}')
