from Data import NumberRange,SuitRange
from BalootException import BalootException
from Range import Range

class Card:
    StateList = [
        'UNDEALT',
        'YOU',
        'Bot-1',
        'Friend',
        'Bot-2',
        'Side0',
        'Side1',
        'Side2',
        'Side3',
        'SCORE1',
        'SCORE2',
    ]

    SuitDict = {
        0: 'SPADES   ',
        1: 'HEART    ',
        2: 'DIAMONDS ',
        3: 'CLUBS    ',
    }

    NumberDict = {
        0: '7',
        1: '8',
        2: '9',
        3: '10',
        4: 'J',
        5: 'Q',
        6: 'K',
        7: 'A',
    }

    NumberToValue = {
        '7': {'Suit': 0, 'Trump': 0},
        '8': {'Suit': 1, 'Trump': 1},
        '9': {'Suit': 2, 'Trump': 6},
        '10': {'Suit': 6, 'Trump': 4},
        'J': {'Suit': 3, 'Trump': 7},
        'Q': {'Suit': 4, 'Trump': 2},
        'K': {'Suit': 5, 'Trump': 3},
        'A': {'Suit': 7, 'Trump': 5},
    }

    NumberToPoints = {
        '7': {'Suit': 0, 'Trump': 0},
        '8': {'Suit': 0, 'Trump': 0},
        '9': {'Suit': 0, 'Trump': 14},
        '10': {'Suit': 10, 'Trump': 10},
        'J': {'Suit': 2, 'Trump': 20},
        'Q': {'Suit': 3, 'Trump': 3},
        'K': {'Suit': 4, 'Trump': 4},
        'A': {'Suit': 11, 'Trump': 11},
    }

    def __init__(self, Number=None, Suit=None, State='UNDEALT'):
        self.Number = None
        self.Suit = None
        self.State = None
        self.Value = None

        self.SetNumber(Number)
        self.SetSuit(Suit)
        self.SetState(State)

    def __repr__(self):
        return "Card(Suit = {!r}, Number = {!r}, State = {!r})".format(self.empty(), self.GetNumber(), self.GetState())

    def __str__(self):
        return '{}-{:>2} {!r}'.format(self.SuitDict[self.Suit], self.NumberDict[self.Number], self.State)

    def GetNumber(self):
        return self.Number

    def SetNumber(self, Number):
        BalootException._CheckParameterType(Number, int, 'Number')
        if Number < NumberRange.Min or Number >= NumberRange.Max:
            raise BalootException(
                'Valid values for Number parameter: 0-7. Number = {}'.format(Number))
        self.Number = Number

    def GetSuit(self):
        return self.Suit

    def SetSuit(self, Suit):
        BalootException._CheckParameterType(Suit, int, 'Suit')
        if Suit < SuitRange.Min or Suit >= SuitRange.Max:
            raise BalootException(
                'Valid values for Suit parameter: 0-4. Suit = {}'.format(Suit))
        self.Suit = Suit

    def GetState(self):
        return self.State

    def SetState(self, State):
        if State not in self.StateList:
            raise BalootException(
                'State {!r} is not a valid state. Valid States = {}'.format(State, self.StateList))
        self.State = State

    def GetValue(self, Trump=None):
        NumberString = self.NumberDict[self.GetNumber()]

        if self.GetSuit() == Trump:
            return self.NumberToValue[NumberString]['Trump']
        else:
            return self.NumberToValue[NumberString]['Suit']

    def GetPoints(self, Trump=None):
        NumberString = self.NumberDict[self.GetNumber()]

        if self.GetSuit() == Trump:
            return self.NumberToPoints[NumberString]['Trump']
        else:
            return self.NumberToPoints[NumberString]['Suit']
