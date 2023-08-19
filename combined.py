import io
import chess.pgn
import chess.engine
from getGame import fetch_and_process_games

# Sample PGN data
sample_pgn = fetch_and_process_games()

print(sample_pgn)

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
       
        # Analyze the position
        info = engine.analyse(board, chess.engine.Limit(time=2.0))
        
        evaluation = info["score"].white().score()
        eval_change = abs(evaluation - prev_evaluation)
        
        mistake = "true" if eval_change >= 100 else "false"
        
        move_data = {"move": move.uci(), "mistake": mistake}
        print(move_data)
        game_data.append(move_data)
        
        prev_evaluation = evaluation
        move_number += 1
    
    games_data.append(game_data)  # Store the move data for the current game

    # Read the next game
    game = chess.pgn.read_game(pgn_stream)

engine.quit()  # Quit the Stockfish engine

# Print the games_data
for idx, game_data in enumerate(games_data, start=1):
    print(f"Game {idx}:")
    for move_info in game_data:
        print(f"Move: {move_info['move']}, Mistake: {move_info['mistake']}")
    
