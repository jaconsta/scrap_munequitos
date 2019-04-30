import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString

site = 'https://readms.net/'
page = requests.get(site)
soup = BeautifulSoup(page.text, 'html.parser')

# get_li_name = lambda x: [y for y in x[0].contents if type(y) == NavigableString][0].string
def get_li_name (x):
    content = x.contents[0]
    text = filter(lambda x: type(x) == NavigableString, content)
    return next(text)

# get_li_name = lambda x: repr(x.contents[0].contents[2].string)
get_li_date = lambda x: x.contents[0].contents[0].string
get_li_link = lambda x: x.find_all('a')[0].get('href')

get_li_values = lambda x: {'name': get_li_name(x), 'date': get_li_date(x), 'link': get_li_link(x)}

# x = [ul.find_all('a')[0]['href'] for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]
# x = [ul.find_all('a')[0] for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]
x = [get_li_values(ul) for ul in soup.find_all('ul', class_='new-list')[0].children if type(ul) != NavigableString]

munequito_site = requests.get(f'{site}{x[0].site}')

if __name__ == '__main__':
    pass
