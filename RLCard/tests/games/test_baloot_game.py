'''
    File name: test_baloot_game.py
    Author: William Hale
    Date created: 11/25/2021
'''

import unittest
import numpy as np

from rlcard.games.baloot.game import BalootGame as Game
from rlcard.games.baloot.dealer import BalootDealer
from rlcard.games.baloot.player import BalootPlayer
from rlcard.games.baloot.utils.action_event import PassAction
from rlcard.games.baloot.utils.baloot_card import BalootCard
from rlcard.games.baloot.utils.move import DealHandMove


class TestBalootGame(unittest.TestCase):

    def test_get_num_players(self):
        game = Game()
        num_players = game.get_num_players()
        self.assertEqual(num_players, 4)

    def test_get_num_actions(self):
        game = Game()
        num_actions = game.get_num_actions()
        self.assertEqual(num_actions, 71)

    def test_baloot_dealer(self):
        dealer = BalootDealer(np.random.RandomState())
        current_deck = BalootCard.get_deck()
        deck_card_ids = [card.card_id for card in current_deck]
        self.assertEqual(deck_card_ids, list(range(32)))
        # Deal 8 cards.
        player = BalootPlayer(player_id=0, np_random=np.random.RandomState())
        dealer.deal_cards(player=player, num=8)
        self.assertEqual(len(dealer.shuffled_deck), 32)
        self.assertEqual(len(dealer.stock_pile), 24)
        self.assertEqual(len(current_deck), 32)
        self.assertEqual(len(BalootCard.get_deck()), 32)
        # Pop top_card from current_deck.
        top_card = current_deck.pop(-1)
        self.assertEqual(str(top_card), "AS")
        self.assertEqual(len(current_deck), 31)
        self.assertEqual(len(BalootCard.get_deck()), 32)

    def test_init_game(self):
        player_ids = list(range(4))
        game = Game()
        state, current_player = game.init_game()
        self.assertEqual(len(game.round.move_sheet), 1)
        self.assertIn(current_player, player_ids)
        self.assertEqual(len(game.actions), 0)
        self.assertEqual(len(game.round.players[current_player].hand), 8)  # current_player has 8 cards
        self.assertEqual(len(game.round.dealer.shuffled_deck), 32)
        self.assertEqual(len(game.round.dealer.stock_pile), 0)
        self.assertEqual(state['player_id'], current_player)
        self.assertEqual(len(state['hand']), 8)

    def test_step(self):
        game = Game()
        _, current_player_id = game.init_game()
        legal_actions = game.judger.get_legal_actions()
        action = np.random.choice(legal_actions)
        print(f'test_step current_player_id={current_player_id} action={action} legal_actions={[str(action) for action in legal_actions]}')
        _, next_player_id = game.step(action)
        next_legal_actions = game.judger.get_legal_actions()
        print(f'test_step next_player_id={next_player_id} next_legal_actions={[str(action) for action in next_legal_actions]}')

    def test_first_legal_bids(self):
        game = Game()
        _, current_player_id = game.init_game()
        for _ in range(3):
            legal_actions = game.judger.get_legal_actions()
            self.assertEqual(len(legal_actions), 36)
            action = PassAction()
            self.assertTrue(action in legal_actions)
            _, next_player_id = game.step(action)
        legal_actions = game.judger.get_legal_actions()
        self.assertEqual(len(legal_actions), 36)
        self.assertTrue(PassAction() in legal_actions)

    def test_pass_out_hand(self):
        game = Game()
        _, current_player_id = game.init_game()
        for _ in range(4):
            legal_actions = game.judger.get_legal_actions()
            action = PassAction()
            self.assertTrue(action in legal_actions)
            _, next_player_id = game.step(action)
        self.assertTrue(not game.round.contract_bid_move)
        self.assertTrue(game.round.is_bidding_over())
        self.assertTrue(game.is_over())
        self.assertTrue(not game.round.get_declarer())
        self.assertTrue(not game.round.get_dummy())
        self.assertTrue(not game.round.get_left_defender())
        self.assertTrue(not game.round.get_right_defender())

    def test_play_game(self):
        game = Game()
        next_state, next_player_id = game.init_game()
        deal_hand_move = game.round.move_sheet[0]
        self.assertTrue(isinstance(deal_hand_move, DealHandMove))
        print(f'test_play_game {deal_hand_move}')
        while not game.is_over():
            current_player_id = game.round.current_player_id
            self.assertEqual(current_player_id, next_player_id)
            legal_actions = game.judger.get_legal_actions()
            action = np.random.choice(legal_actions)
            print(f'test_play_game {current_player_id} {action} from {[str(x) for x in legal_actions]}')
            next_state, next_player_id = game.step(action)
        for player_id in range(4):
            player = game.round.players[player_id]
            hand = player.hand
            self.assertTrue(not hand)

    def test_print_scene(self):
        game = Game()
        next_state, next_player_id = game.init_game()
        deal_hand_move = game.round.move_sheet[0]
        self.assertTrue(isinstance(deal_hand_move, DealHandMove))
        while not game.is_over():
            current_player_id = game.round.current_player_id
            self.assertEqual(current_player_id, next_player_id)
            legal_actions = game.judger.get_legal_actions()
            action = np.random.choice(legal_actions)
            game.round.print_scene()
            next_state, next_player_id = game.step(action)
        game.round.print_scene()
        for player_id in range(4):
            player = game.round.players[player_id]
            hand = player.hand
            self.assertTrue(not hand)


if __name__ == '__main__':
    unittest.main()
