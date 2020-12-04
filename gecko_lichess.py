import berserk
import game
import chess
# The following code has been adapted from cheran-senthil's SultanKhan2 chess engine to interface with the lichess API
# Gets account token and bot id
token = 'gkj6XyUvUSTPg4mJ'
bot_id = 'Gecko_Bot'
# opens sesion with lichess.orf
session = berserk.TokenSession(token)
lichess = berserk.Client(session)
g = None
is_white = True
tc = None
game_id = None
rv = False
# Loops while active
while True:
    # If disconnected, will try to reconnect
    try:
        # loops for challenges
        for event in lichess.bots.stream_incoming_events():
            print("Event Type: "+event['type'])
            if event['type'] == 'challenge':
                challenge = event['challenge']
                # Accepts challenges that are standard variant
                if challenge['variant']['key'] == 'standard':
                    game_id = challenge['id']
                    tc = challenge['timeControl']['limit'], challenge['timeControl']['increment']

                    lichess.bots.accept_challenge(game_id)
                    rv = False
                else:
                    continue
            else:
                game_id = event['game']['id']
                challenge = {'color': 'random'}
            # Loops through game
            for game_state in lichess.bots.stream_game_state(game_id):

                    if game_state['type'] == 'gameFull':
                        # If new game
                        if game_state['state']['moves'] == '':

                            g = game.game()
                            g.lichessPlay = True
                            g.time[0] = tc[0]
                            g.time[1] = tc[0]
                            g.increment = tc[1]
                            is_white = game_state['white']['id'].lower() == bot_id.lower()


                        if is_white:
                            # If need to reconnect
                            if rv:

                                g = game.game()
                                g.lichessPlay = True
                                g.increment = tc[1]
                                g.time[chess.WHITE] = game_state['state']['wtime']/1000
                                g.time[chess.BLACK] = game_state['state']['btime']/1000
                                g.board = chess.Board(fen=chess.STARTING_FEN)
                                for i in game_state['state']['moves'].split():
                                    g.board.push_uci(i)
                                rv = False

                            g.move(mover="bot")
                            lichess.bots.make_move(game_id, g.board.peek())
                    # In game
                    if game_state['type'] == 'gameState':
                        # If have to reconnect as black
                        if rv:


                            g = game.game()
                            g.lichessPlay = True
                            g.increment = tc[1]
                            g.time[chess.WHITE] = game_state['wtime']/1000
                            g.time[chess.BLACK] = game_state['btime']/1000
                            g.board = chess.Board(fen=chess.STARTING_FEN)
                            for i in game_state['moves'].split():
                                g.board.push_uci(i)
                            rv = False
                        moves = game_state['moves'].split(' ')
                        # On his turn
                        if len(moves) % 2 != is_white:
                            g.time[chess.WHITE] = game_state['wtime'].timestamp()

                            g.time[chess.BLACK] = game_state['btime'].timestamp()
                            print(g.time)


                            if len(moves) >=1:
                                g.move(move=moves[-1])
                            g.move(mover="bot")
                            # Make a move
                            lichess.bots.make_move(game_id, g.board.peek())
    # Will exit with keyboard interrupt
    except KeyboardInterrupt:
        break
    # Will not exit if something disconnected it.  Instead, reconnect
    except:
        print("REEVALUATE")
        rv = True
        if g is not None:
            print(g.board)


        continue
