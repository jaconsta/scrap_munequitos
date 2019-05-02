import os
import shutil

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

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

## a for is required
# munequito_item_details = next(munequitos_i_want)

for munequito_item_details in munequitos_i_want:
    # split the url for extraction and post url creation
    munequito_url_components = munequito_item_details['link'].split('/')
    # Create munequito image folder
    munequito_folder = f'downloaded/{munequito_item_details["joined_name"]}'
    episode_number = munequito_url_components[-3]
    episode_folder = f'{munequito_folder}/{episode_number}'

    if not os.path.exists(munequito_folder):
        os.mkdir(munequito_folder)
    if not os.path.exists(episode_folder):
        os.mkdir(episode_folder)

    status = 200  # Default html response code
    page_number = 1  # It should increase for each page name
    while status == 200:
        munequito_url_components[-1] = str(page_number)
        page_url = '/'.join(munequito_url_components)
        munequito_page = requests.get(f'{site}{page_url}')
        status = munequito_page.status_code
        munequito_soup = BeautifulSoup(munequito_page.text, 'html.parser')

        if 'Page Not Found' in munequito_soup.title.text:
            status = 404
            break

        munequito_img_url = munequito_soup.img.get('src')
        img_response = requests.get(f'https:{munequito_img_url}', stream=True)

        with open(f'{episode_folder}/{page_number}.{munequito_img_url.split(".")[-1]}', 'wb') as page:
            shutil.copyfileobj(img_response.raw, page)

        del img_response
        page_number += 1


print('hello')

if __name__ == '__main__':
    pass
