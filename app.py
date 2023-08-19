from flask import Flask, jsonify
from flask_cors import CORS
import io
import chess.pgn
import chess.engine
from getGame import fetch_and_process_games

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def convert_san_to_pgn(san_moves):
    pgn_moves = []
    board = chess.Board()

    for san_move in san_moves:
        move = chess.Move.from_uci(san_move)
        pgn_moves.append(board.san(move))
        board.push(move)

    return pgn_moves

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
            # Apply the move to the board
            board.push(move)
            print(move)
            # Analyze the position
            info = engine.analyse(board, chess.engine.Limit(time=2.0))

            evaluation = info["score"].white().score()
            eval_change = abs(evaluation - prev_evaluation)

            mistake = "true" if eval_change >= 100 else "false"

            

            move_data = {"move": move.uci(), "mistake": mistake}
            game_data.append(move_data)

            prev_evaluation = evaluation
            move_number += 1

        san_moves = [move_data["move"] for move_data in game_data]
        pgn_moves = convert_san_to_pgn(san_moves)
        games_data.append(pgn_moves)  # Store the PGN moves for the current game

        # Read the next game
        game = chess.pgn.read_game(pgn_stream)

    engine.quit()  # Quit the Stockfish engine

    return jsonify(games_data)

if __name__ == '__main__':
    app.run(debug=True)
