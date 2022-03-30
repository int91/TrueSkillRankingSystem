from typing import List
import math
import statistics

#TODO: MOVE THE F*CKING CLASSES TO FILES YOU DIMWIT

#NOTE: GamesWon1 + GamesWon2 - GameLoss = elo (If all 3 games are played)

#NOTE: Once match ends. After result has been retrieved notify any @admin and tell them to give respective stats. (this is for the discord bot that will be made later on)

class User():
    def __init__(self, id: int, nme: str):
        #Discord Bot Vars
        self.uid: int = id
        self.name: str = nme

        #Total Stats
        self.gamesPlayed: int = 0
        self.kills: int = 0
        self.deaths: int = 0
        self.assists: int = 0
        self.objs: int = 0
        self.wins: int = 0
        self.loss: int = 0

        #Recent Match
        self.recentMatch: Match = Match()

class Player():
    def __init__(self, ks: int = 0, dt: int = 0, ass: int = 0, ob: int = 0,):
        #Player's discord user
        self.user: User = None

        #Player's stats for that game (NOT MATCH)
        self.kills: int = ks
        self.deaths: int = dt
        self.assists: int = ass
        self.objs: int = ob

#NOTE: Don't worry about this useless sh*t right here. does nothing atm
class Match():
    def __init__(self):
        #The matches id used for referencing
        self.id: int = 0
        
        #Users In Each Team
        self.team1: List[User] = []
        self.team2: List[User] = []

        #command would be ;givestats 1 uid/name kills, deaths, assists, objpoints/time
        #1 meaning game 1
        
        #Stats for each player & game within the best of 3
        #Each index is a list of that player's stats for index of game number
        self.gamesTeam1: List[List[Player]] = [] 
        self.gamesTeam2: List[List[Player]] = []

        #Matches won for each team
        #(If one team has 2 wins and the other has 0,
        # then that match didn't get played due to best of 3)
        self.team1Result: List[bool] = [False, False, None]
        self.team2Result: List[bool] = [False, False, None]
    
    def Print(self):
        print(self.team1)
        print(self.team2)
        print(self.gamesTeam1)
        print(self.gamesTeam2)
        print(self.team1Result)
        print(self.team2Result)
        
    def UserInMatch(self, id: int) -> bool:
        for i in self.team1:  
            if (i.uid == id): 
                return True
        for i in self.team2: 
            if (i.uid == id): 
                return True
        return False

    def GetPlayerById(self, id: int) -> Player:
        for i in self.team1:  
            if (i.uid == id): 
                return i
        for i in self.team2: 
            if (i.uid == id): 
                return i
        return None

    def GetMatchPlayerById(self, id: int) -> Player:
        for i in self.gamesTeam1:
            if (i[0].user.uid == id):
                return i
        for i in self.gamesTeam2:
            if (i[0].user.uid == id):
                return i
        return None
    
    def GetTeamById(self, id: int) -> int:
        for i in self.team1:
            if (i.uid == id):
                return 1
        for i in self.team2:
            if (i.uid == id):
                return 2
        return 0

    def GetTeamByPlayer(self, p: Player) -> int:
        for i in self.gamesTeam1:
            if (i[0] == p):
                return 1
        for i in self.gamesTeam2:
            if (i[0] == p):
                return 2
        return 0
    
    def GetPlayerList(self, p: Player) -> List[Player]:
        for i in self.gamesTeam1:
            if (i[0] == p):
                return i
        for i in self.gamesTeam2:
            if (i[0] == p):
                return i 
        return None

    def SetPlayerStats(self, id: int, kil: int, det: int, assis: int, obj: int):
        p: Player = self.GetPlayerById(id)
        if (p != None): 
            p.kills = kil
            p.deaths = det
            p.assists = assis
            p.objs = obj
        else:
            print("[ERROR] Player could not be found")
    
    def SetStats(self, id: int, game: int, gamemode: str, kills: int, deaths: int, assists: int, objs: int, result: bool = True):
        if (self.UserInMatch(id)):
            p: Player = Player()
            pList: List[Player] = self.GetPlayerList(p)
            team: int = self.GetTeamById(id)
            p.deaths = deaths
            p.objs = objs
            p.kills = kills
            p.assists = assists
            if (pList == None):
                pList = []
            pList.append(p)
            if (team == 1):
                self.team1Result[game-1] = result              
                self.gamesTeam1.append(pList)
            elif (team == 2):
                self.team1Result[game-1] = result
                self.gamesTeam2.append(pList)

#Place holder weights for ranking system
WIN_WEIGHT = 1.45
KILL_WEIGHT = 1.125
ASSIST_WEIGHT = 1.1
OBJ_WEIGHT = 1.8

POS_WEIGHT = 1.2 #POS_WEIGHT * LeaderboardPosition = outcome for this (This isn't used in the new Calculations but might be ater on)
RANKS = 5
RANK_WEIGHT = 0.4

LOSS_WEIGHT = 0.825
DEATH_WEIGHT = 1

END_RESULT_DIV = 24

def CalculatePlace(Player, Teammates):
    pass

class EloCalculator():
    def CalculateRelatives(self, p: Player, team: List[Player]) -> List[float]:
        results: List[float] = []
        
        relKills: float = 0
        relDeaths: float = 0
        relAssist: float = 0
        relObjs: float = 0
        
        totalKills: int = 0
        totalDeaths: int = 0
        totalAssists: int = 0
        totalObjs: int = 0
        
        killsArr: List[int] = []
        deathsArr: List[int] = []
        assistArr: List[int] = []
        objArr: List[int] = []
        
        if (p in team):
            team.remove(p)
        
        for e in team:
            killsArr.append(e.kills)
            deathsArr.append(e.deaths)
            assistArr.append(e.assists)
            objArr.append(e.objs)
            
            #totalKills += e.kills
            #totalDeaths += e.deaths
            #totalAssists += e.assists
            #totalObjs += e.objs
            
            #NOTE: This is a placeholder system for now
            #relKills += (p.kills-e.deaths)/e.deaths #relative deaths to this enemy
            #relDeaths += (e.deaths-p.deaths)/p.deaths #relative deaths to this enemy
            #if (e.assists != 0):
                #relAssist += (p.assists-e.assists)/e.assists #relative assists to this enemy
            #if (e.objs != 0):
                #relObjs += (p.objs-e.objs)/e.objs #relative objective points to this enemy

        totalKills = statistics.median(killsArr)
        totalDeaths = statistics.median(deathsArr)
        totalAssists = statistics.median(assistArr)
        totalObjs = statistics.median(objArr)

        relKills = (p.kills-totalKills)/totalKills
        relDeaths = (totalDeaths-p.deaths)/p.deaths
        relAssist = (p.assists-totalAssists)/totalAssists
        relObjs = (p.objs-totalObjs)/totalObjs
        
        #Gets average of relatives
        #teamSize = len(team)
        #relKills /= teamSize
        #relDeaths /= teamSize
        #relAssist /= teamSize
        #relObjs /= teamSize
        
        results = [relKills, relDeaths, relAssist, relObjs]
        print(results)
        return results
        
        
        
    #Adjust params to better fit the functions purpose
    def CalculateElo(self, p: Player, lPos: int, won: bool, rank: int = 1, Teammates=None) -> int:
        result: float = 0
        #Get the avg values of team stats
        #Get relative values of enemy stats
        
        #Calculate team first, then enemy team
        
        #TODO: Implement team calculations. Note: Use a new method - self.CalculateAverage and pass in the player and their team
        #Team averages excludes player
        #teamAvgKills: float = 3 #Avg kills of team
        #teamAvgDeaths: float = 5 #Avg deaths of team
        #teamAvgAssists: float = 10 #Avg assists of team
        #teamAvgObj: float = 3 #Avg objs of team
        
        #Test data set of 2 out of the 4 enemy players (stats taken from a Pro-League Search & Destroy match)
        e1 = Player(23, 19, 6, 60)
        e2 = Player(18, 21, 5, 54)
        e3 = Player(15, 22, 8, 90)
        e4 = Player(14, 21, 6, 54)
        e5 = Player(15, 21, 5, 47)
        
        f1 = Player(17, 16, 6, 17)
        f2 = Player(20, 16, 11, 15)
        f3 = Player(8, 20, 6, 66)
        f4 = Player(8, 16, 5, 28)
        
        enemyTeam: List[Player] = [e1, e2, e3, e4, e5]
        playersTeam: List[Player] = [f1, f2, f3, f4]
        #Getting average relatives of the player to the enemy team
        #TODO: Replace relative calc with avg calc then do relatives based on team and enemy after this Note: Use a new method - self.CalculateAverage and pass in the player and their team
        eTeamRels = self.CalculateRelatives(p, enemyTeam)
        pTeamRels = self.CalculateRelatives(p, playersTeam)
        
        #TODO: Convert Self.CalculateRelatives into a function that only does relative calculation for player & X user (I think)
        enemyRelKills: float = eTeamRels[0]
        enemyRelDeaths: float = eTeamRels[1]
        enemyRelAssists: float = eTeamRels[2]
        enemyRelObj: float = eTeamRels[3]
        
        playerRelKills: float = pTeamRels[0]
        playerRelKills: float = pTeamRels[1]
        playerRelKills: float = pTeamRels[2]
        playerRelKills: float = pTeamRels[3]
        
        relKills: float = 0
        relDeaths: float = 0
        relAssist: float = 0
        relObjs: float = 0
        #relatives here are percentages * 100 for more accuracy with weights
        
        #relKills = (p.kills-teamAvgKills)/teamAvgKills * 100 #relative kills
        #relDeaths = (teamAvgDeaths-p.deaths)/p.deaths * 100 #relative deaths
        #if (p.assists != 0):
        #   relAssist = (p.assists-teamAvgAssists)/teamAvgAssists * 100 #relative assists
        #relObjs = (p.objs-teamAvgObj)/teamAvgObj * 100 #relative objective points
        
        
        relKills += enemyRelKills * 100
        relDeaths += enemyRelDeaths * 100
        relAssist += enemyRelAssists * 100
        relObjs += enemyRelObj * 100
        
        relKills += playerRelKills * 100
        relDeaths += playerRelKills * 100
        relAssist += playerRelKills * 100
        relObjs += playerRelKills * 100
        
        #TODO: Remove this
        #print(relKills)
        #print(relDeaths)
        #print(relAssist)
        #print(relObjs)
        
        result += relKills * KILL_WEIGHT
        result += relAssist * ASSIST_WEIGHT
        result += relObjs * OBJ_WEIGHT
        print(result)
        result -= relDeaths * DEATH_WEIGHT
        print(result)
        
        #TODO: Remove this
        #result += p.kills * KILL_WEIGHT
        #result += p.assists * ASSIST_WEIGHT
        #result += p.objs * OBJ_WEIGHT
        #result += (lPos-4) * -POS_WEIGHT
        #result += p.deaths * -DEATH_WEIGHT
        
        #TODO: Add better win loss cases that better reflect the affect of each outcome
        if (won):
            result *= WIN_WEIGHT
        else:
            result *= LOSS_WEIGHT #Determine something for weighting losses
        
        if (rank >= 1):
            result *= (RANKS-rank)*RANK_WEIGHT
        
        return math.ceil(result/END_RESULT_DIV)

    #Seems fine for now but you get Diamond after winning ALL placements
    def LegacyEloCalculate(self, rank: int, result: bool, lPlace: int, winstreak: int = 0) -> int:
        elo: int = 0
        if (result):
            #If win, add result and then calculate bonus based on placement
            elo += 28
            if (lPlace <= 3):
                elo += int(4/lPlace)
                
            if (rank == 0 and winstreak != 0):
            #If unranked and on winstreak calculate bonus
                elo += -int(((rank-6) * 3 * (winstreak+1*1.5)))
            elif (winstreak == 0 and result):
            #If not unranked calculate sub based on rank out of max ranks
                elo += -int((rank-6) * 3)
                
        else:
            #If los, subtract result and then calculate -bonus based on placement
            elo -= 20
            if (lPlace > 1):
                elo -= math.ceil(lPlace/2) * 4
            
            if (rank == 0):
                #If unranked calculate lost elo
                elo += math.ceil(elo * 2.2) 
            elif (rank > 0):
                elo += math.ceil((rank-6) * 1.1) 
            
        return elo

#TODO: Remove this for now
#lastMatch: Match = Match()

#myUser: User = User(1, "zen")

#lastMatch.team1.append(myUser)

#lastMatch.SetStats(1, 1, "hp", 10, 3, 5, 40, True)
#lastMatch.SetStats(1, 2, "hp", 10, 3, 5, 40, True)
#lastMatch.Print()

#TODO: Implement a better test data set that includes team 1 and team 2
e = EloCalculator()

myP: Player = Player()
myP.kills = 50 #30 #50
myP.deaths = 17 #20 #17
myP.assists = 59 #15 #59
myP.objs = 53 #30 #53

print(f"New System: {e.CalculateElo(myP, 1, True)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(3, True, 4)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(3, False, 4, 0)}")



#TODO: Remove this
"""
print(LegacyEloCalculate(0, True, 1))
print(LegacyEloCalculate(4, True, 3))
print(LegacyEloCalculate(2, True, 4))
print(LegacyEloCalculate(3, False, 1))
print(LegacyEloCalculate(2, False, 3))
print(LegacyEloCalculate(0, False, 4))
print(LegacyEloCalculate(0, True, 1, 1)+LegacyEloCalculate(0, True, 1, 2)+LegacyEloCalculate(0, True, 1, 3)+LegacyEloCalculate(0, True, 1, 4)+LegacyEloCalculate(0, True, 1, 4))
print(LegacyEloCalculate(0, True, 1, 1)+LegacyEloCalculate(0, True, 1, 2)+LegacyEloCalculate(0, True, 1, 3)+LegacyEloCalculate(0, False, 1, 0)+LegacyEloCalculate(0, False, 1, 0))
"""