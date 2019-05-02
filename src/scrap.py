import os
import shutil
from collections import deque

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

from_chapters = {
    'the_seven_deadly_sins': 388
}

def get_li_name (x):
    content = x.contents[0]
    text = filter(lambda x: type(x) == NavigableString, content)
    return next(text)

# get_li_name = lambda x: repr(x.contents[0].contents[2].string)
get_li_date = lambda x: x.contents[0].contents[0].string
get_li_link = lambda x: x.find_all('a')[0].get('href')
get_file_name = lambda x: x.strip().lower().replace(' ', '_').replace('.', '_')

def get_li_values(x):
    name = get_li_name(x)
    return {'name': name, 'date': get_li_date(x), 'link': get_li_link(x), 'joined_name': get_file_name(name)}

# x = [ul.find_all('a')[0]['href'] for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]
# x = [ul.find_all('a')[0] for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]
x = [get_li_values(ul) for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]


#
#
# [(comic.text, comic.a.get('href')) for comic in soup.find_all('ul', class_='dropdown-menu')[0].children if type(comic) != NavigableString]
# (comic.text, comic.a.get('href')
#
#
pre_list = soup.find_all('ul', class_='dropdown-menu')[0].children
list_path = deque(pre_list, maxlen=2)[0].a.get('href')  # Gets the last two
list_site = requests.get(f'{site}{list_path}')
list_soup = BeautifulSoup(list_site.text, 'html.parser')

all_munequitos = [(x.a.get('href'), x.a.text, get_file_name(x.a.text)) for x in list_soup.table.find_all('tr')[1:]]

munequitos_i_want = filter(lambda x: x[-1] in expected_munequitos, all_munequitos)


for munequito_item_details in munequitos_i_want:
    munequito_chapters = requests.get(f'{site}{munequito_item_details[0]}')
    chapters_soup = BeautifulSoup(munequito_chapters.text, 'html.parser')
    chapter_list = [(chap.a.get('href'), chap.a.text, get_file_name(chap.a.text)) for chap in chapters_soup.table.find_all('tr')[1:]]

    # split the url for extraction and post url creation
    # Create munequito image folder
    munequito_folder = f'downloaded/{munequito_item_details[-1]}'
    print(munequito_folder)

    if not os.path.exists(munequito_folder):
        os.mkdir(munequito_folder)

    for chapter in chapter_list:
        chap = chapter[-1].split('-')[0].strip()[:-1]
        print(f'chapter: {chap} {chapter[1]}')
        episode_folder = f'{munequito_folder}/{chap}'
        if not os.path.exists(episode_folder):
            os.mkdir(episode_folder)

        chapter_path = chapter[0][:-1]

        status = 200  # Default html response code
        page_number = 1  # It should increase for each page name
        while status == 200:
            print(page_number)
            munequito_page = requests.get(f'{site}{chapter_path}{str(page_number)}')
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
