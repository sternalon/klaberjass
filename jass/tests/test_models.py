from django.test import TestCase

from django.contrib.auth.models import User
from ..models import PlayingCard, Game, Player, Trick, Series
from ..utils import Card, GameConfig

class TestCreateJassGame(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='user1')
        self.user_2 = User.objects.create_user(username='user2')
        self.user_3 = User.objects.create_user(username='user3')
        self.user_4 = User.objects.create_user(username='user4')

        self.users = [self.user_1, self.user_2, self.user_3, self.user_4]

        self.game = Game(game_type="klabberjass")
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

        player, created = Player.objects.get_or_create(user=self.user_1, game = game, position=1)

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

        # Set winner of second trick
        second_trick.set_winner()
        self.assertTrue(second_trick.winner == player4)

        # Playing card from incorrect game.
        game2 = Game(game_type="klabberjass")
        game2.save()
        game2._set_players(self.users)
        game2._deal()
        player1 = game2.get_players()[0]
        wrong_card = player1.get_hand()[0]
        valid, message = wrong_card.play(second_trick)
        self.assertFalse(valid)
        self.assertTrue(message == "Invalid Play: Card belongs to incorrect game")

class TestCreateJassSeries(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='user1')
        self.user_2 = User.objects.create_user(username='user2')
        self.user_3 = User.objects.create_user(username='user3')
        self.user_4 = User.objects.create_user(username='user4')

        self.series1 = Series.objects.create()
        self.series2 = Series.objects.create()
        self.series3 = Series.objects.create()


    def tearDown(self):
        # Clean up after each test
        self.user_1.delete()
        self.user_2.delete()
        self.user_3.delete()
        self.user_4.delete()

    def test_assign_players(self):
        """
        Adding players to Series
        """
        self.series1.add_player(self.user_1, position=1)

        # The following players can not be added to the series
        with self.assertRaises(Exception):
            """Only one player allowed per position"""
            self.series1.add_player(self.user_2, position=1)
        with self.assertRaises(Exception):
            """Player only allowed to play in one position per series"""
            self.series1.add_player(self.user_1, position=2)
        with self.assertRaises(Exception):
            """Position greater than number of players in the game"""
            self.series1.add_player(self.user_2, position=5)

        self.series2.add_player(self.user_1, position=2)

        self.series1.add_player(self.user_2, position=2)
        self.series3.add_player(self.user_2, position=3)

        user1_series = Series.get_series_for_player(self.user_1)
        self.assertEqual(set(user1_series), set([self.series1, self.series2]))
        self.assertEqual(self.series1.get_users_in_series(),[self.user_1, self.user_2])


        user2_series = Series.get_series_for_player(self.user_2)
        self.assertEqual(set(user2_series), set([self.series1, self.series3]))

        self.assertTrue(self.series1.player_in_series(self.user_1))
        self.assertFalse(self.series2.player_in_series(self.user_2))

    def test_create_game_from_series(self):
        """
        Creating a game from an existing series
        """
        series = self.series1
        series.add_player(self.user_1, position=1)
        series.add_player(self.user_2, position=2)
        series.add_player(self.user_3, position=3)
        series.add_player(self.user_4, position=4)

        current_game = series.get_current_game()
        self.assertEqual(current_game, None)

        Game.create_game_from_series(series.id)
        game = Game.objects.get(series=series)

        self.assertEqual(game.series, series)
        self.assertEqual(game.game_type, series.game_type)
        self.assertEqual(game.number, 1)

        response = Game.create_game_from_series(series.id)
        self.assertEqual(response,  "Series game in progress")

        game.completed = True
        game.save()

        Game.create_game_from_series(series.id)
        game = Game.objects.get(series=series, number=2)
        self.assertEqual(game.number, 2)

        current_game = series.get_current_game()
        self.assertEqual(current_game, game)










