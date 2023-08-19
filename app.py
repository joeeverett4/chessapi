import imp
from flask import Flask, jsonify
from flask_cors import CORS
import io
import chess.pgn
import chess.engine
from getGame import fetch_and_process_games

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

@app.route('/get_games', methods=['GET'])
def get_games():
    # Fetch and process games data using the function from getGame.py
    sample_pgn = fetch_and_process_games()

    # Initialize the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")

    # Create a StringIO stream to read the sample PGN data
    pgn_stream = io.StringIO(sample_pgn)

    games_data = []  # List to store game data

    # Read individual games from the sample PGN data
    game = chess.pgn.read_game(pgn_stream)
    while game:
        game_data = []  # List to store move data for the current game

        board = game.board()  # Create a board from the initial position

        prev_evaluation = 0
        move_number = 1

        for move in game.mainline_moves():
            # Analyze the position
            info = engine.analyse(board, chess.engine.Limit(time=2.0))

            if info["score"] is not None and info["score"].white() is not None:
             score_value = info["score"].white().score()

             if score_value is not None:
              evaluation = score_value
             else:
              evaluation = 0  # Set a default value or handle it according to your needs
            else:
             evaluation = 0  # Set a default value or handle it according to your needs


            print(move)
            print(evaluation)
            print(type(evaluation))
            eval_change = abs(evaluation - prev_evaluation)

            mistake = "true" if eval_change >= 100 else "false"

            # Transform SAN to PGN here
            san_move = move.uci()
            pgn_move = board.san(move)

            move_data = {"move": pgn_move, "mistake": mistake}
            game_data.append(move_data)

            # Apply the move to the board after transforming
            board.push(move)

            prev_evaluation = evaluation
            move_number += 1

        games_data.append(game_data)  # Store the move data for the current game

        # Read the next game
        game = chess.pgn.read_game(pgn_stream)

    engine.quit()  # Quit the Stockfish engine

    return jsonify(games_data)

if __name__ == '__main__':
    app.run(debug=True)
