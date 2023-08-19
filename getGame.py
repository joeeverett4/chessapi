import requests
import io
import chess.pgn


def fetch_and_process_games():

# URL of the API endpoint
  url = "https://lichess.org/api/games/user/Calgarysnow?max=2"

# Send a GET request
  response = requests.get(url)

# Check if the request was successful (status code 200)

  if response.status_code == 200:
    concatenated_pgns = response.text
    return concatenated_pgns
    
  else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
