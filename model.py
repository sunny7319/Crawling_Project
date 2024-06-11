import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import plotly.express as px
import numpy as np
from sklearn.neighbors import NearestNeighbors
#사용 패키지 import 


def change_data(data):
    result_list = []
    for i in range(len(data)):
        result_list.append([item.strip(" '[]") for item in data[i].split(',')]) #기술스택이 ['AWS','MySQL']과 같이 되어있는데 이를 리스트 내 요소들로 변환해줌
    return result_list

def company_to_vector(data,model,vec_size): 
    vectors_list = []
    for i in range(len(data)):
        vectors = [0 for i in range(vec_size)] #w2v model의 vector size 만큼 0벡터 생성
        cnt = 0 #나중에 평균내주기 위해서 저장
        for j in range(len(data[i])):
            if data[i][j] in model.wv.index_to_key:

                vectors += model.wv[data[i][j]] #해당 기업이 가진 스킬들의 벡터 합
                cnt += 1
            else:
                pass
        
        for k in range(len(vectors)):
            if cnt == 0:
                pass
            else:
                vectors[k]= vectors[k]/cnt #평균내줌
        vectors_list.append(vectors) #기업 벡터로 사용
    return vectors_list


def draw_plotly_company_names(vectors_list, tsne,data):
    feat = tsne.fit_transform(np.array(vectors_list)) #2차원에 표현해주기 위해서 tsne사용
    cluster = KMeans(n_clusters=5) #k-means clustering으로 색깔 표시
    cluster.fit(vectors_list) #유사한 벡터들끼리 색깔 유사하게
    y_kmeans = cluster.predict(vectors_list)
    fig = px.scatter(x = feat[:,0],y = feat[:,1],color=y_kmeans,text=data['기업명'],width=1200, height=1200) #tsne 그려줌
    fig.update_traces(marker={'size': 8},textposition='top center')

    fig.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=13,  # Set the font size here
            color="RebeccaPurple"
        ) #기업 이름 크기 설정
    )
    return fig

def draw_plotly_skill_names(model, tsne):
    x_embed3 = tsne.fit_transform(model.wv.vectors) #스킬들 tsne
    cluster = KMeans(n_clusters=3) #클러스터링 
    cluster.fit(model.wv.vectors)
    y_kmeans = cluster.predict(model.wv.vectors)
    fig = px.scatter(x_embed3[:,0],x_embed3[:,1],color=y_kmeans,text=model.wv.index_to_key,width=800, height=800) #그려줌
    fig.update_traces(marker={'size': 8},textposition='top center')
    return fig

def index_search(data,search_name,company_vector):
    neighbor = NearestNeighbors(n_neighbors=10,metric='cosine') #코사인 유사도 기반 kNN
    neighbor.fit(company_vector)
    result_neig = neighbor.kneighbors(company_vector,return_distance=True) #kNN 계산된 내용 
    name_list = data['기업명']
    ind_list = []
    cnt = 0
    for i in name_list:
        if i == search_name:
            ind_list.append(cnt) #이름과 검색하는 검색어와 동일 시 추가
            cnt += 1
    nei_name = [] #유사한 기업 이름 
    for i in ind_list:
        for j in result_neig[1][i]: #거리 말고 유사도 기반으로 탐색
            nei_name.append(j)
    nei_name = list(set(nei_name)) #유사한 기업 추가
    return_name = []
    cnt = 0
    idx = []
    for i in nei_name:
        if cnt == 5: #5개 검색
            break
        elif data['기업명'][i] != search_name: #동일한 기업일 시 pass
            return_name.append(data['기업명'][i])
            idx.append(i)
            cnt += 1
    for i in idx:
        print('기업정보는 다음과 같아요 \n',data.drop('features',axis=1).iloc[i])
    return return_name



def make_mean(inp, vec,model,data,vec_size):
    vectors = [0 for i in range(vec_size)] #검색하는 스킬들의 벡터 구하기 위함
    cnt = 0
    for i in inp:
        vector = model.wv[i]
        vectors += vector #vector sum 계산
        cnt += 1

    for k in range(len(vectors)):
        if cnt == 0:
            pass
        else:
            vectors[k]= vectors[k]/cnt  #vector mean 계산
    vec.append(vectors) #마지막 벡터가 구하고자 하는 벡터임
    neighbor = NearestNeighbors(n_neighbors=10,metric='cosine')
    neighbor.fit(vec) #구해진 vector에서 kNN진행

    result_neig = neighbor.kneighbors(vec,return_distance=False)
    sim_vec = result_neig[-1] #마지막 벡터와 유사한 벡터들 구함

    return_name = []
    cnt = 0
    idx = []
    for i in sim_vec:
        if i >= 170: #170개 기준으로 했기 때문에 사용, index error 회피
            pass
        else:
            if cnt == 5: #5개까지 구함
                break

            elif data['기업명'][i] not in return_name: #중복되지 않게 구함
                return_name.append(data['기업명'][i])
                idx.append(i)
                cnt += 1

    for i in idx:
        print('기업정보는 다음과 같아요 \n',data.drop('features',axis=1).iloc[i])
    return return_name

def skill_search(search_name,model):
    neighbor = NearestNeighbors(n_neighbors=10,metric='cosine')
    neighbor.fit(model.wv.vectors)
    result_neig = neighbor.kneighbors(model.wv.vectors,return_distance=True) #스킬들의 유사도 구하기 위함
    #print(result_neig)
    skill_name = model.wv.index_to_key
    ind_list = []
    cnt = 0
    for i in skill_name:
        if i == search_name:
            ind_list.append(cnt)
        cnt += 1
    nei_name = []
    for i in ind_list:
        for j in result_neig[1][i]:
            nei_name.append(j)
    nei_name = list(set(nei_name))
    return_name = []
    cnt = 0
    for i in nei_name:
        if cnt == 5: #5개 까지 구함
            break
        elif skill_name[i] != search_name:
            return_name.append(skill_name[i])
            cnt += 1
    return return_name


df = pd.read_csv('./integrated_data.csv') #data load and preprocessing
