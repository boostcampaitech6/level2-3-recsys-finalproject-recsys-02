import pandas as pd
import numpy as np
from tqdm import tqdm

from google.cloud import storage
from google.oauth2 import service_account



def tfidf_data_load():
    """
    ----------
    TF-IDF를 위한 데이터 로드 함수
    ----------
    """
    #gcs()

    ## DATA LOAD
    interaction = pd.read_csv('../../data/inter_240129.csv')
    item = pd.read_csv('../../data/item.csv')

    id_to_title = { item.loc[i,'id']:item.loc[i, 'title']for i in range(len(item))}
    interaction['title'] = interaction['products'].map(id_to_title)


    ## DATA PROCESSING
    data_drop_local_time = interaction.drop(columns='local_time', axis=0)
    grouped = data_drop_local_time.groupby('hashed_ip')

    df_grouped = pd.DataFrame(columns=['hashed_ip', 'products', 'product_titles'])
    for i in tqdm(grouped):
        df_grouped.loc[len(df_grouped)] = [
            i[0],
            list(set(i[1]['products'][:])),
            str(list(set(i[1]['title'][:]))),
            ]
            
    df_grouped['product_titles'] = title_processing(df_grouped['product_titles'])

    
    ## SAVE PRODUCT_ID:TITLE
    # print('--------------- SAVE PRODUCT_ID_TITLE ---------------')
    # with open(args.save_vector_path + 'tfidf_pid_title_dict.pickle','wb') as fw:
    #     pickle.dump(id_to_title, fw)

    # pid_to_idx_path = f'{args.save_vector_path}/test.csv'
    # blob.upload_from_filename(pid_to_idx_path, content_type='text/csv')


    return df_grouped


def gcs():
    """
    ----------
    GCS로부터 파일 가져오기
    ----------
    """

    GCS_SERVICE_ACCOUNT_PATH = "../../config/level3-416207-893f91c9529e.json"

    credentials = service_account.Credentials.from_service_account_file(GCS_SERVICE_ACCOUNT_PATH)
    client = storage.Client(credentials = credentials)

    bucket_name = "crwalnoti"
    bucket = client.get_bucket(bucket_name)

    interaction_file = 'inter_240129.csv'
    file_path = f"240320/{interaction_file}"
    blob = bucket.get_blob(file_path)
    blob.download_to_filename(interaction_file)

    item_file = 'item.csv'
    file_path = f"240320/{item_file}"
    blob = bucket.get_blob(file_path)
    blob.download_to_filename(item_file)



def title_processing(series):
    """
    ----------
    title 문자열 특수문자 처리 및 공백 제거
    ----------
    """
    series = series.map(lambda x: x.replace('[','').replace(']','').replace("'",'').replace(',','').replace('(', ' ').replace(')', ' '))
    series = series.map(lambda x: x.split(' '))
    series = series.map(lambda x: ' '.join(x))
    return series