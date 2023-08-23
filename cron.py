import schedule
import time
import io
import chess.pgn
import chess.engine
import json
import sqlite3
from datetime import date
from getGame import fetch_and_process_games
from getGame import fetch_and_json_games




def job():
    print('Running the cron job...')

    conn = sqlite3.connect('games.sqlite')
    cursor = conn.cursor()
    # Run your code here
    # Fetch and process games data using the function from getGame.py
    sample_pgn = fetch_and_process_games()

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

    user_id = 123  # Replace with the actual user ID
    desired_date = '2023-08-23'  # Replace with the desired date in 'YYYY-MM-DD' format

    for game in games_data:
       new_data_json = json.dumps(game)
       cursor.execute('INSERT OR REPLACE INTO games (user_id, date, data) VALUES (?, ?, ?)', (user_id, desired_date, new_data_json))

    conn.commit()
    conn.close()           


# Schedule the job to run every 5 minutes
schedule.every(5).minutes.do(job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
