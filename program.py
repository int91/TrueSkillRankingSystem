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

LOSS_WEIGHT = 0.6
DEATH_WEIGHT = 1

ENEMY_SKILL_WEIGHT = 0.3
TEAM_SKILL_WEIGHT = 1

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
        
        medianKills: int = 0
        medianDeaths: int = 0
        medianAssists: int = 0
        medianObjs: int = 0
        
        killsArr: List[int] = []
        deathsArr: List[int] = []
        assistArr: List[int] = []
        objArr: List[int] = []
        
        #If the player accidentally gets put in the team array then remove them
        #if (p in team):
            #team.remove(p)
        
        for e in team:
            #Adds all team data to respective arrays
            killsArr.append(e.kills)
            deathsArr.append(e.deaths)
            assistArr.append(e.assists)
            objArr.append(e.objs)
            
            
            #TODO: Remove all comments below
            #medianKills += e.kills
            #medianDeaths += e.deaths
            #medianAssists += e.assists
            #medianObjs += e.objs
            
            #NOTE: This is a placeholder system for now
            #relKills += (p.kills-e.deaths)/e.deaths #relative deaths to this enemy
            #relDeaths += (e.deaths-p.deaths)/p.deaths #relative deaths to this enemy
            #if (e.assists != 0):
                #relAssist += (p.assists-e.assists)/e.assists #relative assists to this enemy
            #if (e.objs != 0):
                #relObjs += (p.objs-e.objs)/e.objs #relative objective points to this enemy

        killsArr.sort()
        deathsArr.sort()
        assistArr.sort()
        objArr.sort()

        #Takes the median of the array data
        medianKills = statistics.mean(killsArr)
        medianDeaths = statistics.mean(deathsArr)
        medianAssists = statistics.mean(assistArr)
        medianObjs = statistics.mean(objArr)

        relKills = (p.kills-medianKills)/medianKills
        relDeaths = (medianDeaths-p.deaths)/p.deaths
        if (medianAssists != 0):
            relAssist = (p.assists-medianAssists)/medianAssists
        else:
            relAssist = p.assists
        if (medianObjs != 0):
            relObjs = (p.objs-medianObjs)/medianObjs
        else:
            relObjs = p.objs
        
        #TODO: Remove this
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
        
        #Testing data set (Taken from a pro-league SnD match)
        e1 = Player(9, 6, 2, 0)
        e2 = Player(11, 6, 3, 1)
        e3 = Player(3, 6, 2, 1)
        e4 = Player(1, 5, 0, 0)
        e5 = Player(12, 6, 4, 0)
        
        f1 = Player(3, 8, 3, 1)
        f2 = Player(5, 7, 0, 1)
        f3 = Player(6, 7, 2, 1)
        f4 = Player(6, 8, 1, 0)
        
        enemyTeam: List[Player] = [e1, e2, e3, e4, e5]
        playersTeam: List[Player] = [f1, f2, f3, f4] #self.CalculateRelatives will remove the player from this array
        
        #Getting relatives of the player to the enemy team and their team
        eTeamRels = self.CalculateRelatives(p, enemyTeam)
        pTeamRels = self.CalculateRelatives(p, playersTeam)
        
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
        
        #Adds all data * 100
        relKills += (enemyRelKills * 100) * ENEMY_SKILL_WEIGHT
        relDeaths += (enemyRelDeaths * 100) * ENEMY_SKILL_WEIGHT
        relAssist += (enemyRelAssists * 100) * ENEMY_SKILL_WEIGHT
        relObjs += (enemyRelObj * 100) * ENEMY_SKILL_WEIGHT
        
        relKills += (playerRelKills * 100) * TEAM_SKILL_WEIGHT
        relDeaths += (playerRelKills * 100) * TEAM_SKILL_WEIGHT
        relAssist += (playerRelKills * 100)* TEAM_SKILL_WEIGHT
        relObjs += (playerRelKills * 100) * TEAM_SKILL_WEIGHT
        
        result += relKills * KILL_WEIGHT
        result += relAssist * ASSIST_WEIGHT
        result += relObjs * OBJ_WEIGHT
        result -= relDeaths * DEATH_WEIGHT
        
        #TODO: Add better win loss cases that better reflect the affect of each outcome
        #NOTE: I think this is done, not quite sure atm
        if (won):
            
            if (result < 0):
                result += result * (1-WIN_WEIGHT)
            else:
                result *= WIN_WEIGHT
                
        else:
            
            if (result < 0):
                result += result * (1-LOSS_WEIGHT)
            else:
                result *= LOSS_WEIGHT
                
        
        if (rank >= 1):
            result *= (RANKS-rank)*RANK_WEIGHT
        
        return math.ceil(result/END_RESULT_DIV)

    #Seems fine for now but you get Diamond after winning ALL placements
    #This will be used until the new system is read to be used
    def LegacyEloCalculate(self, rank: int, result: bool, lPlace: int, winstreak: int = 0) -> int:
        elo: int = 0
        if (result):
            #If win, add result and then calculate bonus based on placement
            elo += 28
            if (lPlace <= 3):
                elo += int(4/lPlace)
                
            if (rank == 0 and winstreak != 0):
            #If unranked and on winstreak calculate bonus
                elo += -int(((rank-6) * 3 * ((winstreak+1)*1.5)))
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

e = EloCalculator()

myP: Player = Player()
myP.kills = 9 #30 #50
myP.deaths = 6 #20 #17
myP.assists = 1 #15 #59
myP.objs = 1 #30 #53

print(f"New System: {e.CalculateElo(myP, 1, False, 0)}")

"""
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(0, True, 1)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(0, True, 1, 1)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(0, True, 1, 2)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(0, True, 1, 3)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(0, True, 1, 4)}")
print(f"Legacy Elo (Fixed) System: {e.LegacyEloCalculate(1, False, 4)}")
"""