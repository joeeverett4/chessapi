import chess
import chess.engine
import chess.pgn

# Initialize the Stockfish engine
with chess.engine.SimpleEngine.popen_uci("stockfish") as engine:
    # Load the PGN file
    pgn_file = open("game.pgn")
    game = chess.pgn.read_game(pgn_file)

    # Create a board from the initial position
    board = chess.Board()

    # Initialize variables to track the previous evaluation and move number
    prev_evaluation = 0
    move_number = 1

    # Iterate through the moves and analyze positions
    node = game
    while node is not None:
        if node.move is not None:
            # Apply the move to the board
            board.push(node.move)

            # Analyze the position
            info = engine.analyse(board, chess.engine.Limit(time=2.0))

            # Get the evaluation from the white point of view
            evaluation = info["score"].white().score()

            # Calculate the absolute difference from the previous evaluation
            eval_change = abs(evaluation - prev_evaluation)

            if eval_change >= 100:  # Check if the evaluation has changed by a pawn or more
                print(f"Position has swung by a pawn or more after move {node.move}")

            print(f"Move {move_number}: {node.move}")
            print(f"Evaluation: {evaluation / 100.0:.2f} pawns")

            # Update the previous evaluation
            prev_evaluation = evaluation

        # Move to the next node
        node = node.next()
        move_number += 1





