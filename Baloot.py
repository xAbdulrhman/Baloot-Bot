# ** THIS IS THE MAIN FILE TO RUN **
# This Python file uses the following encoding: utf-8


from msilib.schema import SelfReg
import random
from datetime import datetime
import traceback
import math
from typing_extensions import Self
import numpy
from torch import randint


Verbose = False


class BalootException(Exception):
    pass


def _CheckParameterType(Parameter=None, Type=None, ParameterName=None):
    if not isinstance(Parameter, int):
        raise BalootException('{} parameter is expected to be of type int. {} = {}, type({}) = {}'.format(
            ParameterName, ParameterName, Parameter, ParameterName, type(Parameter)))


class Range(object):
    def __init__(self, RangeMin=None, RangeMax=None):
        self.Min = RangeMin
        self.Max = RangeMax


NumberRange = Range(0, 8)
SuitRange = Range(0, 4)
PlayerRange = Range(0, 4)
TableRange = Range(0, 4)
TeamRange = Range(0, 2)

PlayerDict = {
    0: 'YOU',
    1: 'Bot-1',
    2: 'Friend',
    3: 'Bot-2',
}

TableDict = {
    0: 'Side0',
    1: 'Side1',
    2: 'Side2',
    3: 'Side3',
}

TeamDict = {
    0: 'SCORE1',
    1: 'SCORE2',
}


class Card(object):
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
        _CheckParameterType(Number, int, 'Number')
        if Number < NumberRange.Min or Number >= NumberRange.Max:
            raise BalootException(
                'Valid values for Number parameter: 0-7. Number = {}'.format(Number))
        self.Number = Number

    def GetSuit(self):
        return self.Suit

    def SetSuit(self, Suit):
        _CheckParameterType(Suit, int, 'Suit')
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


class Pack(list):
    def __init__(self):
        list.__init__(self)

    def __repr__(self):
        ReprOut = ''
        for i, Card in enumerate(self):
            ReprOut += '{!r}: {!r}\n'.format(i, Card)
        return ReprOut

    def __str__(self):
        if self == []:
            return ''
        ReprOut = ''
        for i, Card in enumerate(self):
            ReprOut += '{!r:>01}: {!s}\n'.format(i, Card)
        return ReprOut


class BalootPack(Pack):
    def __init__(self):
        Pack.__init__(self)

        for Suit in range(SuitRange.Max):
            for Number in range(NumberRange.Max):
                CardObject = Card(Number=Number, Suit=Suit)
                self.append(CardObject)

        self.TableList = []
        self.Trump = None
        self.DealingPlayer = None
        self.FirstPlayer = None
        self.LastTrick = None

    def Shuffle(self):
        random.shuffle(self)

    def Deal(self, DealingPlayer=None):
        if DealingPlayer is None:
            raise BalootException('DealingPlayer parameter cannot be None')

        self.DealingPlayer = DealingPlayer
        self.FirstPlayer = (self.DealingPlayer + 1) % TableRange.Max

        i = 0

        while i < PlayerRange.Max*3:  # Deals first 3 cards
            for j_ in range(PlayerRange.Max):
                j = (DealingPlayer + j_ + 1) % PlayerRange.Max
                for u in range(3):
                    self[i+u].SetState(PlayerDict[j])
                    if self.DealingPlayer == 3 and j == 0:
                        print(self[i+u])
                else:
                    i += 3

        while i < PlayerRange.Max*3 + PlayerRange.Max*2:  # Deals second 2 cards
            for j_ in range(PlayerRange.Max):
                j = (DealingPlayer + j_ + 1) % PlayerRange.Max
                for u in range(2):
                    self[i+u].SetState(PlayerDict[j])
                    if j == 0 and self.DealingPlayer == 3:
                        print(self[i+u])
                else:
                    i += 2

        RandInt = random.randrange(0, PlayerRange.Max)
        self[PlayerRange.Max*3+PlayerRange.Max*2].SetState(PlayerDict[RandInt])

        self.Suit = self[0].GetSuit()
        self.Number = self[0].GetNumber()

# *******- Decide the game type -***********

        if self.DealingPlayer == 3:

            print('\n{} Take {} of {}'.format(PlayerDict[(
                self.DealingPlayer+1) % 4], Card.NumberDict[self.Number], Card.SuitDict[self.Suit]))

            GameType = input("Select game type Hokom or Sun (H/S)")

            if GameType == "H" or GameType == "h":

                self.Trump = self[0].GetSuit()
        else:
            print('\n{} Take {} of {}'.format(PlayerDict[(
                self.DealingPlayer+1) % 4], Card.NumberDict[self.Number], Card.SuitDict[self.Suit]))

            if RandInt >= 2:
                self.Trump = self[0].GetSuit()
                print("Game type is Hokom ")
            else:
                print("Game type is Sun")

        i = PlayerRange.Max*3+PlayerRange.Max*2+1
        while i < SuitRange.Max*NumberRange.Max:
            for j_ in range(PlayerRange.Max):
                j = (DealingPlayer + j_ + 1) % PlayerRange.Max
                for u in range(3):
                    if j != RandInt or u != 2:
                        self[i+u].SetState(PlayerDict[j])
                    else:
                        i += 2
                        break
                else:
                    i += 3

    def GetPlayerPack(self, Player=None):

        PlayerPack = Pack()
        for CardObject in self:
            if CardObject.GetState() == PlayerDict[Player]:
                PlayerPack.append(CardObject)
        return PlayerPack

    def GetTablePack(self):

        TablePack = Pack()

        for CardObject in self:
            if CardObject.GetState() == 'Side0':
                TablePack.append(CardObject)

        for CardObject in self:
            if CardObject.GetState() == 'Side1':
                TablePack.append(CardObject)

        for CardObject in self:
            if CardObject.GetState() == 'Side2':
                TablePack.append(CardObject)

        for CardObject in self:
            if CardObject.GetState() == 'Side3':
                TablePack.append(CardObject)

        return TablePack

    def ToTablePack(self, Player=None, PlayerPackIndex=None):

        TableListSize = len(self.TableList)

        PlayerPack = self.GetPlayerPack(Player)

        # check state of Players
        CurrentState = PlayerPack[PlayerPackIndex].GetState()
        for j in range(PlayerRange.Max):
            if CurrentState == PlayerDict[j]:
                break
        else:
            raise BalootException(
                'State {!r} is unexpected'.format(CurrentState))

        PlayerPack[PlayerPackIndex].SetState('Side{}'.format(TableListSize))
        self.TableList.append(None)

    def CheckPlayerMove(self, Player=None, PlayerPackIndex=None, CheckPlayerMoveVerbose=False):

        PlayerPack = self.GetPlayerPack(Player)

        CardToPlay = PlayerPack[PlayerPackIndex]

        TablePack = self.GetTablePack()

        # check playing move is allowed
        if TablePack != []:
            RequestedColor = TablePack[0].GetSuit()
            if CardToPlay.GetSuit() == RequestedColor:
                if RequestedColor == self.Trump:
                    WinningPlayedTrumpCard = self.GetWinningPlayedTrumpCard()
                    if CardToPlay.GetValue(Trump=self.Trump) < WinningPlayedTrumpCard.GetValue(Trump=self.Trump):
                        if self.TrumpHigher(Player=Player):
                            if CheckPlayerMoveVerbose:
                                print("You have to Trump higher")
                            return False
                        else:
                            if CheckPlayerMoveVerbose:
                                print("Player may play lower Trump")
                            return True
                    else:
                        if CheckPlayerMoveVerbose:
                            print("Player rises to Trump")
                        return True
                else:
                    if CheckPlayerMoveVerbose:
                        print("The player must play the requested suit")
                    return True
            else:
                HasRequestedColor = self.HasRequestedColor(
                    Player, RequestedColor)
                if HasRequestedColor:
                    if CheckPlayerMoveVerbose:
                        print('The player must play the requested suit')
                    return False
                else:
                    if CardToPlay.GetSuit() == self.Trump:
                        WinningPlayedTrumpCard = self.GetWinningPlayedTrumpCard()
                        if WinningPlayedTrumpCard != None:
                            if CardToPlay.GetValue(Trump=self.Trump) < WinningPlayedTrumpCard.GetValue(Trump=self.Trump):
                                if self.TrumpHigher(Player=Player):
                                    if CheckPlayerMoveVerbose:
                                        print(
                                            "When you cut you must Trump higher")
                                    return False
                                else:
                                    if CheckPlayerMoveVerbose:
                                        print(
                                            "The player plays lower Trump card")
                                    return True
                            else:
                                if CheckPlayerMoveVerbose:
                                    print("Player cuts and raises to Trump")
                                return True
                        else:
                            if CheckPlayerMoveVerbose:
                                print(
                                    "Player cuts (first Trump to fall in this trick)")
                            return True
                    else:
                        HasTrump = self.HasTrump(Player)
                        if HasTrump:
                            if CheckPlayerMoveVerbose:
                                # TODO: partenaire maitre
                                print("Player must cut if he has Trump cards")
                            return False
                        else:
                            if CheckPlayerMoveVerbose:
                                print("Player cannot cut (no Trump cards in hand)")
                            return True

        else:
            if CheckPlayerMoveVerbose:
                print('The winning player chooses a card')
            return True

    def GetScorePack(self, Team=None):

        ScorePack = Pack()

        for CardObject in self:
            if CardObject.GetState() == TeamDict[Team]:
                ScorePack.append(CardObject)

        return ScorePack

    def ToScorePack(self, Team=None):

        TablePack = self.GetTablePack()

        for i in range(len(TablePack)):
            # check state is Tablex
            CurrentState = TablePack[i].GetState()
            for e in range(TableRange.Max):
                if CurrentState == TableDict[e]:
                    break
            else:
                raise BalootException(
                    'State {!r} is unexpected'.format(CurrentState))

            TablePack[i].SetState(TeamDict[Team])

        self.TableList = []

    def HasRequestedColor(self, Player=None, RequestedColor=None):
        PlayerPack = self.GetPlayerPack(Player)

        for card in PlayerPack:
            if card.GetSuit() == RequestedColor:
                return True
        else:
            return False

    def HasTrump(self, Player=None):
        PlayerPack = self.GetPlayerPack(Player)

        for card in PlayerPack:
            if card.GetSuit() == self.Trump:
                return True
        else:
            return False

    def GetWinningPlayedTrumpCard(self):
        WinningPlayedTrumpCard = None
        TablePack = self.GetTablePack()
        for card in TablePack:
            if card.GetSuit() == self.Trump:
                if WinningPlayedTrumpCard == None or card.GetValue(Trump=self.Trump) > WinningPlayedTrumpCard.GetValue(Trump=self.Trump):
                    WinningPlayedTrumpCard = card
        return WinningPlayedTrumpCard

    def TrumpHigher(self, Player=None):
        PlayerPack = self.GetPlayerPack(Player)

        if not self.HasTrump(Player=Player):
            return False

        WinningPlayedTrumpCard = self.GetWinningPlayedTrumpCard()

        for card in PlayerPack:
            if card.GetSuit() != self.Trump:
                continue
            if card.GetValue(Trump=self.Trump) > WinningPlayedTrumpCard.GetValue(Trump=self.Trump):
                return True

    def GetWinningTablePackIndex(self):
        TablePack = self.GetTablePack()

        WinningTablePackIndex = 0
        MaxValue = TablePack[0].GetValue(Trump=self.Trump)
        FirstCardSuit = TablePack[0].GetSuit()
        bTrumpJoue = (FirstCardSuit == self.Trump)
        for TablePackIndex_, card in enumerate(TablePack[1:]):

            TablePackIndex = TablePackIndex_ + 1

            CardSuit = card.GetSuit()
            if bTrumpJoue:
                if CardSuit != self.Trump:
                    continue
                else:
                    CardValue = card.GetValue(Trump=self.Trump)
                    if CardValue > MaxValue:
                        MaxValue = CardValue
                        WinningTablePackIndex = TablePackIndex
            else:
                if CardSuit == self.Trump:
                    bTrumpJoue = True
                    CardValue = card.GetValue(Trump=self.Trump)
                    MaxValue = CardValue
                    WinningTablePackIndex = TablePackIndex
                else:
                    if CardSuit != FirstCardSuit:
                        continue
                    else:
                        CardValue = card.GetValue(Trump=self.Trump)
                        if CardValue > MaxValue:
                            MaxValue = CardValue
                            WinningTablePackIndex = TablePackIndex

        return WinningTablePackIndex

    def Player2Team(self, Player=None):
        if Player is None:
            raise BalootException('Player parameter cannot be None')

        if Player == 0 or Player == 2:
            return 0
        elif Player == 1 or Player == 3:
            return 1
        else:
            raise BalootException(
                'Player parameter must be 0-3. Player = {!r}'.format(Player))

    def GetScore(self, Team=None):
        ScorePack = self.GetScorePack(Team)

        Score = 0
        for card in ScorePack:
            CardValue = card.GetPoints(Trump=self.Trump)
            Score += CardValue

        # Last Trick
        if self.LastTrick == Team:
            Score += 10

        return Score


class Baloot(object):
    def __init__(self):

        HumanPlayer = 0
        rscoreT1 = 0
        rscoreT2 = 0
        TotalScore1 = 0
        TotalScore2 = 0

        def rscore(x):
            return int(x + math.copysign(0.5, x))

        Dealer = 3
        while TotalScore1 < 152 and TotalScore2 < 152:
            BalootPackObject = BalootPack()
            BalootPackObject.Shuffle()
            BalootPackObject.Deal(Dealer)

            for t in range(8):  # that many rounds

                if True:
                    print('------------------------------------')
                if True:
                    print('Round {}'.format(t+1))
                if True:
                    print('------------------------------------')

                # for each player. TODO: index which depends on DealingPlayer
                for j_ in range(TableRange.Max):

                    j = (BalootPackObject.FirstPlayer + j_) % PlayerRange.Max
                    PlayerPack = BalootPackObject.GetPlayerPack(j)

                    if HumanPlayer == j:
                        while True:
                            print("Table: >>>>>>>>>>>>>>>>")
                            print(BalootPackObject.GetTablePack())
                            print("Your hand:")
                            print(PlayerPack)
                            try:
                                PlayerPackIndex = int(
                                    input('Pick card index > '))
                                # checks card validity
                                if BalootPackObject.CheckPlayerMove(j, PlayerPackIndex, CheckPlayerMoveVerbose=True):
                                    BalootPackObject.ToTablePack(
                                        j, PlayerPackIndex)  # play it
                                    break
                            except:
                                traceback.print_exc()
                    else:
                        if Verbose:
                            print(PlayerDict[j])
                        if Verbose:
                            print(PlayerPack)
                        for PlayerPackIndex, card in enumerate(PlayerPack):
                            # first card that is valid
                            if BalootPackObject.CheckPlayerMove(j, PlayerPackIndex, CheckPlayerMoveVerbose=Verbose):
                                BalootPackObject.ToTablePack(
                                    j, PlayerPackIndex)  # play it
                                break

                print("Last Trick: =======================")
                print(BalootPackObject.GetTablePack())
                input('<<<PAUSE>>> Press Enter to continue\n')

                WinningTablePackIndex = BalootPackObject.GetWinningTablePackIndex()
                WinningPlayer = (BalootPackObject.FirstPlayer +
                                 WinningTablePackIndex) % PlayerRange.Max
                print('WinningPlayer:', PlayerDict[WinningPlayer]+"\n")
                BalootPackObject.ToScorePack(BalootPackObject.Player2Team(
                    WinningPlayer))  # puts played cards in the score pile

                # Last trick
                if t == 7:
                    BalootPackObject.LastTrick = BalootPackObject.Player2Team(
                        WinningPlayer)

                # update first player for next round
                BalootPackObject.FirstPlayer = WinningPlayer

            rscoreT1 = (BalootPackObject.GetScore(0))
            rscoreT2 = (BalootPackObject.GetScore(1))

            if BalootPackObject.Trump == None:
                rscoreT1 *= 2
                rscoreT2 *= 2

            print("Score1:", rscoreT1)
            print("Score2:", rscoreT2, "\n")
            rscoreT1 = rscore(rscoreT1/10)
            rscoreT2 = rscore(rscoreT2/10)
            TotalScore1 += rscoreT1
            TotalScore2 += rscoreT2

            print("Total Score Team 1: ", TotalScore1)
            print("total Score Team 2: ", TotalScore2, "\n")

            Dealer = (Dealer + 1) % 4


StartTime = datetime.now()
BalootObject = Baloot()
print("Elapsed time: {} minutes".format(datetime.now() - StartTime))
