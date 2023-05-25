from app import theme
from app.theme.get_radom_theme import get_random_theme

for x in range(10000):
    print(get_random_theme())
