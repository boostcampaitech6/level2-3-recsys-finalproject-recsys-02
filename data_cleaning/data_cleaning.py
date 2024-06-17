import pandas as pd

def data_cleaning(df, time_limit=10, consecutive_clicks=3):

    df['time'] = pd.to_datetime(df['time'], format='%d/%b/%Y:%H:%M:%S')     # 시간 포멧 변경
    df = df.drop_duplicates(subset=['user', 'item', 'time'])                # 중복 데이터 제거

    abuse_indices = []
    for _, group in df.groupby(['user', 'item']):
        group = group.sort_values(by='time')  # 시간 순으로 정렬
        for i in range(len(group) - consecutive_clicks + 1):
            # 첫 번째 클릭과 마지막 클릭 사이의 시간 차이 계산
            time_diff = (group.iloc[i + consecutive_clicks - 1]['time'] - group.iloc[i]['time']).total_seconds()
            if time_diff <= time_limit:
                # 조건을 만족하는 인덱스를 리스트에 추가
                abuse_indices.extend(group.iloc[i:i + consecutive_clicks].index.tolist())

    # 어뷰징으로 판단된 인덱스를 제거하고 중복 제거
    abuse_df = df.loc[abuse_indices].drop_duplicates()
    
    # 어뷰징 데이터 전체 제거
    cleaned_df = df.drop(abuse_df.index)

    # 첫번째 데이터 처리
    first_user_df = abuse_df.drop_duplicates(subset=['user', 'item'], keep='first')
    
    # merge
    merge_df = pd.concat([cleaned_df, first_user_df])
    merge_df.sort_values(by=['user', 'item', 'time'])
    merge_df.reset_index(drop=True, inplace=True)
    
    return merge_df
