from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from main_page.models import AllFilms,Genere
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from environs import Env

class Command(BaseCommand):
    def parse_links(self)->list:
        options = Options()
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service,options=options)
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://okko.tv/")
        driver.implicitly_wait(10)
        
        html = driver.page_source
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')        
        film_links: list[str] = []    
        film_blocks = soup.find_all('div', class_ = 'Oce5ukhe')
        for block in film_blocks:
            link_tag = block.find('a', attrs = {'test-id': 'search_collection_element'})
            if link_tag and 'href' in link_tag.attrs:
                full_link = "https://okko.tv" + link_tag['href']
                film_links.append(full_link)
        driver.quit()
        
        return film_links       
                    
    def fetch_film_deteils(self, film_urls):
        for film_url in film_urls:
            options = Options()
            options.add_argument("--ignore-ssl-errors=yes")
            options.add_argument("--ignore-certificate-errors")
            service = Service(executable_path=ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service,options=options)
            #driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(film_url)
            driver.implicitly_wait(10)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            title_tag = soup.find('div', {'test-id': 'content_title'})
            title = title_tag.text.strip() if title_tag else 'No title found'
            
            description_tag = soup.find('span', class_='gUTsHpWs')
            description = description_tag.text.strip() if description_tag else 'No description available'
            
            image_tag = soup.find('img', class_='UU6mICOo')
            image_url = image_tag.get('src') if image_tag else None
            
            video_tag = soup.find('video')
            video_url = video_tag.get('src') if video_tag else None
            
            genre, _ = Genere.objects.get_or_create(genere='Default Genre Name')
            driver.quit()
            print (title,description,image_url,video_url)
            film, created = AllFilms.objects.get_or_create(
                title=title,
                defaults={
                    'description': description,
                    'video': video_url,
                    'image': image_url,
                }
            )
            if created:
                film.genre.add(genre)
                film.save()
                print(f"Created new film: {title}")
            else:
                print(f"Film already exists: {title}")
    
    def get_movies(self,api_key):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ru-RU"
        response = requests.get(url)
        match response.status_code:
            case 200:
                return response.json()
            case _:
                return {}
    
    def get_genere_name_by_id(self, api_key) -> dict[int:str]:
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-EN"
        response = requests.get(url)
        match response.status_code:
            case 200:
                genere_data = response.json()
                genere_mapping = {genre['id']: str(genre['name']).lower() for genre in genere_data['genres']}
                return genere_mapping
            case _:
                return {}
    
    def use_api(self):
        env = Env()
        env.read_env()
        api_key = env('FILM_API_KEY')
        movies = self.get_movies(api_key)
        existing_genres = {genere.genere for genere in Genere.objects.all()}
        print(existing_genres)
        default_genere, created = Genere.objects.get_or_create(genere = "default")
        all_genres = self.get_genere_name_by_id(api_key)
        for movie in movies['results']:
            print("_________________________________",movie['id'])
            url = f'https://api.themoviedb.org/3/movie/{movie['id']}/videos?api_key={api_key}'
            response = requests.get(url)
            match response.status_code:
                case 200:
                    print(f"получен доступ к трейлеру{movie['id']}")
                    movies_videos = response.json()
                    trailer = None
                    for video in movies_videos['results']: 
                        if video['type'] == 'Trailer':
                            trailer = f"https://www.youtube.com/watch?v={video['key']}"
                            if trailer:
                                film, created = AllFilms.objects.get_or_create(
                                    title=movie['title'],
                                    defaults={
                                        'description': movie['overview'],
                                        'video': trailer,
                                        'image': f'https://image.tmdb.org/t/p/w200/{movie["poster_path"]}',
                                    }
                                )
                                genere_ids = movie['genre_ids']
                                if genere_ids:
                                    for genere_id in genere_ids:
                                        genre_name = all_genres[genere_id]
                                        if genre_name in existing_genres:
                                            genre = Genere.objects.get(genere = genre_name)
                                        else:
                                            genre = default_genere
                                        film.genre.add(genre)
                                        film.save()
                                else:
                                    film.genre.add(default_genere)
                                    film.save()
                            break
                        else:
                            continue
                case _:
                    print('нет доступа к сайту')
                                
                        
                    
    
    
                    
    def handle(self, *args, **kwargs):
        #film_urls = self.parse_links()
        #self.fetch_film_deteils(film_urls)        
        self.use_api()
    
    