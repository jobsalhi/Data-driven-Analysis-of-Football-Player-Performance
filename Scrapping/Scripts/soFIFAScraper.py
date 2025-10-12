import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response

def parse_players(html):
    soup = BeautifulSoup(html, 'html.parser')
    players = []
    # Example: Find all player rows in a table
    for row in soup.select('table.players-table tr'):
        name_cell = row.find('td', class_='player-name')
        if name_cell:
            name = name_cell.get_text(strip=True)
            players.append(name)
    return players

def main():
    url = 'https://sofifa.com/'
    html = fetch_page(url)
    # players = parse_players(html)
    # for player in players:
    #     print(player)
    print(html)

if __name__ == '__main__':
    main()
