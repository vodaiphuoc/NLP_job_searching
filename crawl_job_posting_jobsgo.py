import requests
from bs4 import BeautifulSoup
import json



request_headers = {'Host': "jobsgo.vn",
                    'Referer':"https://jobsgo.vn/",
                    'Referrer Policy': "strict-origin-when-cross-origin",
                    'Sec-Ch-Ua-Platform': "Windows",
                    'Sec-Fetch-Dest': "document",
                    'Sec-Fetch-Site': "same-origin",
                    'Sec-Fetch-Mode': "navigate",
                    'Sec-Fetch-User': "?1",
                    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    'Accept-Encoding': "gzip, deflate, br, zstd",
                    'Accept-Language': "en-US,en;q=0.9,vi;q=0.8",
                    'Connection': "keep-alive",
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    }


def make_content_per_cate(url:str, num_job_per_page = 50):
    total_link_in_category = []

    # this is first page
    response =requests.get(url= url, headers= request_headers, allow_redirects= False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        num_pages_region = soup.find_all("span", {"class": "pull-right"})
        start_end, total_jobs = (num_pages_region[0].contents[-1].split("/"))
        start, end  = (start_end.split(" - "))

        assert -int(start) + int(end) + 1 == num_job_per_page, f"found {int(start) - int(end) + 1}"
        total_pages = int(total_jobs)//50 + 1

        response =requests.get(url= url, headers= request_headers, allow_redirects= False)
        soup = BeautifulSoup(response.content, "html.parser")
        target_region = soup.find_all("div", {"class": "brows-job-company-img"})
        page_1_job_links = [each_tag.find_all("a", href = True)[0]["href"] for each_tag in target_region]
        total_link_in_category.extend(page_1_job_links)
    else:
        print("Error: ", response.status_code)

    # this is for from page 2 to the total_pages
    for page_number in range(2, total_pages+1):
        response =requests.get(url= url+f"?page={page_number}", headers= request_headers, allow_redirects= False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            target_region = soup.find_all("div", {"class": "brows-job-company-img"})
            job_links = [each_tag.find_all("a", href = True)[0]["href"] for each_tag in target_region]
            total_link_in_category.extend(job_links)

    assert len(total_link_in_category) == int(total_jobs), f"Found {len(total_link_in_category)} with {int(total_jobs)}"
    return total_link_in_category


def single_job_processing(job_url:str, max_chidlren_elements= 20):
    """
    Region 1: includes job_type, level, age, skills
    Region 2: JD, requirements, benefit
    
    """
    response =requests.get(url = job_url, headers = request_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        region = soup.find_all("div", {"class": ["content-group mrg-top-25","content-group"]})

        # filter by counting number of children in each element
        filtered_elemnts = [ele for ele in region if len(ele.findChildren()) < max_chidlren_elements]
        
        key_tags = [ele.find(["p","h2"], {"class":"h5 text-semibold"}).string for ele in filtered_elemnts]
        

        values_tags = []
        for ele in filtered_elemnts:

            str_value = ""
            list_ele = ele.find(["p","a","div"])

            if len(list_ele) == 1:
                str_value = list_ele.string
            else:
                # str_value = " ".join([ele.contents for ele in list_ele])
                str_value = list_ele.contents

            values_tags.append(str_value)

        print(values_tags)

    else:
        return False



if __name__ == "__main__":

    job_links = []
    job_categoricals = ["ke-toan-kiem-toan", 
                        "tai-chinh-ngan-hang",
                        "hanh-chinh-van-phong",
                        "kinh-doanh-ban-hang",
                        "marketing",
                        "xay-dung",
                        "it-phan-mem",
                        "hanh-chinh-van-phong"
                        ]

    # for categorical in job_categoricals:
    current_target_url = f"https://jobsgo.vn/viec-lam-{job_categoricals[0]}.html"
    current_job_links = make_content_per_cate(url= current_target_url)
    job_links.extend(current_job_links)

    print(job_links[0])
    single_job_processing(job_url= job_links[0])