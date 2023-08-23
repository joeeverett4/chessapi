import chess.engine

# Create a Stockfish engine instance
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

# Generate a random FEN position (replace this with your FEN)
random_fen = "rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 4"

# Create a board from the random FEN
board = chess.Board(random_fen)

# Perform the analysis using the engine
info = engine.analyse(board, chess.engine.Limit(time=2.0), multipv=3)

# Print the analysis information
print("Analysis Result:")
for idx in range(len(info)):
    move_info = info[idx]
    moves = []
  

for move in move_info["pv"]:
    current_fen = board.fen()  # Get the current FEN after applying the move
    print("Current FEN:", current_fen)
    print(move)
    
    move_san = board.san(move)  # Convert UCI to SAN notation
    board.push(move)  # Apply the move to the board
    moves.append(move_san)  # Add the SAN notation move to the list 

   

   # for move_san in moves:
     # print(move_san)
    
    
  

    score = move_info["score"].relative.score()  # Get the score
    print(f"Move {idx + 1}: {' '.join(moves)} - Score: {score:.2f}")

# Close the enginec
engine.quit()


