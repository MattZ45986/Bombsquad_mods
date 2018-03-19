import bs
import random

def bsGetAPIVersion():
    return 4

def bsGetGames():
    return [NewGame]

def bsGetLevels():
    return [bs.Level('NewGame 124',
                     displayName='${GAME}',
                     gameType=NewGame,
                     settings={},
                     previewTexName='courtyardPreview')]

class NewGame(bs.TeamGameActivity):
    @classmethod
    def getName(cls):
        return 'Flag Day'
    
#Gives it how things are scored
    @classmethod
    def getScoreInfo(cls):
        return {'scoreType':'points'}

    @classmethod
    def getDescription(cls,sessionType):
        return 'Pick up flags to receive a prize.\nBut beware...'

    @classmethod
    def getSupportedMaps(cls,sessionType):
        return ['Courtyard']
        
    @classmethod
    def supportsSessionType(cls,sessionType):
        return True if issubclass(sessionType,bs.FreeForAllSession) else False

    def onTransitionIn(self):
        #Sets the music to "To the Death"
        bs.TeamGameActivity.onTransitionIn(self,music='ToTheDeath')

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)
        bs.ScoreBoard(label='Points')
        self._bots = bs.BotSet()
        self._scoredis = bs.ScoreBoard(label='Points')
        for team in self.teams:
            team.gameData['score'] = 0
        for team in self.teams:
            self._scoredis.setTeamValue(team,team.gameData['score'])
        self._count = 1
        self._flag1 = bs.Flag(position=(0,3,1),touchable=True,color=(0,0,1))
        self._flag2 = bs.Flag(position=(0,3,-5),touchable=True,color=(1,0,0))
        self._flag3 = bs.Flag(position=(3,3,-2),touchable=True,color=(0,1,0))
        self._flag4 = bs.Flag(position=(-3,3,-2),touchable=True,color=(1,1,1))
        self._flag5 = bs.Flag(position=(1.8,3,.2),touchable=True,color=(0,1,1))
        self._flag6 = bs.Flag(position=(-1.8,3,.2),touchable=True,color=(1,0,1))
        self._flag7 = bs.Flag(position=(1.8,3,-3.8),touchable=True,color=(1,1,0))
        self._flag8 = bs.Flag(position=(-1.8,3,-3.8),touchable=True,color=(0,0,0))
        self._flag9 = bs.Flag(position=(-10,5,5), touchable=True, color=(.5,.5,.5))

    def handleMessage(self,m):
        if isinstance(m,bs.FlagPickedUpMessage):
            m.flag._lastPlayerToHold = m.node.getDelegate().getPlayer()
            self._player = m.node.getDelegate()
            self._prizeRecipient = m.node.getDelegate().getPlayer()
            self.killFlags()
            self.givePrize(random.randint(1,8))
        if isinstance(m,bs.PlayerSpazDeathMessage):
            guy = m.spaz.getPlayer()
            bs.screenMessage(str(guy.getName()) + " died!",color=guy.color)
            self.checkGame()
        if isinstance(m,bs.SpazBotDeathMessage):
            team = self._prizeRecipient.getTeam()
            team.gameData['score'] += self._badGuyCost
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])
                                              
    def resetFlags(self):
        #remake the flags
        self._flag1 = bs.Flag(position=(0,3,1),touchable=True,color=(0,0,1))
        self._flag2 = bs.Flag(position=(0,3,-5),touchable=True,color=(1,0,0))
        self._flag3 = bs.Flag(position=(3,3,-2),touchable=True,color=(0,1,0))
        self._flag4 = bs.Flag(position=(-3,3,-2),touchable=True,color=(1,1,1))
        self._flag5 = bs.Flag(position=(1.8,3,.2),touchable=True,color=(0,1,1))
        self._flag6 = bs.Flag(position=(-1.8,3,.2),touchable=True,color=(1,0,1))
        self._flag7 = bs.Flag(position=(1.8,3,-3.8),touchable=True,color=(1,1,0))
        self._flag8 = bs.Flag(position=(-1.8,3,-3.8),touchable=True,color=(0,0,0))

    def killFlags(self):
        #destroy all the flags by erasing all references to them, indicated by None similar to null
        self._flag1 = None
        self._flag2 = None
        self._flag3 = None
        self._flag4 = None
        self._flag5 = None
        self._flag6 = None
        self._flag7 = None
        self._flag8 = None

    def givePrize(self, prize):

        if prize == 1:
            self._prizeRecipient.actor.curse()
            bs.screenMessage("You were", color=(1,0,0))
            bs.screenMessage("CURSED", color=(.1,.1,.1))
            self.resetFlags()
        if prize == 2:
            self._prizeRecipient.actor.handleMessage(bs.FreezeMessage())
            self._prizeRecipient.actor.handleMessage(bs.ShouldShatterMessage())
            bs.screenMessage("You were", color=(1,1,1))
            bs.screenMessage("FROZEN", color=(.7,.7,1))
            self.resetFlags()
        if prize == 3:
            team = self._prizeRecipient.getTeam()
            team.gameData['score'] += 100
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])
            bs.screenMessage("!!!You won 100 points!!!", color=(0,.9,0))
            self.resetFlags()
        if prize == 4:
            team = self._prizeRecipient.getTeam()
            team.gameData['score'] += 10
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])
            bs.screenMessage("You won 10 points", color=(.1,1,.1))
            self.resetFlags()
        if prize == 5:
            bs.screenMessage("BOMB RAIN!", color=(1,.5,.16))
            for bzz in range(-5,6):
                for azz in range(-5,2):
                    self.makeBomb(bzz,azz)
            self.resetFlags()
        if prize == 6:
            self._badGuyCost = 50
            bs.screenMessage("NINJA!", color=(.1,.1,.1))
            self._bots.spawnBot(bs.NinjaBotProShielded,pos=(0,2.5,-2))
            self._player.equipBoxingGloves()
            self._player.equipShields()
            self.resetFlags()
        if prize == 7:
            self._badGuyCost = 10
            bs.screenMessage("Lame Guys", color=(1,.5,.16))
            for a in range(-1,2):
                for b in range(-3,0):
                    self._bots.spawnBot(bs.ToughGuyBotLame,pos=(a,2.5,b))
            self._player.equipBoxingGloves()
            self._player.equipShields()
            self.resetFlags()
        if prize == 8:
            bs.screenMessage("!JACKPOT!", color=(1,0,0))
            bs.screenMessage("!JACKPOT!", color=(0,1,0))
            bs.screenMessage("!JACKPOT!", color=(0,0,1))
            team = self._prizeRecipient.getTeam()
            team.gameData['score'] += 500
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])
            self.resetFlags()

    def makeBomb(self,xpos,zpos):
        b=bs.Bomb(position=(xpos, 12, zpos)).autoRetain()

    def checkGame(self):
        livingTeamCount = 0
        for team in self.teams:
            for player in team.players:
                if player.isAlive():
                    #if a player is actually alive then increase the number of players alive (When a player is in the process of dying they are still considered alive)
                    livingTeamCount += 1
                    break
        if livingTeamCount == 1:
            self.endGame()

    def endGame(self):
        results = bs.TeamGameResults()
        for team in self.teams:
            results.setTeamScore(team, team.gameData['score'])
        self.end(results=results)
