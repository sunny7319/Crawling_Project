from selenium import webdriver
import pandas as pd
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC   
from selenium.webdriver.support.ui import WebDriverWait
from model import *
import konlpy
class CModels():
    def __init__(self):
        pass
    
    #원티드 인사이트 크롤링
    def company_info(data):
        driver = webdriver.Chrome()
        driver.get('https://insight.wanted.co.kr/')
        company_df = pd.DataFrame(columns= ['업종분류','사원수','연혁','기업형태','매출액','홈페이지','평균연봉'])
        company_names = data
        class_list = []
        num_worker_list = []
        made_list = []
        company_cla = []
        money_list = []
        homepage_list = []
        worker_money_list = []
        for i in company_names:  # 사이트에 등록된 기업명으로 검색
            if i == '피어테크(지닥)':
                i = '피어테크'
            elif i == '아인잡(AINJOB)':
                i = '아인잡'
            time.sleep(1)
            
            driver.find_element(By.XPATH,f'//*[@id="__next"]/div[1]/main/div/div/div[1]/button/div[2]').click()
            time.sleep(2)
            
            driver.find_element(By.XPATH,f'//*[@id="__next"]/div[2]/div/div/form/div/div/input').click()
            keyword = i
            element = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div/div/form/div/div/input')
            element.send_keys(keyword)
            time.sleep(1)
            element.send_keys('\n')
            time.sleep(4)
            try:

                class_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div[2]/dl[1]/dd').text) #업종분류
                num_worker_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div[2]/dl[9]/dd').text[:-2])
                made_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div[2]/dl[2]/dd').text)
                company_cla.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div[2]/dl[5]/dd').text)
                money_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div[2]/dl[4]/dd').text[:-2])
                homepage_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div[2]/dl[12]/dd').text)

                worker_money_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div[2]/dl[6]/dd').text[:-2])
            except:
                
                class_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div/dl[1]/dd').text) #업종분류
                num_worker_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div/dl[9]/dd').text[:-2])
                made_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div/dl[2]/dd').text)
                company_cla.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div/dl[5]/dd').text)
                money_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div/dl[4]/dd').text[:-2])
                homepage_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div/dl[8]/dd').text)

                worker_money_list.append(driver.find_element(By.XPATH,'//*[@id="summary"]/div[2]/div/dl[6]/dd').text[:-2])
            driver.back()
        company_df['업종분류'] = class_list
        company_df['사원수'] = num_worker_list
        company_df['연혁'] = made_list
        company_df['기업형태'] = company_cla
        company_df['매출액'] = money_list
        for i in range(len(homepage_list)):
            if homepage_list[i][0] != 'h':
                homepage_list[i] = '-'
            
        company_df['홈페이지'] = homepage_list
        company_df['평균연봉'] = worker_money_list

        return company_df

    
    #원티드 크롤링
    def wanted_craw():
        driver = webdriver.Chrome()
        driver.get('https://www.wanted.co.kr/search?query=aws&tab=position') #AWS 직무 검색된 페이지로 이동
        time.sleep(5) #혹시모를 네트워크 장애 대비
        actions = driver.find_element(By.CSS_SELECTOR, 'body') # home, end 키 설정을 위함
        all_ = int(driver.find_element(By.XPATH,'//*[@id="search_tabpanel_position"]/div/div[1]/h2/span').text) #모든 공고 숫자
        tcnt = len(driver.find_elements(By.CLASS_NAME,"JobCard_container__FqChn.JobCard_container--variant-card__znjV9")) #반응형이라서 표시된 공고 카운팅
        while tcnt < all_: #표시된 공고가 전체 공고보다 작을 때 
            actions.send_keys(Keys.END) #end를 계속 누름
            tcnt = len(driver.find_elements(By.CLASS_NAME,"JobCard_container__FqChn.JobCard_container--variant-card__znjV9")) #count 다시 계산
            time.sleep(2) 
            print(tcnt)
        time.sleep(1)
        actions.send_keys(Keys.HOME) #위로 올라감
        time.sleep(3)
        import pandas as pd
        wanted_df = pd.DataFrame(columns= ['기업명','주소','직급','기술스택','자격요건','우대사항','url','기업url'])
        # 데이터 설정
        loca_list = []
        name_list = []
        must_list = []
        prefer_list = []
        experience_list = []
        url_list = []
        for j in range(1,all_+1):
            driver.find_element(By.XPATH,f'//*[@id="search_tabpanel_position"]/div/div[4]/div[{j}]/a/div[2]/strong').click() # J번째 공고 클릭 

            time.sleep(3)
            company_name = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/a').text #기업이름
            

            name_list.append(company_name) 
            time.sleep(.5)
            driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/button').send_keys(Keys.ENTER)#.click() #클릭 안되는 오류로 인해서 엔터로 상세 페이지
            experience = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/span[4]').text #경력
            experience_list.append(experience)
            url_list.append(driver.current_url) #해당 페이지 URL
            
            actions.send_keys(Keys.PAGE_DOWN) #내려가기
            
            time.sleep(1)
            try:
                location = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[1]/div/section/section/article[4]/div/div/span').text
                loca_list.append(location)    #위치
            except:
                location = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[1]/div/section/section/article[5]/div/div/span').text
                loca_list.append(location)         
            time.sleep(3)

            
            for i in range(2,4):
                
                if i == 2:
                    must = re.sub('•','',driver.find_element(By.XPATH,f'//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[{i}]').text).split('\n')[1:]
                    #자격요건
                elif i == 3:
                    prefer = re.sub('•','',driver.find_element(By.XPATH,f'//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div[{i}]').text).split('\n')[1:]
                    #우대사항
            must_list.append(must)
            prefer_list.append(prefer)
            driver.back() #뒤로가기
        wanted_df['주소'] = loca_list #['기업명','주소','직급','기술스택','자격요건','우대사항','url','기업url']
        wanted_df['기업명'] = name_list
        wanted_df['직급'] = experience_list
        wanted_df['자격요건'] = must_list
        wanted_df['우대사항'] = prefer_list
        wanted_df['url'] = url_list
        
        for i in range(len(wanted_df)):
            data = DataPreprocessing(must_list[i]).change_data()
            #기술스택 추출하기 위해서 자격요건에서 영어 데이터만 사용
            wanted_df['기술스택'][i] = DataPreprocessing(data).only_eng()
        return wanted_df
    

    # 프로그래머스 크롤링
    def prog_craw():
        page_no = 1
        programmers_url = f"https://career.programmers.co.kr/job?page={page_no}&tags=AWS%20Alexa&tags=AWS%20CloudFront&tags=AWS%20CloudWatch&tags=AWS%20DynamoDB&tags=AWS%20EC2&tags=AWS%20RDS&tags=AWS%20Redshift&tags=AWS%20S3&tags=AWS%20IAM&tags=AWS%20Lambda&tags=AWS%20Polly&tags=AWS%20ElastiCache&tags=AWS%20Pinpoint&tags=AWS%20ElasticBeanstalk&tags=AWS%20ECS&tags=AWS%20CodePipeline&tags=AWS%20Amplify&tags=AWS%20AppStream&tags=AWS%20AppSync&tags=AWS%20Artifact&tags=AWS%20Athena&tags=AWS%20Backup&tags=AWS%20Batch&tags=AWS%20Budgets&tags=AWS%20Chime&order=recent"
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 창을 열지 않고 실행

        driver = webdriver.Chrome(options= option)
        driver.get(programmers_url)
        # jobs라는 변수에 aws 관련 모든 공고 갯수를 지정해줌. 자료형 int로 바꾸어주었음.
        jobs = int(re.sub('개의 포지션','',driver.find_element(By.XPATH,'//*[@id="list-positions-wrapper"]/div/div[1]/h6').text))
        
        # 한 페이지에 표현되는 공고 건수 20개
        # 총 공고 건수에서 20을 나누어 max page를 컨트롤 하겠음
        max_page = jobs//20 + 1
        programmers_df = pd.DataFrame(columns= ['기업명','주소','직급','기술스택','자격요건','우대사항','url','기업url'])

        for page_no in range(1, max_page+1):
            programmers_url = f"https://career.programmers.co.kr/job?page={page_no}&tags=AWS%20Alexa&tags=AWS%20CloudFront&tags=AWS%20CloudWatch&tags=AWS%20DynamoDB&tags=AWS%20EC2&tags=AWS%20RDS&tags=AWS%20Redshift&tags=AWS%20S3&tags=AWS%20IAM&tags=AWS%20Lambda&tags=AWS%20Polly&tags=AWS%20ElastiCache&tags=AWS%20Pinpoint&tags=AWS%20ElasticBeanstalk&tags=AWS%20ECS&tags=AWS%20CodePipeline&tags=AWS%20Amplify&tags=AWS%20AppStream&tags=AWS%20AppSync&tags=AWS%20Artifact&tags=AWS%20Athena&tags=AWS%20Backup&tags=AWS%20Batch&tags=AWS%20Budgets&tags=AWS%20Chime&order=recent"
        
            driver = webdriver.Chrome(options= option)
            driver.get(programmers_url)
            time.sleep(3) # 타임슬립 안 걸어주면 로딩 다 안 된 상태라 오류남
            
            # 현재 page_no에서 표시되는 공고의 갯수를 확인
            현재페이지공고 = len(driver.find_elements(By.XPATH,'//*[@id="list-positions-wrapper"]/ul/li'))
            
            for i in range(1, 현재페이지공고+1):
                
                # 첫번째 공고부터 차례대로 클릭해서 크롤링하겠음
                driver.find_element(By.XPATH,f'//*[@id="list-positions-wrapper"]/ul/li[{i}]').click()
                time.sleep(.5)
                # 새로운 창으로 포커스 변경
                driver.switch_to.window(driver.window_handles[-1])
                
                time.sleep(2)
            
                # 기업명
                try:
                    기업명 = driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').text 

                except:
                    기업명 = driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div[1]/div[1]/div[1]/header/div/div[2]/h4/a').text                   
                
                # 주소
                # 주소의 경우 명시되지 않은 공고가 있어, 해당 경우 결측치 부여
                try:
                    주소 = driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[2]/div/div[2]').text
                except NoSuchElementException:
                    주소 = float('nan')
                    
                # 직급 (경력)
                # 직급의 경우 명시되지 않은 공고가 있어, 해당 경우 결측치 부여
                try:
                    직급 = driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[4]/div[2]').text
                except NoSuchElementException:
                    직급 = float('nan')
                    
                # 기술스택
                기술스택 = driver.find_elements(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/div[2]/section/ul')[0].text.split('\n')

                # 자격요건
                # 3가지의 다른 태그(<p>,<ul>,<ol>)로 분류되어 있어 예외 반영
                try:
                    자격요건 = [a.lstrip('• ').lstrip('○') for a in driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/div[3]/section[2]/div/div/p').text.split('\n')]
                except NoSuchElementException:
                    try: 
                        자격요건 = [a.lstrip('• ').lstrip('○') for a in driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/div[3]/section[2]/div/div/ul').text.split('\n')]
                    except NoSuchElementException:
                        자격요건 = [a.lstrip('• ').lstrip('○') for a in driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/div[3]/section[2]/div/div/ol').text.split('\n')]


                # 우대사항
                # 3가지의 다른 태그(<p>,<ul>,<ol>)로 분류되어 있어 예외 반영
                try:
                    우대사항 = [a.lstrip('• ').lstrip('○') for a in driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/div[3]/section[3]/div/div/p').text.split('\n')]
                except NoSuchElementException:
                    try:
                        우대사항 = [a.lstrip('• ').lstrip('○') for a in driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/div[3]/section[3]/div/div/ul').text.split('\n')]
                    except NoSuchElementException:
                        우대사항 = [a.lstrip('• ').lstrip('○') for a in driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/div[3]/section[3]/div/div/ol').text.split('\n')]
                
                # 해당 공고 url
                url = driver.current_url
                
                # 기업 url
                driver.find_element(By.XPATH,'//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').click()
                기업url = driver.find_elements(By.CLASS_NAME, "list-value" )[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                
                
                # 임시 데이터프레임 생성
                programmers_df_temp = pd.DataFrame([기업명, 주소, 직급, 기술스택, 자격요건, 우대사항, url, 기업url],
                                        index = ['기업명','주소','직급','기술스택','자격요건','우대사항','url','기업url']).T
                
                # 최종 데이터프레임과 합치기, 인덱스 번호 초기화
                programmers_df = pd.concat([programmers_df, programmers_df_temp]).reset_index(drop=True)
                
                driver.close()
                time.sleep(.5)
                driver.switch_to.window(driver.window_handles[-1])
        return programmers_df
    

    # 랠릿 크롤링
    def rallit_craw():
        '''
        stext : 검색내용
        page_no : 크롤링할 페이지
        '''
        stext = 'AWS'
        page_no = 1

        Rallit_data = pd.DataFrame(columns=['기업명', '주소', '직급', '기술스택', '자격요건', '우대사항', 'url', '기업url'])

        while 1:
            
            url = f'https://www.rallit.com/?jobSkillKeywords={stext}&pageNumber={page_no}'
            # import html data
            driver = webdriver.Chrome()
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # 5페이지 이상은 '검색결과가 없어요'가 뜸
            if '검색결과가 없어요' in soup.text:
                break

            기업명 = []
            직급 = []
            기술스택 = []
            url = []
            자격요건 = []
            우대사항 = []
            주소 = []
            기업url = []
            
            # 한 페이지 안의 공고 수
            post_num = len(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[3]/ul/li'))

            for i in range(1, post_num+1):

                # 기업명, 직급, 기술스택, url parsing
                기업명.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[3]/ul/li[{i}]/article/a/div[1]/div[1]/div[1]/p').text)
                직급.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[3]/ul/li[{i}]/article/a/div[1]/div[2]/span[1]/p').text)
                기술스택.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[3]/ul/li[{i}]/article/a/div[1]/ul').text.split('\n'))
                url.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[3]/ul/li[{i}]/article/a').get_attribute('href'))



                # 제목 눌러서 url 사이트로 이동 ==> 자격요건, 우대사항 parsing
                driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[3]/ul/li[{i}]/article/a/div[1]/div[1]/div[2]').click()
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)

                try:     # 자격요건과 우대사항의 XPATH가 다른 기업이 있음
                    자격요건.append(re.sub('[-•]+', '', driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[1]/section[2]/div[1]/section[2]/section[2]/p').text).split('\n'))
                    우대사항.append(re.sub('[-•]+', '', driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[1]/section[2]/div[1]/section[2]/section[3]/p').text).split('\n'))
                except:     
                    자격요건.append(re.sub('[-•]+', '', driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[1]/section/div[1]/section[2]/section[2]/p').text).split('\n'))
                    우대사항.append(re.sub('[-•]+', '', driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[1]/section/div[1]/section[2]/section[3]/p').text).split('\n'))



                # 회사명 눌러서 새로운 창으로 이동 ==> 전체 주소, 기업url parsing
                try:     # 회사명 누르는 XPATH가 다른 기업이 있음
                    driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[1]/section[2]/div[2]/div/aside/div[1]/div/dl[4]/div/dd/a').click()
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[-1])   # focus 창 이동
                    주소.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/section[2]/aside/div[1]/dl[1]/div[2]/dd').text)
                    기업url.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/section[2]/aside/div[1]/dl[1]/div[1]/dd/a').get_attribute('href'))

                    driver.close()   # 맨 마지막에 열어놓은 창 종료 (창 하나만 닫는거)
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.back()   # 뒤로가기
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[-1])   # 원래 처음 창으로 focus 이동
                except:
                    try:     # 새로운 창으로 이동 후 
                        driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[1]/section[2]/div[2]/div/aside/div[1]/div/dl[5]/div/dd/a').click()
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[-1])   # focus 창 이동

                        주소.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/section[2]/aside/div[1]/dl[1]/div[2]/dd').text)
                        기업url.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/section[2]/aside/div[1]/dl[1]/div[1]/dd/a').get_attribute('href'))

                        driver.close()   # 맨 마지막에 열어놓은 창 종료 (창 하나만 닫는거)
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.back()   # 뒤로가기
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[-1])   # 원래 처음 창으로 focus 이동  
                    except:
                        driver.find_element(By.XPATH, f'//*[@id="__next"]/main/div/section[1]/section/div[2]/div/aside/div[1]/div/dl[4]/div/dd/a').click()
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[-1])   # focus 창 이동
                        주소.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/section[2]/aside/div[1]/dl[1]/div[2]/dd').text)
                        기업url.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/main/section/section[2]/aside/div[1]/dl[1]/div[1]/dd/a').get_attribute('href'))

                        driver.close()   # 맨 마지막에 열어놓은 창 종료 (창 하나만 닫는거)
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.back()   # 뒤로가기
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[-1])   # 원래 처음 창으로 focus 이동

            res = pd.DataFrame([기업명, 주소, 직급, 기술스택, 자격요건, 우대사항, url, 기업url], 
                            index=['기업명', '주소', '직급', '기술스택', '자격요건', '우대사항', 'url', '기업url']).T
            Rallit_data = pd.concat([Rallit_data, res])
            
            # 다음페이지로
            page_no += 1
        return Rallit_data
    
class DataPreprocessing():
    def __init__(self,data):
        self.data = data

    def change_data(self):  # 리스트 형식으로 변경
        result_list = []
        for i in range(len(self.data)):
            result_list.append([item.strip(" '[]") for item in self.data[i].split(',')])
        return result_list
    
    def only_eng(self):  # 영어 데이터만 가져오기
        result_list = self.data
        for i in range(len(result_list)):
            for j in range(len(result_list[i])):
                
                result_list[i][j] = ' '.join(re.findall(r'[a-zA-Z]+', result_list[i][j]))
            result_list[i] = [x for x in result_list[i] if x != '']
        for i in result_list:
            if i == []:

                result_list.remove(i)
        return result_list
    
    def data_concat(data1,data2,data3):
        inte_data = pd.concat([pd.concat([data1,data2],axis=0),data3],axis=0)
        inte_data = inte_data.reset_index().drop('index',axis=1)
        return inte_data
    
    def name_chk(data):  # 사이트에 등록된 기업명으로 검색
        if data == '인프랩 (인프런)':
            data = '인프랩'
        elif data == '(주) 미스터카멜':
            data = '미스터카멜'
        elif data[:3] == '(주)':
            data = data[3:]
        elif data == '브레이브모바일 (숨고)':
            data = '브레이브모바일'
        elif data == '코코네 M':
            data = '코코네'
        elif data == '주식회사그로잉랩':
            data = '그로잉랩'
        elif data[:4] == '주식회사':
            try:
                data = data[5:]
            except:
                pass
        elif data == '사이벨 헬스 (주)':
            data = '사이벨헬스'
        elif data == '빅웨이브로보틱스(주)':
            data = '빅웨이브로보틱스'
        elif data == '피어테크(지닥)':
            data = '피어테크'
        elif data == '아인잡(AINJOB)':
            data = '아인잡'
        elif data == 'AB180':
            data = '에이비일팔공'
        elif data == '피나클 FINAKLE':
            data = '피나클'
        elif data == '유한회사 일루미나리안':
            data = '일루미나리안'
        elif data == '런치팩 주식회사':
            data = '런치팩'
        elif data == '바텍 네트웍스':
            data = '바텍'
        elif data == '에이치디현대글로벌서비스':
            data = '에이치디현대'
        elif data == '롯데헬스케어 주식회사':
            data = '롯데헬스케어'
        elif data == '바티AI':
            data = '바티에이아이'
        elif data == '리본솔루션':
            data = '닥터리본'
        return data
    

# 매출액, 평균연봉 전처리
def all_preprocess(integrated_data):
    integrated_data['사원수'] = integrated_data['사원수'].apply(lambda x:int(x.replace('-','1')))
    def convert_price(x):
        if '-' in x:
            return 42157500  # 결측치 평균연봉 하위 25%로 대체

         # '만,억,조'를 숫자로 변환
        단위 = re.findall('[가-힣]', x) 
        끝단위 = 단위[-1]
        if 끝단위 == '만':
            price = re.findall('\d+', x.replace(',', '').replace('만', '만0000'))
        elif 끝단위 == '억':
            price = re.findall('\d+', x.replace(',', '').replace('억', '억00000000'))
        elif 끝단위 == '조':
            price = re.findall('\d+', x.replace(',', '').replace('조', '조000000000000'))

        return int(''.join([i.zfill(4) for i in price]))
   

    def 경력_cat(x):
        if pd.isnull(x) or x == 'nan':  # 결측치 신입으로 대체
            return '신입'
        
        # 정규표현식을 사용하여 문자열에서 숫자 추출
        숫자 = re.findall('\d', x)
        if 숫자:  # 추출된 숫자가 있는 경우
            경력년수 = int(숫자[0])  # 추출된 숫자 중 첫 번째 숫자를 사용
            if 경력년수 <= 3:
                return '주니어'
            elif 경력년수 <= 8:
                return '미들'
            else:
                return '시니어'
        else:  # 추출된 숫자가 없는 경우
            if any([i in x for i in ['신입', '인턴', '무관']]):
                return '신입'
            else:
                return '시니어'
    
    integrated_data['평균연봉'] = integrated_data['평균연봉'].apply(lambda x:convert_price(x))
    integrated_data['매출액'] = integrated_data['매출액'].apply(lambda x:convert_price(x))
    integrated_data['직급'].fillna('경력 무관')
    integrated_data['직급'] = integrated_data['직급'].apply(lambda x: 경력_cat(x))


    # 주소 결측치 행 '미기재'로 대체
    integrated_data.loc[integrated_data['주소'] !=integrated_data['주소'], '주소'] = '미기재'

    # '구' 미포함 행 '미기재'로 대체
    integrated_data.loc[~integrated_data['주소'].str.contains('구'), '주소'] = '미기재'
    #integrated_data['주소'].apply(lambda x: np.nan if not x.str.contains('구') else x)

    # 시작부분 '서울' '경기' 로 통일
    replace_dict = {'대한민국 ':'', '서울특별시': '서울', '서울시': '서울', '경기도':'경기', r'^\d+\s+': ''}
    integrated_data['주소'] = integrated_data['주소'].replace(replace_dict, regex=True)

    # '구' 이름만 기재하는 경우 앞에 '서울' 추가
    integrated_data['주소'] = integrated_data['주소'].apply(lambda x: '서울 ' + x if not x.startswith(('서울', '경기', '인천', '부산', '미기재')) else x)

    # ~구 이후 문자열 제외
    def address_extact(x):
        if x == '미기재':
            return x
        else:
            x= re.match(r'(.*?)구', x).group(0)
            return x

    integrated_data['주소'] =integrated_data['주소'].apply(lambda x: address_extact(x).replace('서울 구', '서울 구로구'))

    result_list = change_data(integrated_data['기술스택'])
    integrated_data['기술스택'] = result_list
    integrated_data = integrated_data.fillna('-')
    integrated_data = integrated_data.drop('홈페이지',axis=1)

    df = integrated_data.iloc[:, [4,5]]
    
    # 텍스트 마이닝은 KoNLPy의 Kkma 패키지를 이용해주겠습니다.
    # 한국어와 영어를 동시에 처리해주는 기능이 없으므로 따로 처리해줄게요.
    kkma = konlpy.tag.Kkma()

    # '자격요건' 열에서 한글 명사만 뽑아주기
    df['자격요건_한글명사'] = df['자격요건'].apply(kkma.nouns)

    # '자격요건' 열에서 영어 명사만 뽑아주기
    # 이 때, React.js와 Next.js가 . 을 기준으로 나뉘어지기 때문에 처리해주었습니다.
    df['자격요건_영어명사'] = df['자격요건'].apply(
        lambda x: re.findall(
            r'\b(?:React\.js|Next\.js|[A-Za-z]+(?:\.js)?)\b', x))

    # 위와 같은 방법으로 '우대사항'열도 처리해주겠습니다.
    df['우대사항_한글명사'] = df['우대사항'].apply(kkma.nouns)
    df['우대사항_영어명사'] = df['우대사항'].apply(
        lambda x: re.findall(
            r'\b(?:React\.js|Next\.js|[A-Za-z]+(?:\.js)?)\b', x))
    자격_한글_list = [item for sublist in df['자격요건_한글명사'].values for item in sublist]
    자격_영어_list = [item for sublist in df['자격요건_영어명사'].values for item in sublist]
    우대_한글_list = [item for sublist in df['우대사항_한글명사'].values for item in sublist]
    우대_영어_list = [item for sublist in df['우대사항_영어명사'].values for item in sublist]

    # 한글명사와 영어명사 리스트를 더해서 하나의 리스트로 만들어줄게요.
    자격요건_list = 자격_한글_list + 자격_영어_list
    우대사항_list = 우대_한글_list + 우대_영어_list
    stp_df = pd.read_csv('./불용어 리스트.csv')
    stp_list = stp_df['Stopword'].tolist()
    자격요건_list = [i for i in 자격요건_list if i not in stp_list]
    우대사항_list = [i for i in 우대사항_list if i not in stp_list]

    for i in range(len(df['자격요건_한글명사'])):
       
        df['자격요건_한글명사'][i].extend(df['자격요건_영어명사'][i])
        df['우대사항_한글명사'][i].extend(df['우대사항_영어명사'][i])


    integrated_data['자격요건_키워드'] = df['자격요건_한글명사']
    integrated_data['우대사항_키워드'] = df['우대사항_한글명사']

    for i in range(len(integrated_data['자격요건_키워드'])):
        
        integrated_data['자격요건_키워드'][i] = [j for j in integrated_data['자격요건_키워드'][i] if j not in stp_list]
        integrated_data['우대사항_키워드'][i] = [j for j in integrated_data['우대사항_키워드'][i] if j not in stp_list]
    
    # 사원수 100명 단위로 범주화
    def change(data):
        if data <= 100:
            data = '100명이하'
        elif data >100 and data <= 200:
            data = '100명 초과 200명 이하'
        elif data > 200 and data <=300:
            data = '200명 초과 300명 이하'
        else:
            data = '300명 초과' 
        return data
    integrated_data['사원수_범주형'] = integrated_data['사원수'].apply(lambda x : change(int(x)))
    integrated_data.to_csv('preprocessing_integrated.csv')
    return integrated_data