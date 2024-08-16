# Selenium 사용해서 403 오류 해결하기!
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)

def get_page_count(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  
  browser = webdriver.Chrome(options=options)
  base_url = "https://kr.indeed.com/jobs?q="

  # 데이터 가져오기
  browser.get(f"{base_url}{keyword}")
  #  html 텍스트로 변환해줌
  soup = BeautifulSoup(browser.page_source,'html.parser')
  #  html 텍스트 중 tag가 nav이고, attrs가 {"aria-label": "pagination"}인 것 추출
  pagination = soup.find('nav',attrs={"aria-label": "pagination"})

  pagees = []

  if pagination == None:
    return 1
  
  last_page = int([i.get_text() for i in soup.find('nav',attrs={"aria-label": "pagination"}).find_all('div')][-2])
  pagees.append(last_page)
  print(pagees)
  return pagees
  # print(last_page)

def extract_indeed_jobs(keyword):
  results =[]
  pages = get_page_count(keyword)
  print("Found", pages, "pages")
  # if pages > 10:
  #   print('Too many')
  #   pages = 10
  
  for page in range(pages):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    base_url = "https://kr.indeed.com/jobs"
    final_url=f"{base_url}?q={keyword}&start={page*10}"
    print("requesting",final_url)
    browser.get(final_url)

    soup = BeautifulSoup(browser.page_source,'html.parser')
    job_list = soup.find('ul', class_='jobsearch-ResultsList')
    jobs = job_list.find_all('li', recursive=False)

    
    for job in jobs:
      zone = job.find('div', class_='mosaic-zone')
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find('span', class_='companyName')
        location = job.find('div', class_='companyLocation')
        job_data ={
          'link':f"https://kr.indeed.com{link}",
          'company':company.string.replace(",", ""),
          'location':location.string.replace(",", ""),
          'position': title.replace(",", ""),           
        }
        results.append(job_data)
  return results
