
# coding: utf-8

# In[3]:


class ARcrawler(object):
    from selenium import webdriver
    import time
    import datetime as dt
    from selenium.common.exceptions import NoSuchElementException
    import re
    
    user_agent= "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) " +                "AppleWebKit/537.36 (KHTML, like Gecko) " +                 "Chrome/37.0.2062.94 Safari/537.36"
    headers = {"User-Agent": user_agent}
    save_path = 'C:/Users/stu/git/AppReview_Crawler/output/'
    driver_path = 'C:/Users/stu/git/DA_Academy/chromedriver'
    today = dt.datetime.today().strftime('%y%m%d')
    # 접속 URL
    #게임: 최고매출
    url = 'https://play.google.com/store/apps/category/GAME/collection/topgrossing'
    results = []

    def __init__(self, rank=1, repeat=1, order=1):        
        # 찾고싶은 앱의 순위
        self.rank = rank
        # 검색 반복 횟수(기본 120개 + 1 회당 120개 리뷰 추가)
        self.repeat = repeat
        self.browser = self.webdriver.Chrome(self.driver_path)
        self.browser.get(self.url)
        self.browser.implicitly_wait(3)
        self.click_app(order)
        self.browser.implicitly_wait(3)
        self.more_pages()
        self.browser.implicitly_wait(3)
        self.results = self.get_reviews()
        
    def click_app(self, order=1):
        # rank 순위의 앱 클릭
        self.browser.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div/div/div/div[2]/div[{}]'.format(self.rank)).click()
        self.browser.implicitly_wait(3)
        #리뷰 모두보기 클릭
        self.browser.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div/div[6]/div/content/span').click()
        #리뷰를 원하는 방식으로 정렬. 기본은 최신. (1. 최신 2. 높은 평점순 3. 유용도순)
        self.browser.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div/div[2]/c-wiz/div/div/div[1]/div[2]/span').click()
        self.browser.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div/div[2]/c-wiz/div/div/div[2]/div[{}]'.format(order)).click()
        
    def page_scroll(self):
        self.scroll_pause_time = 2
        # Get scroll height
        self.last_height = self.browser.execute_script("return document.body.scrollHeight")
        print('*---자동 스크롤 시작---*')
        while True:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            self.time.sleep(self.scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            self.new_height = self.browser.execute_script("return document.body.scrollHeight")
            if self.new_height == self.last_height:
                print('*---자동 스크롤 종료---*')
                break
            self.last_height = self.new_height
            
    def more_pages(self):
        self.progress = 0
        for i in range(self.repeat): 
            self.page_scroll()
            try:
                self.browser.find_element_by_css_selector('div.JNury.Ekdcne > div > div > div.W4P4ne > div > div.PFAhAf > div > content > span').click()
                self.progress += 1
                print('*---{}번째 추가 페이지 로딩중---*'.format(self.progress))
                self.browser.implicitly_wait(3)
            
            except self.NoSuchElementException:
                print('*---불러올 페이지가 없습니다---*')
                break

    def get_reviews(self):
        print('*---데이터 수집 시작---*')
        self.ids = self.browser.find_elements_by_css_selector('div.JNury.Ekdcne > div > div > div > div > div > div > div > div.d15Mdf.bAhLNe > div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > span')
        self.rates = self.browser.find_elements_by_css_selector('div.JNury.Ekdcne > div > div > div > div > div > div > div > div.d15Mdf.bAhLNe > div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > div > span.nt2C1d > div > div')
        self.dates = self.browser.find_elements_by_css_selector('div.JNury.Ekdcne > div > div > div > div > div > div > div > div.d15Mdf.bAhLNe > div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > div > span.p2TkOb')
        self.reviews = self.browser.find_elements_by_css_selector('div.JNury.Ekdcne > div > div > div > div > div > div > div > div.d15Mdf.bAhLNe > div.UD7Dzf > span')
        print('*---데이터 수집 종료---*')
        
        self.special_chars_remover = self.re.compile("[^\w'|_]")
        self.date_chars_remover = self.re.compile('(년 |월 |일)')
        
        self.n = len(self.ids)
        print('*---데이터 정제 시작---*')
        for i in range(self.n):
            if i > 0 and i%200 == 0:
                print('*---{}번째데이터 정제중---*'.format(i))
            
            self.refined_id = self.special_chars_remover.sub(' ', self.ids[i].text)
            self.refined_rate = self.rates[i].get_attribute('aria-label').replace('별표 5개 만점에 ', '').replace('개를 받았습니다.', '')
            self.refined_date = self.date_chars_remover.sub('.', self.dates[i].text)
            self.refined_review = self.special_chars_remover.sub(' ', self.reviews[i*2].text)
            self.results.append([self.refined_id, self.refined_rate, self.refined_date, self.refined_review])
            
            if i > 0 and i%500 == 0:
                self.index = str(i)+'of'+str(self.n)
                self.save(self.index, self.results)
                print('*---중간 저장 완료({}) ---*'.format(self.index))
        
        print('*---크롤링 완료---*')
        self.save('final', self.results)
        print('*---저장 완료---*')   
    
    def save(self, index, results):
        self.csv_path = self.save_path + '{}_rank{}_app_reviews_{}.csv'.format(index, self.rank, self.today)
        with open(self.csv_path, 'w+', encoding = 'utf-8')as f:
            for result in results:
                self.text = ','.join(result)
                f.write(self.text+'\n')

