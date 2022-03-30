from typing import List
import math

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
    def __init__(self):
        #Player's discord user
        self.user: User = None

        #Player's stats for that game (NOT MATCH)
        self.kills: int = 0
        self.deaths: int = 0
        self.assists: int = 0
        self.objs: int = 0

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
WIN_WEIGHT = 1.3
LOSS_WEIGHT = 1.2
KILL_WEIGHT = 1.4
ASSIST_WEIGHT = 1.2
DEATH_WEIGHT = 1.1
OBJ_WEIGHT = 1.7
POS_WEIGHT = 1.2 #POS_WEIGHT * LeaderboardPosition = outcome for this (This isn't used in the new Calculations but might be ater on)
RANKS = 5
RANK_WEIGHT = 0.1

def CalculatePlace(Player, Teammates):
    pass

class EloCalculator():
    def CalculateRelatives(self, p: Player, enemyTeam: List[Player]) -> List[float]:
        results: List[float] = []
        
        relKills: float = 0
        relDeaths: float = 0
        relAssist: float = 0
        relObjs: float = 0
        
        for e in enemyTeam:
            relKills += (p.kills-e.kills)/e.kills #relative kills to this enemy
            relDeaths += (e.deaths-p.deaths)/p.deaths#relative deaths to this enemy
            if (e.assists != 0):
                relAssist += (p.assists-e.assists)/e.assists #relative assists to this enemy
            if (e.objs != 0):
                relObjs += (p.objs-e.objs)/e.objs #relative objective points to this enemy
            
        #Gets average of relatives
        teamSize = len(enemyTeam)
        relKills /= teamSize
        relDeaths /= teamSize
        relAssist /= teamSize
        relObjs /= teamSize
        
        results = [relKills, relDeaths, relAssist, relObjs]
        return results
        
        
        
    #Adjust params to better fit the functions purpose
    def CalculateElo(self, p: Player, lPos: int, won: bool, Teammates=None) -> int:
        result: float = 0
        #Get the avg values of team stats
        #Get relative values of enemy stats
        
        #Calculate team first, then enemy team
        
        #TODO: Implement team calculations. Note: Use a new method - self.CalculateAverage and pass in the player and their team
        #Team averages excludes player
        teamAvgKills: float = 3 #Avg kills of team
        teamAvgDeaths: float = 5 #Avg deaths of team
        teamAvgAssists: float = 10 #Avg assists of team
        teamAvgObj: float = 3 #Avg objs of team
        
        #Test data set of 2 out of the 4 enemy players (stats taken from a Pro-League Search & Destroy match)
        e1 = Player()
        e1.kills = 18
        e1.deaths = 7
        e1.assists = 0
        e1.objs = 0
        e2 = Player()
        e2.kills = 9
        e2.deaths = 8
        e2.assists = 0
        e2.objs = 2
        
        #Getting average relatives of the player to the enemy team
        #TODO: Replace relative calc with avg calc then do relatives based on team and enemy after this Note: Use a new method - self.CalculateAverage and pass in the player and their team
        eTeamRels = self.CalculateRelatives(p, [e1, e2])
        
        #TODO: Convert Self.CalculateRelatives into a function that only does relative calculation for player & X user (I think)
        enemyRelKills: float = eTeamRels[0] #you got 80% more kills than the enemy team
        enemyRelDeaths: float = eTeamRels[1] # you died 70% more than the enemy team
        enemyRelAssists: float = eTeamRels[2] #you got 30% more assists than the enemy team
        enemyRelObj: float = eTeamRels[3] #you got 10% less objectives than the enemy team
        
        relKills: float = 0
        relDeaths: float = 0
        relAssist: float = 0
        relObjs: float = 0
        #relatives here are percentages * 100 for more accuracy with weights
        
        relKills = (p.kills-teamAvgKills)/teamAvgKills * 100 #relative kills
        relDeaths = (teamAvgDeaths-p.deaths)/p.deaths * 100 #relative deaths
        if (p.assists != 0):
            relAssist = (p.assists-teamAvgAssists)/teamAvgAssists * 100 #relative assists
        relObjs = (p.objs-teamAvgObj)/teamAvgObj * 100 #relative objective points
        
        
        relKills += enemyRelKills * 100
        relDeaths += enemyRelDeaths * 100
        relAssist += enemyRelAssists * 100
        relObjs += enemyRelObj * 100
        
        #TODO: Remove this
        #print(relKills)
        #print(relDeaths)
        #print(relAssist)
        #print(relObjs)
        
        result += relKills * KILL_WEIGHT
        result += relDeaths * DEATH_WEIGHT
        result += relAssist * ASSIST_WEIGHT
        result += relObjs * OBJ_WEIGHT
        
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
            result *= -LOSS_WEIGHT
        
        return math.ceil(result/12)

    #Seems fine for now but you get Diamond after winning ALL placements
    def LegacyEloCalculate(self, rank: int, result: bool, lPlace: int, winstreak: int = 0) -> int:
        elo: int = 0
        if (result):
            #If win, add result and then calculate bonus based on placement
            elo += 14
            if (lPlace <= 3):
                elo += int(4/lPlace)
                
            if (rank == 0 and winstreak != 0):
            #If unranked and on winstreak calculate bonus
                elo += -int(((rank-8) * 3 * (winstreak+1*1.5)))
            elif (winstreak == 0 and result):
            #If not unranked calculate sub based on rank out of max ranks
                elo += -int((rank-8) * 3)
                
        else:
            #If los, subtract result and then calculate -bonus based on placement
            elo -= 10
            if (lPlace > 1):
                elo -= math.ceil(lPlace/2) * 2
            
            if (rank == 0):
                #If unranked calculate lost elo
                elo += math.ceil(elo * 2.2)  
            
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
myP.kills = 11
myP.deaths = 7
myP.assists = 0
myP.objs = 3

print(f"New System: {e.CalculateElo(myP, 1, False)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(1, True, 1, 0)}")



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