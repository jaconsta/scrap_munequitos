import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import shutil

site = 'https://readms.net/'
page = requests.get(site)
soup = BeautifulSoup(page.text, 'html.parser')

expected_munequitos = [
    'one-punch_man',
    'the_seven_deadly_sins'
]

# get_li_name = lambda x: [y for y in x[0].contents if type(y) == NavigableString][0].string
def get_li_name (x):
    content = x.contents[0]
    text = filter(lambda x: type(x) == NavigableString, content)
    return next(text)

# get_li_name = lambda x: repr(x.contents[0].contents[2].string)
get_li_date = lambda x: x.contents[0].contents[0].string
get_li_link = lambda x: x.find_all('a')[0].get('href')
get_file_name = lambda x: x.strip().lower().replace(' ', '_')

def get_li_values(x):
    name = get_li_name(x)
    return {'name': name, 'date': get_li_date(x), 'link': get_li_link(x), 'joined_name': get_file_name(name)}

# x = [ul.find_all('a')[0]['href'] for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]
# x = [ul.find_all('a')[0] for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]
x = [get_li_values(ul) for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]

munequitos_i_want = filter(lambda x: x['joined_name'] in expected_munequitos, x)
munequito_page = requests.get(f'{site}{x[0]["link"]}')
munequito_soup = BeautifulSoup(munequito_page.text, 'html.parser')

munequito_img_url = munequito_soup.img.get('src')
img_response = requests.get(f'https:{munequito_img_url}', stream=True)

with open('downloaded/first.png', 'wb') as comic_file:
    shutil.copyfileobj(img_response.raw, comic_file)

del img_response


print('hello')

if __name__ == '__main__':
    pass
