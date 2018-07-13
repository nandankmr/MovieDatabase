from requests import get
from bs4 import BeautifulSoup
from home.models import Director, Actor


def director_data(link):
    # with open('E:/imdb.html') as data:
    #     html_data = data.read()
    all_data = dict()

    html_data = get(link).content
    html_soup = BeautifulSoup(html_data, 'html.parser')
    all_data['name'] = html_soup.find('h1').span.text
    try:
        all_data['logo'] = \
            html_soup.find('div', attrs={'id': 'name-overview-widget'}).find('div', class_='image').a.img['src']
    except:
        all_data['logo'] = '#'
    all_data['profession'] = ', '.join(
        [x.span.text.strip() for x in html_soup.find('div', class_="infobar").find_all('a')])
    all_data['imdb_link'] = link
    try:
        all_data['dob'] = \
            [', '.join([str(y.text) for y in x.time.find_all('a')]) for x in
             html_soup.find_all('div', class_='txt-block') if
             x['id'] == 'name-born-info'][0]
    except:
        all_data['dob'] = 'Unknown'
    try:
        all_data['birth_place'] = \
            [x.find_all('a')[-1].text for x in html_soup.find_all('div', class_='txt-block') if
             x['id'] == 'name-born-info'][0]
    except:
        all_data['birth_place'] = 'Unknown'

    all_data['movies'] = [[z.a.text, 'https://imdb.com/' + z.a['href'].split('?')[0]] for z in
                          [y for y in html_soup.find_all('div', class_='filmo-category-section') if
                           y.div['id'].startswith('director')][0].find_all('div') if z.a is not None]
    adding_actor(all_data)


def adding_director(data):
    database = Director()
    database.logo = data['logo']
    database.name = data['name']
    database.imdb_link = data['imdb_link']
    database.date_of_birth = data['dob']
    database.profession = data['profession']
    database.birth_place = data['birth_place']
    database.movies = '|'.join([x[0] for x in data['movies']])
    database.movie_links = '|'.join([x[1] for x in data['movies']])
    database.save()
    print(database.name)



def actor_data(link):
    # with open('E:/imdb.html') as data:
    #     html_data = data.read()
    all_data = dict()

    html_data = get(link).content
    html_soup = BeautifulSoup(html_data, 'html.parser')
    all_data['name'] = html_soup.find('h1').span.text
    try:
        all_data['logo'] = \
            html_soup.find('div', attrs={'id': 'name-overview-widget'}).find('div', class_='image').a.img['src']
    except:
        all_data['logo'] = '#'
    all_data['profession'] = ', '.join(
        [x.span.text.strip() for x in html_soup.find('div', class_="infobar").find_all('a')])
    all_data['imdb_link'] = link
    try:
        all_data['dob'] = \
            [', '.join([str(y.text) for y in x.time.find_all('a')]) for x in
             html_soup.find_all('div', class_='txt-block') if
             x['id'] == 'name-born-info'][0]
    except:
        all_data['dob'] = 'Unknown'
    try:
        all_data['birth_place'] = \
            [x.find_all('a')[-1].text for x in html_soup.find_all('div', class_='txt-block') if
             x['id'] == 'name-born-info'][0]
    except:
        all_data['birth_place'] = 'Unknown'

    all_data['movies'] = [[z.a.text, 'https://imdb.com/' + z.a['href'].split('?')[0]] for z in
                          [y for y in html_soup.find_all('div', class_='filmo-category-section') if
                           y.div['id'].startswith('actor') or y.div['id'].startswith('actress')][0].find_all('div') if z.a is not None]
    adding_actor(all_data)





def adding_actor(data):
    database = Actor()
    database.name = data['name']
    database.logo = data['logo']
    database.imdb_link = data['imdb_link']
    database.date_of_birth = data['dob']
    database.profession = data['profession']
    database.birth_place = data['birth_place']
    database.movies = '|'.join([x[0] for x in data['movies']])
    database.movie_links = '|'.join([x[1] for x in data['movies']])
    database.save()
    print(database.name)

# temp = "{'Craig T. Nelson': 'https://imdb.com/name/nm0005266/?ref_=adv_li_st_0', 'Holly Hunter': 'https://imdb.com/name/nm0000456/?ref_=adv_li_st_1', 'Sarah Vowell': 'https://imdb.com/name/nm1102970/?ref_=adv_li_st_2', 'Huck Milner': 'https://imdb.com/name/nm9133740/?ref_=adv_li_st_3'}"
# link_list = [x.split(':')[2].strip()[1:-1].split('?')[0][15:-1] for x in movie.cast[1:-1].split(',')]
# print(list)
