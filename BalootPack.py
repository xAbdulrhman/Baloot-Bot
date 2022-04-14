from Pack import Pack
from Data import NumberRange,SuitRange,TableRange,PlayerRange,PlayerDict,TableDict,TeamDict
from Card import Card
import random
from BalootException import BalootException

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
                print("Game type is Hokom")
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