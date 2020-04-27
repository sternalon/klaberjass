from django.test import TestCase

from django.contrib.auth.models import User
from ..models import PlayingCard, Game, Player
from ..utils import Card, GameConfig

class TestCreateJassGame(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='user1')
        self.user_2 = User.objects.create_user(username='user2')
        self.user_3 = User.objects.create_user(username='user3')
        self.user_4 = User.objects.create_user(username='user4')

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
        users = [self.user_1, self.user_2, self.user_3, self.user_4]

        game = Game(name = "klabberjass")
        game.save()
        game._set_players(users)

        players = [player for player in Player.objects.filter(game=game).order_by('position')]
        self.assertIs(len(set(players)), 4)
        self.assertEqual(players, game.get_players())

        player_users = [player.user for player in players]
        self.assertEqual(users, player_users)

        player_positions = [player.position for player in players]
        self.assertEqual(player_positions, [1,2,3,4])

        with self.assertRaises(Exception):
            """Klabberjass game should only have 4 players"""
            game._set_players([self.user_1, self.user_2, self.user_3])


    def test_create_playing_card(self):
        """
        Test PlayingCard Model
        """
        game = Game(name = "klabberjass")
        game.save()
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
        users = [self.user_1, self.user_2, self.user_3, self.user_4]

        game = Game(name = "klabberjass")
        game.save()
        game._set_players(users)
        game._deal()

        # Check that all cards are present
        cards = []
        players = game.get_players()
        for player in players:
            hand = player.get_hand()
            self.assertEqual(len(set(hand)), 8)
            cards.extend(hand)
        self.assertEqual(len(set(cards)), 32)
        self.assertEqual(set([card.card.as_number() for card in cards]), set(card.as_number() for card in GameConfig(game.name).deck.cards) )

        # Check one cards:
        playing_card = cards[0]
        self.assertEqual(playing_card.played, False)
        self.assertEqual(playing_card.game, game)
        self.assertEqual(type(playing_card.card), type(Card(number="five", suit="club")))
