from django.test import TestCase

from django.contrib.auth.models import User
from ..models import PlayingCard, Game, Player, Trick
from ..utils import Card, GameConfig

class TestCreateJassGame(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='user1')
        self.user_2 = User.objects.create_user(username='user2')
        self.user_3 = User.objects.create_user(username='user3')
        self.user_4 = User.objects.create_user(username='user4')

        self.users = [self.user_1, self.user_2, self.user_3, self.user_4]

        self.game = Game(name="klabberjass")
        self.game.save()
        self.game._set_players(self.users)

    def tearDown(self):
        # Clean up after each test
        self.user_1.delete()
        self.user_2.delete()
        self.user_3.delete()
        self.user_4.delete()

    def test_assign_players(self):
        """
        Test PlayingCard Model
        """
        game =self.game
        players = list(Player.objects.filter(game=game).order_by('position'))
        self.assertIs(len(set(players)), 4)
        self.assertEqual(players, game.get_players())

        player_users = [player.user for player in players]
        self.assertEqual(self.users, player_users)

        player_positions = [player.position for player in players]
        self.assertEqual(player_positions, [1,2,3,4])

        with self.assertRaises(Exception):
            """Klabberjass game should only have 4 players"""
            game._set_players([self.user_1, self.user_2, self.user_3])


    def test_create_playing_card(self):
        """
        Test PlayingCard Model
        """
        game = self.game
        card = Card(number="five", suit="club")

        player = Player.objects.create(user=self.user_1, game = game, position=1)

        playing_card = PlayingCard.objects.create(player=player, game = game, card=card)

        self.assertEqual(playing_card.card.number, "five")
        self.assertEqual(playing_card.card.suit, "club")

        card_from_db =  PlayingCard.objects.get(id= playing_card.id).card

        self.assertTrue(isinstance(card_from_db, Card))


    def test_deal_cards(self):
        """
        Test PlayingCard Model
        """
        config = GameConfig("klabberjass")
        game = self.game
        game._deal()

        # Check that all cards are present
        cards = []
        players = game.get_players()
        for player in players:
            hand = player.get_hand()
            self.assertEqual(len(set(hand)), config.num_tricks)
            cards.extend(hand)
        self.assertEqual(len(set(cards)), len(config.deck.cards))
        self.assertEqual(set([card.card.as_number() for card in cards]), set(card.as_number() for card in config.deck.cards) )

        # Check one cards:
        playing_card = cards[0]
        self.assertEqual(playing_card.played, False)
        self.assertEqual(playing_card.game, game)
        self.assertEqual(type(playing_card.card), type(Card(number="five", suit="club")))

        # Check that tricks have been created
        tricks = list(Trick.objects.filter(game=game).order_by('number'))
        self.assertEqual(tricks, game.get_tricks())
        self.assertEqual(len(tricks), config.num_tricks)
        self.assertEqual(set([trick.number for trick in tricks]), set(list(range(1,config.num_tricks+1))))

        #Card and trick together
        self.assertTrue(playing_card._validate_game(tricks[0]))
        self.assertTrue(playing_card._not_played())

    def test_play_cards(self):
        """
        Test that validations work when playing cards in and out of order.
        """
        game = self.game
        game._deal()
        players = game.get_players()
        player1 = players[0]
        player2 = players[1]
        player4 = players[3]

        # First player has the lead
        first_trick = game.get_current_trick()
        self.assertTrue(first_trick.number == 1)
        self.assertTrue(first_trick.lead() == player1)
        self.assertTrue(first_trick.to_play() == player1)

        # Player2 playing out of turn
        playing_card2 = player2.get_hand()[0]
        valid, message = playing_card2.play(first_trick)
        self.assertFalse(valid)
        self.assertTrue(message == "Invalid Play: Card played in incorrect order")

        # Player 1 plays first card
        playing_card1 = player1.get_hand()[0]
        valid, message = playing_card1.play(first_trick)
        self.assertTrue(valid)
        self.assertTrue(first_trick.to_play() == player2)
        self.assertTrue(playing_card1.order_in_trick == 1)

        # Player 1 attempts to play first card again:
        valid, message = playing_card1.play(first_trick)
        self.assertFalse(valid)
        self.assertTrue(message == "Invalid Play: Card has already been played")

        # Closing the trick by setting the winner
        first_trick.winner = player4
        first_trick.save()
        second_trick = game.get_current_trick()
        self.assertTrue(second_trick.number == 2)
        self.assertTrue(second_trick.lead() == player4)
        self.assertTrue(second_trick.to_play() == player4)

        # Player 4 plays card in second trick - first player plays next
        playing_card4 = player4.get_hand()[0]
        valid, message = playing_card4.play(second_trick)
        self.assertTrue(valid)
        self.assertTrue(second_trick.to_play() == player1)

        # Playing card from incorrect game.
        game2 = Game(name="klabberjass")
        game2.save()
        game2._set_players(self.users)
        game2._deal()
        player1 = game2.get_players()[0]
        wrong_card = player1.get_hand()[0]
        valid, message = wrong_card.play(second_trick)
        self.assertFalse(valid)
        self.assertTrue(message == "Invalid Play: Card belongs to incorrect game")



