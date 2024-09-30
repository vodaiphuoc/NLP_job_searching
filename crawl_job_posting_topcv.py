import requests
from bs4 import BeautifulSoup
import json



target_url = "https://www.topcv.vn/api-featured-jobs"


session = requests.Session()

request_headers = {'Origin': "https://www.topcv.vn",
                    'Priority': "u=1, i",
                    'Referer':"https://www.topcv.vn/viec-lam",
                    'Referrer Policy': "strict-origin-when-cross-origin",
                    'Sec-Ch-Ua-Platform': "Windows",
                    'Sec-Fetch-Dest': "empty",
                    'Sec-Fetch-Site': "same-origin",
                    'Sec-Fetch-Mode': "cors",
                    'Content-Length':'71',
                    'Content-Type': "application/json;charset=UTF-8",
                    'Accept': "application/json, text/plain, */*",
                    'Accept-Encoding': "gzip, deflate, br, zstd",
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    }

cookies = {"topcv_session": "eyJpdiI6Ik4wM1p5MVRhc0FhQ3NTaHYxU2hvblE9PSIsInZhbHVlIjoiMTBoZ1ZBa3dWYnhxNnpaSFk5K0tYL0tHeDI2aFZzTlRPNEZsOEx1ck5LQTdCaUFTNTRZZFpCQTFuWmt6Y3Y5Wm85aTJwaGxMdGR0SVIreGNxU1lYaHhkOGl5UXB2TlZRTVg4Rk5odE5SMjlvZk5aZjN2b3JLeGJCaDlTRUQrK0oiLCJtYWMiOiI3NDQ5NzMwNzMxZmYyOWQ2NzE0NzNkYjhjYjNiMDAxZjFhZTA2OWUyODcyZDVkMjJkNDNkZjUzNzU0MjM0ZWQyIiwidGFnIjoiIn0",
           "X-XSRF-TOKEN": "eyJpdiI6Ii9OQk16ODhPdkhkVWE2TFgrRVdkbWc9PSIsInZhbHVlIjoiOVJ6U0E4MXJWbWlMRHhGSWJFSW1xMzlwZjlmMGZKTGwxNzlZWXFYZ1BQcC9YeFlxV0Q1cFdFYnduTXNDVS9oRk9VcjZxUWlkNVpnSEc2L3FwN3h5MHh1SkMwZmtCd3R1bSt5R2ZmSnVnVlVINWpEWnhPRmxqYkdndHkwRWZvRlEiLCJtYWMiOiI1N2ZlOTA4YWJhMTBlMDVlMzMyMjdlN2I4NDgzZTllNzFiNTAzMmU1NWU4MzI4MDhmMGE2OWQzMTY0ODFlZWM4IiwidGFnIjoiIn0"
           }

payload = {"page": 2, "limit": 1000, "city": 0, "salary": None, "exp": None, "category": None, "reRanking": "[]"}

reponse = session.post(url= target_url,headers =request_headers, data=json.dumps(payload), cookies= cookies)

if reponse.status_code == 200:
    print(reponse.json())

else:
    print("Error: ", reponse.status_code)

