import requests
import re
import hashlib
import json

def get_content(url):
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(name, 'r') as f:
            content = f.read()
            return content
    except:
        response = requests.get(url)
        with open(name, 'w') as f:
            f.write(response.text)
        return response.text

if __name__ == '__main__':
    url = 'https://www.lejobadequat.com/emplois'
    content = get_content(url)
    regex = r'<a href=\"(.+?)\" [^>]+?>.+?<h3 class=\"jobCard_title m-0\">(.+?)</h3>'
    result = re.findall(regex, content, re.DOTALL)

    result = [{"title": title, "url": url} for url, title in result]

    output_file = "result.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)