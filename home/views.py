from django.shortcuts import render
from .models import Movie, Director, Actor
from django.shortcuts import get_object_or_404
from home.web_scaping.adding_director import director_data, actor_data
from django.core.mail import send_mail


def home(request):
    return render(request, 'home/homepage.html')


def index(request, page, size=50):
    t = round((Movie.objects.count()) / size)
    i = (page - 1) * size
    pre = page - 1
    j = 0
    movies = []
    titles = []
    for movie in Movie.objects.order_by('-year'):
        if j in range(i, page * size):
            movies.append(movie.imdb_link.split('?')[0][-10:-1])
            titles.append(movie.title)
        elif j > page * size:
            break
        j += 1
    total = []
    for ttl in range(1, t + 1):
        total.append(ttl)
    ind = []
    for j in range(size):
        ind.append(j)

    context = {'movies': movies, 'page': page, 'pre': pre, 'total': total, 'titles': titles, 'ind': ind}
    return render(request, 'home/index.html', context)


def detail(request, value):
    movie = get_object_or_404(Movie, imdb_link='https://imdb.com/title/' + value + '/?ref_=adv_li_tt')
    director = [x.strip() for x in movie.director.strip().split(',') if x.find('https://') == -1]
    director.pop()
    dir_link = [x.strip().split('?')[0][22:-1] for x in movie.director.split(',') if x.find('https://') != -1]
    count = [x for x in range(len(director))]
    cast = [x.split(':')[0].strip()[1:-1] for x in movie.cast[1: -1].split(',')]
    count1 = [x for x in range(len(cast))]
    cast_link = [x.split(':')[2][16:25] for x in movie.cast[1:-1].split(',')]
    context = {'movie': movie, 'director': director, 'cast': cast, "dir_link": dir_link, 'count': count,
               'cast_link': cast_link, 'count1': count1}
    return render(request, 'home/detail.html', context)


def dir_detail(request, link):
    director = get_object_or_404(Director, pk='https://www.imdb.com/name/' + link)
    if director.date_of_birth == 'Unknown':
        date_of_birth = None
    else:
        date_of_birth = director.date_of_birth
    movies = [movie.strip() for movie in director.movies.split('|')]
    movie_links = [x.imdb_link.split('?')[0][-10:-1] for x in Movie.objects.all()]
    dir_movie_links = [x[-10:-1] for x in director.movie_links.split('|')]

    i = [x for x in range(len(movies))]

    context = {'director': director, 'date_of_birth': date_of_birth, 'movies': movies, 'movie_links': movie_links,
               'dir_movie_links': dir_movie_links, 'i': i, }

    return render(request, 'home/director_detail.html', context)


def act_detail(request, link):
    actor = get_object_or_404(Actor, pk='https://www.imdb.com/name/' + link)
    if actor.date_of_birth == 'Unknown':
        date_of_birth = None
    else:
        date_of_birth = actor.date_of_birth
    movies = [movie.strip() for movie in actor.movies.split('|')]
    movie_links = [x.imdb_link.split('?')[0][-10:-1] for x in Movie.objects.all()]
    act_movie_links = [x[-10:-1] for x in actor.movie_links.split('|')]

    # for each in dir_movie_links:

    i = [x for x in range(len(movies))]

    context = {'director': actor, 'date_of_birth': date_of_birth, 'movies': movies, 'movie_links': movie_links,
               'dir_movie_links': act_movie_links, 'i': i, }

    return render(request, 'home/actor_detail.html', context)


def actor_detail0(link):
    try:
        actor_links = [x.imdb_link.split('?')[0][26:] for x in Actor.objects.all()]
        if link not in actor_links:
            actor_data('https://www.imdb.com/name/' + link)
        else:
            print('Already done--------------------------')
    except:
        print('Exception--------------------------------')
        pass

    # return render(request, 'home/director_detail.html')


# for movie in Movie.objects.order_by('-year'):
#     if movie.year <= '1997':
#         print('--', movie.title, movie.year, '--')
#         link_list = [x.split(':')[2].strip()[1:-1].split('?')[0][15:-1] for x in movie.cast[1:-1].split(',')]
#         for link in link_list:
#             actor_detail0(link)

def search(request):

    if request.GET['category'] == 'movie':
        movie_list = Movie.objects.filter(title__icontains=request.GET["search"])
        return render(request, 'home/search_result.html', {'list': movie_list})

    elif request.GET['category'] == 'director':
        director_list = Director.objects.filter(name__icontains=request.GET["search"])
        return render(request, 'home/search_result.html', {'list': director_list})

    elif request.GET['category'] == 'actor':
        actor_list = Actor.objects.filter(name__icontains=request.GET["search"])
        return render(request, 'home/search_result.html', {'list': actor_list})

    # print(request.POST("search"))
