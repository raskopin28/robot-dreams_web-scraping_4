import requests
import re
import hashlib
import json
import csv
import xml.etree.ElementTree as ET
import sqlite3

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

def write_sql(data: list) -> None:
    filename = 'output.db'

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    sql = """
        create table if not exists emplois (
            id integer primary key,
            title text,
            url text
        )
    """
    cursor.execute(sql)

    for item in data:
        cursor.execute("""
            insert into emplois (title, url)
            values (?, ?)
        """, (item['title'], item['url']))

    conn.commit()
    conn.close()

def write_xml(data: list) -> None:
    filename = 'output.xml'

    root = ET.Element('Emplois')
    for item in data:
        emploi = ET.SubElement(root, 'Emploi')
        ET.SubElement(emploi, 'title').text = item['title']
        ET.SubElement(emploi, 'url').text = item['url']

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def write_json(data: list):
    output_file = "output.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

def write_csv(data: list) -> None:
    filename = 'output.csv'

    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Title'])
        writer.writerows(data)

if __name__ == '__main__':
    url = 'https://www.lejobadequat.com/emplois'
    content = get_content(url)
    regex = r'<a href=\"(.+?)\" [^>]+?>.+?<h3 class=\"jobCard_title m-0\">(.+?)</h3>'
    result = re.findall(regex, content, re.DOTALL)

    write_csv(result)

    result = [{"title": title, "url": url} for url, title in result]

    write_sql(result)
    write_xml(result)
    write_json(result)
