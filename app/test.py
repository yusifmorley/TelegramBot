from app import theme_file
from app.theme_file.get_radom_link import get_random_theme

for x in range(100):

    print("http" in get_random_theme() )
