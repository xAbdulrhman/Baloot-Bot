# ** THIS IS THE MAIN FILE TO RUN **
# This Python file uses the following encoding: utf-8

from copy import deepcopy
from Data import PlayerRange, PlayerDict, TableRange
from datetime import datetime
import math
from BalootPack import BalootPack


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

                print('\n------------------------------------')
                print('\t     Round {}'.format(t+1))
                print('------------------------------------\n')

                # for each player. TODO: index which depends on DealingPlayer
                for j_ in range(TableRange.Max):

                    j = (BalootPackObject.FirstPlayer + j_) % PlayerRange.Max
                    PlayerPack = BalootPackObject.GetPlayerPack(j)
                    LegalPack = deepcopy(PlayerPack)
                    LegalPack.clear()                    

                    if HumanPlayer == j:
                        while True:

                            LegalIds = []
                            LegalIndex = 0
                            print("Table: >>>>>>>>>>>>>>>>\n")
                            print(BalootPackObject.GetTablePack())
                            print("Your hand:\n")
                            for index in range(len(PlayerPack)):
                                if BalootPackObject.CheckPlayerMove(j, index, CheckPlayerMoveVerbose=True):
                                    LegalPack.append(PlayerPack[index])
                                    print("{}: {}".format(index, LegalPack[LegalIndex]))
                                    LegalIds.append(index)
                                    LegalIndex = LegalIndex + 1

                            try:
                                # print(LegalIds) #for condition testing purposes
                                PlayerPackIndex = int(
                                    input('\nPick card index > '))
                                # checks card validity
                                if not PlayerPackIndex in LegalIds:
                                    print("\nIT WAS A MISINPUT!\nMISINPUT!\n>> Enter One of The Options Displayed\n")
                                else:
                                    if BalootPackObject.CheckPlayerMove(j, PlayerPackIndex, CheckPlayerMoveVerbose=True):
                                        BalootPackObject.ToTablePack(j, PlayerPackIndex)  # play it
                                    break
                            except:
                                print("\nIT WAS A MISINPUT!\nMISINPUT!\n>> Enter One of The Options Displayed\n")
                    else:
                        for PlayerPackIndex, card in enumerate(PlayerPack):
                            # first card that is valid
                            if BalootPackObject.CheckPlayerMove(j, PlayerPackIndex, CheckPlayerMoveVerbose=False):
                                BalootPackObject.ToTablePack(
                                    j, PlayerPackIndex)  # play it
                                break

                print("Last Trick: =======================")
                print(BalootPackObject.GetTablePack())
                input('<<<PAUSE>>> Press Enter to continue\n')

                WinningTablePackIndex = BalootPackObject.GetWinningTablePackIndex()
                WinningPlayer = (BalootPackObject.FirstPlayer +
                                 WinningTablePackIndex) % PlayerRange.Max
                print('WinningPlayer:', PlayerDict[WinningPlayer])
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

            Dealer = (Dealer + 1) % 4   # changing dealer each round


StartTime = datetime.now()
BalootObject = Baloot()
print("Elapsed time: {} minutes".format(datetime.now() - StartTime))
