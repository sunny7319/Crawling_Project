import pandas as pd
from aws_craw import * 
from config import get_args
from model import *
import gensim
import time
import sys #사용하는 패키지 라이브러리 import
if __name__ == '__main__':
    args = get_args() # args 설정
    pre_data = args.predata # pre 크롤링 된 파일 사용 여부
    all_prepro = args.allpreprocess # 데이터 전체 전처리 여부
    pre_model = args.premodel # pretrained w2v 모델 사용 여부
    vec_size = args.model_vec_size # w2v model vector size
    win_size = args.model_win_size # w2v model window size
    neg_size = args.model_neg_size # w2v model negative size
    min_size = args.model_min_size # w2v model min count size
    search_name = args.search_name # 프롬프트 모드에서 검색할 기업
    search_skill = args.search_skill # 프롬프트 모드에서 검색할 스킬
    prompt_mode = args.prompt_mode # 프롬프트 모드 사용 여부
    if pre_data == False:
        # 크롤러 실행
        wanted = CModels.wanted_craw() #원티드
        rallit = CModels.rallit_craw() #랠릿
        programmers = CModels.prog_craw() #프로그래머스 크롤링 진행
        #통합 데이터 제작
        concat_data = DataPreprocessing.data_concat(programmers,rallit,wanted)#.drop('Unnamed: 0',axis=1)

        names = concat_data['기업명']
        #잘못된 기업 이름 수정
        for i in range(len(names)):
            fix_names = DataPreprocessing.name_chk(names[i])
            names[i] = fix_names

        names = list(names)

        #기업 정보 크롤링
        result = CModels.company_info(names)


        integrated_data = pd.concat([concat_data,result],axis=1)#.drop('Unnamed: 0',axis=0) #얻어진 데이터 concat

        integrated_data.to_csv('./integrated_data.csv',encoding='utf-8') #저장
    else:
        integrated_data = pd.read_csv('./integrated_data.csv') #미리 저장된 파일 사용
        integrated_data = integrated_data.drop('Unnamed: 0',axis=1) #불러왔으니까 Unnamed: 0 drop



    result_list = change_data(integrated_data['기술스택']) #기술스택 전처리
    
    if pre_model == True:
        # load W2V 16, 5, 5, 5
        model = gensim.models.Word2Vec.load('./w2v_16.model') 
    else:
        # train W2V by skills
        model = gensim.models.Word2Vec(sentences=result_list,vector_size=vec_size,window=win_size,negative=neg_size,min_count=min_size)
    
    if all_prepro == 1:
        integrated_data = all_preprocess(integrated_data) #data preprocessing 모든 데이터 전처리 한번에 해주는 코드

    # make company vector by skills mean
    company_vector = company_to_vector(result_list,model,vec_size)

    # add company vectors to df
    new_df = integrated_data.copy()
    new_df['features'] = company_vector

    # vectors to tsne (for draw)
    tsne = TSNE(n_components=2,metric='cosine',random_state=42)
    if prompt_mode == True:
        company_name_plotly = draw_plotly_company_names(company_vector,tsne,new_df) #plotly 로 기업 tsne 그림
        skill_name_plotly = draw_plotly_skill_names(model,tsne) #plotly로 기술스택 tsne 그림
        print('안녕하세요')
        print('프롬프트 모드입니다.')
        time.sleep(.5)
        print('어떤 것을 도와드릴까요?')
        time.sleep(.5)
        print('1. AWS 직무 채용을 하는 기업들의 유사도를 보고 싶어')
        print('2. 어떤 스킬을 공부하면 어떤 기업들을 갈 수 있는지 보고 싶어')
        print('3. 스킬들의 유사도를 보고 싶어')
        print('1 or 2 or 3 으로 입력해주세요')
        input = sys.stdin.readline
        search_keyword = int(input()) #사용자 입력 
        cnt = 0 #한번만 보여주기 위해서 사용
        while True:
            
            if search_keyword == 1:
                name_list = new_df['기업명'].unique()
                if cnt == 0:
                    company_name_plotly.show() #plotly 보여줌
                    cnt += 1
                print('유사한 기업들을 검색할 수 있습니다. 원하시는 기업을 검색해주세요')
                print(f'기업 검색가능 항목 : {name_list}') #검색 가능한 리스트 제공
                print('종료하시려면 컨트롤 C')
                search_keyword2 = list(str(input()).split())[0]         #사용자 입력 
                sim_company = index_search(new_df,search_keyword2,company_vector) #입력된 데이터와 유사한 기업 반환 
                time.sleep(.5)
                if len(sim_company) > 0:
                    
                    print(f'{search_keyword2}와 유사한 채용을 하고 있는 기업들은 다음과 같습니다.',sim_company) #0개 이상 반환된다면 보여줌
                    time.sleep(1)
                else:
                    print('목록에 없는 기업을 검색하셨어요 !') #0개면 없는 것을 검색한 것이니 없다고 표시
                    time.sleep(1)

            elif search_keyword == 2:
                if cnt == 0:
                    company_name_plotly.show()
                    cnt += 1
                print('검색하는 스킬을 채용하는 기업들을 알 수 있습니다. 스킬을 검색해주세요')
                print('여러가지 스킬도 검색할 수 있습니다. ex) AWS MySQL 과 같이 띄어쓰기로 구분해서 검색해주세요')
                print(f'스킬 검색가능 항목 : {model.wv.index_to_key}') #검색 가능 스킬 리스트 보여줌
                print('종료하시려면 컨트롤 C')

                search_keyword2 = list(str(input()).split())            #검색어 입력
                resu = make_mean(search_keyword2,company_vector,model,new_df,vec_size) #스킬들의 벡터 평균과 유사한 기업 반환
                time.sleep(.5)
                if len(resu) > 0:

                    print(f'{search_keyword2} 검색하신 스킬을 채용하는 회사는 다음과 같습니다.',resu)
                    time.sleep(1)
                else:
                    print('목록에 없는 스킬을 검색하셨어요 !')
                    time.sleep(1)

            elif search_keyword == 3: 
                if cnt == 0:
                    skill_name_plotly.show()
                    cnt += 1
                print('검색하는 스킬과 공고에 함께 올라오는 스킬들을 검색할 수 있습니다')
                print(f'스킬 검색가능 항목 : {model.wv.index_to_key}') #스킬 리스트
                print('종료하시려면 컨트롤 C')

                search_keyword2 = list(str(input()).split())[0]            
                resu = skill_search(search_keyword2,model) #유사한 스킬 반환
                time.sleep(.5)
                if len(resu) > 0:

                    print(f'{search_keyword2} 검색하신 스킬과 유사한 스킬은 다음과 같습니다..',resu)
                    time.sleep(1)
                else:
                    print('목록에 없는 스킬을 검색하셨어요 !')
                    time.sleep(1)
    else:
        company_name_plotly = draw_plotly_company_names(company_vector,tsne,new_df)
        sim_company = index_search(new_df,search_name,company_vector)
        skill_name_plotly = draw_plotly_skill_names(model,tsne)
        resu = make_mean(search_skill,company_vector,model,new_df,vec_size)
        print(sim_company)

        print(resu)
        #프롬프트 모드가 아니면 유사한 기업과 유사한스킬을 채용하는 회사 반환