import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
from args import args



def tfidf_data_load(args):
    """
    ----------
    TF-IDF를 위한 데이터 로드 함수
    ----------
    """

    ## DATA LOAD
    interaction = pd.read_csv('./inter_240129.csv')
    item = pd.read_csv('./item.csv')

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
        if len(df_grouped)==900:
            break
    df_grouped['product_titles'] = title_processing(df_grouped['product_titles'])


    ## SAVE df_grouped
    with open( args.save_path + 'df_grouped.pickle','wb') as fw:
        pickle.dump(df_grouped, fw)


    return df_grouped



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




tfidf_data_load(args)