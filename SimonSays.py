#SimonSays
import bs

def bsGetAPIVersion():
    return 4

def bsGetGames():
    return [SimonSays]

class SimonSays(bs.TeamGameActivity):
    @classmethod
    def getName(cls):
        return "Simon Says"

    @classmethod
    def getDescription(cls, sessionType):
        return "You had better do what Simon says..."

    @classmethod
    def getScoreInfo(cls):
        return{'scoreType':'points'}

    @classmethod
    def getSettings(cls, sessionType):
        return [("Epic Mode", {'default': False})]
    
    @classmethod
    def getSupportedMaps(cls, sessionType):
        return ["Courtyard"]

    @classmethod
    def supportsSessionType(cls, sessionType):
        return True if issubclass(sessionType, bs.FreeForAllSession) else False

    def __init__(self,settings):
        bs.TeamGameActivity.__init__(self,settings)
        if self.settings['Epic Mode']: self._isSlowMotion = True
        self.roundNum = 1
        self._r1 = 2
        n1 = bs.newNode('locator',attrs={'shape':'circle','position':(-4,0,-6),
                                         'color':(1,0,0),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n2 = bs.newNode('locator',attrs={'shape':'circle','position':(0,0,-6),
                                         'color':(0,1,0),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n3 = bs.newNode('locator',attrs={'shape':'circle','position':(4,0,-6),
                                         'color':(0,0,1),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n4 = bs.newNode('locator',attrs={'shape':'circle','position':(-4,0,-2),
                                         'color':(1,1,0),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n5 = bs.newNode('locator',attrs={'shape':'circle','position':(0,0,-2),
                                         'color':(0,1,1),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n6 = bs.newNode('locator',attrs={'shape':'circle','position':(4,0,-2),
                                         'color':(1,0,1),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n7 = bs.newNode('locator',attrs={'shape':'circle','position':(-4,0,2),
                                         'color':(.5,.5,.5),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n8 = bs.newNode('locator',attrs={'shape':'circle','position':(0,0,2),
                                         'color':(.5,.325,0),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        n9 = bs.newNode('locator',attrs={'shape':'circle','position':(4,0,2),
                                         'color':(1,1,1),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        bs.animateArray(n1,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n2,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n3,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n4,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n5,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n6,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n7,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n8,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n9,'size',1,{0:[0.0],200:[self._r1*2.0]})

    def onTransitionIn(self):
        bs.TeamGameActivity.onTransitionIn(self,music='FlagCatcher')

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)
        for team in self.teams:
            team.gameData['score'] = 0
        for player in self.players:
            player.gameData['score'] = 0
        self.explainGame()

    def explainGame(self):
        bs.screenMessage("Follow the commands...")
        bs.screenMessage("but only when Simon says!")
        bs.gameTimer(3000, self.callRound)

    def callRound(self):

    def inCircle(self, pos):
        circles = []
        pos[0] = x
        pos[2] = z
        if (x + 4) ** 2 + (z + 6) ** 2 < 4: circles.append("red")
        elif (x) ** 2 + (z + 6) ** 2 < 4: circles.append("green")
        elif (x - 4) ** 2 + (z + 6) ** 2 < 4: circles.append("blue")
        elif (x + 4) ** 2 + (z + 2) ** 2 < 4: circles.append("yellow")
        elif (x) ** 2 + (z + 2) ** 2 < 4: circles.append("teal")
        elif (x - 4) ** 2 + (z + 2) ** 2 < 4: circles.append("purple")
        elif (x + 4) ** 2 + (z - 2) ** 2 < 4: circles.append("gray")
        elif (x) ** 2 + (z - 2) ** 2 < 4: circles.append("orange")
        elif (x - 4) ** 2 + (z - 2) ** 2 < 4: circles.append("white")
        else: circles.append("none")
        if x < -2: circles.append("left")
        if x > 2: circles.append("right")
        if x > -2 and x < 2: circles.append("center")

    def handleMessage(self, m):
        if isinstance(m, bs.PlayerSpazDeathMessage): self.endGame()

    def endGame(self):
        results = bs.TeamGameResults()
        for team in self.teams:
            results.setTeamScore(team, team.gameData['score'])
        self.end(results=results)
        
