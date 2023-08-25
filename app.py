import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import chess.pgn
import chess.engine
from getGame import fetch_and_process_games
from getGame import fetch_and_json_games

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

@app.route('/get_pgn', methods=['GET'])
  
def get_pgn():
    # Fetch and process games data using the function from getGame.py
    lichess_pgn_text = fetch_and_json_games()
    print(lichess_pgn_text)
    
    
    return jsonify(objects=lichess_pgn_text), 200



@app.route('/get_games', methods=['GET'])

def get_games():

    user_id = int(request.args.get('user_id'))  # Get user_id from the query parameter

    # Connect to the SQLite database
    connection = sqlite3.connect('games.sqlite')
    cursor = connection.cursor()

    # Execute a SELECT statement to fetch data for the specified user_id
    cursor.execute('SELECT date, data FROM games WHERE user_id = ?', (user_id,))
    result = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Convert query results to a list of dictionaries
    data_list = [{'date': row[0], 'data': row[1]} for row in result]

    # Return the data as JSON to the frontend
    return jsonify(data_list)



@app.route('/init_games', methods=['GET'])
def init_games():
    # Fetch and process games data using the function from getGame.py
    sample_pgn = fetch_and_process_games()

    # Split the PGN string into individual PGNs
    lichess_pgns = sample_pgn.split('\n\n')


    # Initialize the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")

    # Create a StringIO stream to read the sample PGN data
    pgn_stream = io.StringIO(sample_pgn)

    games_data = []  # List to store game data

    # Read individual games from the sample PGN data
    game = chess.pgn.read_game(pgn_stream)
     
    print(game) 

    while game:
        game_data = []  # List to store move data for the current game

        board = game.board()  # Create a board from the initial position

        prev_evaluation = 0
        move_number = 1

        for move in game.mainline_moves():
            # Analyze the position
            
            info = engine.analyse(board, chess.engine.Limit(time=2.0))

            if move_number == 1:

              number_of_moves = sum(1 for _ in game.mainline_moves())

              print(number_of_moves)

              number_of_moves = number_of_moves // 2

              game_data.append(number_of_moves)

              #code stops here on first iteration

            if info["score"] is not None and info["score"].white() is not None:
                score_value = info["score"].white().score()
               
                if score_value is not None:
                    evaluation = score_value
                else:
                    evaluation = 0  # Set a default value or handle it according to your needs
            else:
                evaluation = 0  # Set a default value or handle it according to your needs
            print(move)
            print(type(game.mainline_moves()))

            eval_change = abs(evaluation - prev_evaluation)

            next_mistake = "true" if eval_change >= 100 else "false"

            pgn_move = board.san(move)

            print(pgn_move)

            move_data = {
                "move": pgn_move,
                "next_mistake": next_mistake,
                "game_length" : number_of_moves,
                "evaluation": evaluation,
            }
            game_data.append(move_data)

            # Apply the move to the board after transforming
            board.push(move)

            prev_evaluation = evaluation
            move_number += 1

        games_data.append(game_data)  # Store the move data for the current game

        # Read the next game
        game = chess.pgn.read_game(pgn_stream)

    engine.quit()  # Quit the Stockfish engine

    print(games_data)

    return jsonify(games_data)

if __name__ == '__main__':
    app.run(debug=True)
