import lxml.html as html
import requests

SEARX_URL = 'https://swag.pw/search'
query = 'Җырларым, сез шытып йөрәгемдә'

def search(query):
    result = requests.get(
        f'{SEARX_URL}?q='
        f'{query}&category_general=on&language=ru-RU&time_range=&safesearch=0&theme=simple')

    return result.text

result = search(query)

tree = html.fromstring(result)
links = tree.xpath('body//article//a/@href')

print(links)

for link in links:
    response = requests.get(link)
    tree = html.fromstring(response.text)
    all_text = tree.text_content().strip()