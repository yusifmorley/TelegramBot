import requests
from urllib.parse import quote

#与nodejs 交互
main_url0="http://127.0.0.1:3000/android?query="
main_url1="http://127.0.0.1:3000/desktop?query="
head = {
        'Content-Type': 'application/octet-stream'
    }
def get_from(theme_type,theme_name,theme_data):
    if theme_type == "android":
       url = main_url0 + quote(theme_name)
    else:
       url = main_url1 + quote(theme_name)

    content= requests.post(url, data=theme_data,headers=head).content

    if content != b'fail':
        return  content
    else:
        return None

