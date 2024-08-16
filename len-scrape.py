import requests
from bs4 import BeautifulSoup

all_jobs = []

def scrape_page(url):
    print(f"Scrapping {url}...")
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("section", class_="jobs").find_all("li")[0:-1]
        
    """
    #첫 번째 방법
    for job in jobs:
        title = job.find("span", class_="title").text
        company, position, region = job.find_all("span", class_="company")
        company = company.text
        position = position.text
        region = region.text
        print(title, company, position, region, "---------/n")
    """

    #두번째 방법
    for job in jobs:
        title = job.find("span", class_="title").text
        company, position, region = job.find_all("span", class_="company")
        url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
        #same
        #url = job.find("a")
        #if url:
        #   url = url["href"]
        job_data = {
            "title": title, 
            "company": company.text,
            "position": position.text, 
            "region": region.text,
            "url": f"https://weworkremotely.com{url}",
        }
        all_jobs.append(job_data)        

def get_pages(url):
    response = requests.get("url", headers={
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})

    soup = BeautifulSoup(response.content, "html.parser")

    return len(soup.find("div", class_="pagination").find_all("span", class_="page"))
    
total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")

for x in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)

print(len(all_jobs))