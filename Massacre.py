#Massacre

import bs
import random

def bsGetAPIVersion():
    return 4


def bsGetGames():
    return [NewGame]

def bsGetLevels():
    return [bs.Level('NewGame 123',
                     displayName='${GAME}',
                     gameType=NewGame,
                     settings={},
                     previewTexName='courtyardPreview')]


class NewGame(bs.TeamGameActivity):

    @classmethod
    def getName(cls):
        return 'Massacre'

    @classmethod
    def getScoreInfo(cls):
        return {'scoreType':'points'}

    @classmethod
    def getDescription(cls,sessionType):
        return 'Kill as many as you can.'
    
    @classmethod
    def getSupportedMaps(cls,sessionType):
        return ['Doom Shroom']
        

    @classmethod
    def supportsSessionType(cls,sessionType):
        return True if issubclass(sessionType,bs.CoopSession) else False

    def onTransitionIn(self):
        bs.TeamGameActivity.onTransitionIn(self,music='ToTheDeath')

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)
        bs.gameTimer(60000,bs.WeakCall(self.endGame))
        bs.OnScreenCountdown(60).start()
        bs.gameTimer(1000,bs.WeakCall(self.spawnBots))
        self._gamescore = 0
        self._scoredis = bs.ScoreBoard()
        self._scoredis.setTeamValue(self.teams[0],self._gamescore)
        self.setupStandardPowerupDrops(enableTNT=True)
        

    def spawnBots(self):
        self._gamescore = 0
        self._bots = bs.BotSet()
        bs.screenMessage('Here come the Bots')
        for i in range(0,100):
            p = [0, 2.5, -3]
            bs.gameTimer(1000,bs.Call(self._bots.spawnBot,bs.ToughGuyBotLame,pos=(p[0] + random.randint(-3,3),2.5,p[2] + random.randint(-3,3)),spawnTime=3000))
    def onPlayerLeave(self, player):
        message = str(player.getName(icon=False)) + " has chickened out!"
        bs.screenMessage(message, color=player.color, top=True)

    def handleMessage(self,m):

        if isinstance(m,bs.PlayerSpazDeathMessage):
            bs.TeamGameActivity.handleMessage(self,m)
            self.respawnPlayer(m.spaz.getPlayer())
            bs.screenMessage("You DIED!", color=(1,0,0))
        elif isinstance(m,bs.SpazBotDeathMessage):
            self._gamescore = 5 + self._gamescore
            bs.TeamGameActivity.handleMessage(self,m)
            if self._gamescore % 100 == 0:
                bs.screenMessage("Nice!", color=(0,1,0))
            self.scoreBoard()
            self.respawn()
        else:
            bs.TeamGameActivity.handleMessage(self,m)

    def scoreBoard(self):
        for team in self.teams:
            self._scoredis.setTeamValue(team,self._gamescore)


    def respawn(self):
        p = [0,2.5,-3]
        bs.gameTimer(1000,bs.WeakCall(self._bots.spawnBot,bs.ToughGuyBotLame,pos=(p[0] + random.randint(-3,3),2.5,p[2] + random.randint(-3,3)),spawnTime=3000))
        
      
    def endGame(self):
        ourResults = bs.TeamGameResults()
        for team in self.teams:
            ourResults.setTeamScore(team, self._gamescore)
        self.end(results=ourResults)
