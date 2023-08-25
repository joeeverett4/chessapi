import requests
import io
import chess.pgn
import json


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


def fetch_and_json_games():

    # URL of the API endpoint
    url = "https://lichess.org/api/games/user/Calgarysnow?max=2"

# Send a GET request
    response = requests.get(
        url,
        headers={"Accept": "application/x-ndjson"}
    )

    # Split the response text into separate JSON objects
    json_objects = response.text.split('\n')

    parsed_json_objects = []
    # Convert each JSON object to a dictionary and store in a list
    for json_obj in json_objects:
        if json_obj.strip():
            parsed_json = json.loads(json_obj)
            parsed_json_objects.append(parsed_json)

    # Print the parsed JSON objects
    for obj in parsed_json_objects:
        print("Parsed JSON Object:")
        print(obj)
        print("--------------------")

# Check if the request was successful (status code 200)

    if response.status_code == 200:
        print(response)
        # concatenated_pgns = response.body
        return parsed_json_objects

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
