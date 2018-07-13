from requests import get
from bs4 import BeautifulSoup
from home.models import Movie


def scrap_data(year, i):
    raw_url = "https://www.imdb.com/search/title?title_type=feature&release_date={}&count=200&sort=num_votes," \
              "desc&page=1 "
    url = raw_url.format(str(year))
    html_data = get(url, headers={"Accept-Language": "en-US, en;q=0.5"})
    html_soup = BeautifulSoup(html_data.text, 'html.parser')
    movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

    for movie in movie_containers:
        data = imdb_scrap(movie)
        base = Movie()
        base.logo = data['logo']
        base.title = data['title']
        base.imdb_link = data['imdb_link']
        base.year = data['year']
        base.certificate = data['certificate']
        base.runtime = data['runtime']
        base.genre = data['genre']
        base.imdb_rating = data['imdb_rating']
        base.metascore = data['metascore']
        base.director = data['director']
        base.cast = str(data['cast'])
        base.gross = data['gross']
        base.save()
        i += 1
        print(year, '-', i)
    return i


def imdb_scrap(first_movie):
    movie_data = {}

    movie_data['logo'] = first_movie.find('div', class_="lister-item-image float-left").a.img['loadlate']
    movie_data['title'] = first_movie.h3.a.text
    movie_data['imdb_link'] = 'https://imdb.com' + first_movie.h3.a['href']
    movie_data['year'] = first_movie.h3.find('span', class_='lister-item-year text-muted unbold').text[-5:-1]
    if first_movie.find('div', class_='lister-item-content').p.find('span', class_='certificate') is not None:
        movie_data['certificate'] = first_movie.find('div', class_='lister-item-content').p.find('span',
                                                                                                 class_='certificate').text
    else:
        movie_data['certificate'] = 'None'
    if first_movie.find('div', class_='lister-item-content').p.find('span', class_='runtime') is not None:
        movie_data['runtime'] = first_movie.find('div', class_='lister-item-content').p.find('span',
                                                                                             class_='runtime').text
    else:
        movie_data['runtime'] = 'None'
    if first_movie.find('div', class_='lister-item-content').p.find('span', class_='genre') is not None:
        movie_data['genre'] = first_movie.find('div', class_='lister-item-content').p.find('span',
                                                                                           class_='genre').text.strip()
    else:
        movie_data['genre'] = 'None'
    if first_movie.strong is not None:
        movie_data['imdb_rating'] = first_movie.strong.text
    else:
        movie_data['imdb_rating'] = 'None'
    if first_movie.find('div', class_='inline-block ratings-metascore') is not None:
        movie_data['metascore'] = first_movie.find('div', class_='inline-block ratings-metascore').span.text
    else:
        movie_data['metascore'] = 'None'

    temp_list = first_movie.find('div', class_='lister-item-content').find_all('p', class_="")[1].find_all('a')
    director = ''
    while True:
        if "ref_=adv_li_dr_" in temp_list[0]['href']:
            director += temp_list[0].text + ', ' + "https://imdb.com" + temp_list[0]['href'] + ', '
            temp_list.pop(0)
        else:
            break
    movie_data['director'] = director
    cast = {}

    for each in temp_list:
        url = "https://imdb.com" + each['href']
        cast[each.text] = url

    movie_data['cast'] = cast
    movie_data['gross'] = \
        first_movie.find('div', class_='lister-item-content').find('p', class_='sort-num_votes-visible').find_all(
            'span')[-1].text

    return movie_data

#
# i = 0
# for year in range(2005, 2018):
#     i = scrap_data(year, i)
#     print('\n\n')
