import chess
import chess.pgn

# Create a new chess game
game = chess.pgn.Game()

# Set up the initial position
board = game.board()

# Add SAN moves to the game
san_moves = ["e2e4", "e7e5", "g1f3"]
for san_move in san_moves:
    move = chess.Move.from_uci(chess.Move.from_uci(san_move).uci())
    print(move)

