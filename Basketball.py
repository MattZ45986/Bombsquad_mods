#Basketball
import bs
import bsUtils


def bsGetAPIVersion():
    return 4

def bsGetGames():
    return [Basketball]

class ImpactMessage(object):
    pass

class Referee(bs.SpazBot):
    character = 'Bernard'
    chargeDistMax = 9999
    throwDistMin = 9999
    throwDistMax = 9999
    color=(0,0,0)
    highlight=(1,1,1)
    punchiness = 0.0
    chargeSpeedMin = 0.0
    chargeSpeedMax = 0.0

class Hoop(bs.Actor):
    def __init__(self,position):
        self._r1 = 0.7
        self._rFudge = 0.15
        bs.Actor.__init__(self)
        self._position = bs.Vector(*position)
        p1 = position
        p2 = (position[0]+1,position[1],position[2])
        p3 = (position[0]-1,position[1],position[2])
        showInSpace = False
        self._hit = False
        n1 = bs.newNode('locator',attrs={'shape':'circle','position':p1,
                                         'color':(1,0,0),'opacity':0.5,
                                         'drawBeauty':showInSpace,'additive':True})
        n2 = bs.newNode('locator',attrs={'shape':'circle','position':p2,
                                         'color':(1,0,0),'opacity':0.5,
                                         'drawBeauty':showInSpace,'additive':True})
        n3 = bs.newNode('locator',attrs={'shape':'circle','position':p3,
                                         'color':(1,0,0),'opacity':0.5,
                                         'drawBeauty':showInSpace,'additive':True})
        bs.animateArray(n1,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n2,'size',1,{0:[0.0],200:[self._r1*2.0]})
        bs.animateArray(n3,'size',1,{0:[0.0],200:[self._r1*2.0]})
        self._nodes = [n1,n2,n3]

class BasketBallFactory(bs.BombFactory):
    def __init__(self):
        self.basketBallMaterial = bs.Material()
        self.basketBallMaterial.addActions(conditions=(('weAreOlderThan',200),
                        'and',('theyAreOlderThan',200),
                        'and',('evalColliding',),
                        'and',(('theyHaveMaterial',bs.getSharedObject('footingMaterial')),
                               'or',('theyHaveMaterial',bs.getSharedObject('objectMaterial')))),
            actions=(('message','ourNode','atConnect',ImpactMessage())))
        bs.BombFactory.__init__(self)
    
    
class BasketBomb(bs.Bomb):
    def __init__(self,position=(0,1,0),velocity=(0,0,0),bombType='normal',blastRadius=2.0,sourcePlayer=None,owner=None):
        bs.Actor.__init__(self)
        factory = BasketBallFactory()
        self.bombType = 'basketball'
        self._exploded = False
        self.blastRadius = blastRadius
        self._explodeCallbacks = []
        self.sourcePlayer = sourcePlayer
        self.hitType = 'impact'
        self.hitSubType = 'basketball'
        owner = bs.Node(None)
        self.owner = owner
        materials = (factory.bombMaterial, bs.getSharedObject('objectMaterial'))
        materials = materials + (factory.normalSoundMaterial,)
        materials = materials + (factory.basketBallMaterial,)
        self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere',
                                          'model':factory.bombModel,
                                          'shadowSize':0.3,
                                          'colorTexture':bs.getTexture('aliColor'),
                                          'reflection':'powerup',
                                          'reflectionScale':[1.5],
                                          'materials':materials})
        bsUtils.animate(self.node,"modelScale",{0:0, 200:1.3, 260:1})


    def handleMessage(self, m):
        if isinstance(m, bs.OutOfBoundsMessage):
            self.getActivity().respawnBall()
            bs.Bomb.handleMessage(self, m)
        elif isinstance(m, bs.PickedUpMessage):
            self.heldLast = m.node.getDelegate().getPlayer()
            self.getActivity().heldLast = self.heldLast
            if self.heldLast in self.getActivity().teams[0].players: self.getActivity().possession = True
            else: self.getActivity().possession = False
            bs.Bomb.handleMessage(self, m)
        elif isinstance(m, ImpactMessage): self.getActivity().handleShot(self)
        else: bs.Bomb.handleMessage(self, m)



class Basketball(bs.TeamGameActivity):
    @classmethod
    def getName(cls):
        return "Basketball"

    @classmethod
    def getDescription(cls, sessionType):
        return "A classic game, Bombsquad style!"

    @classmethod
    def getScoreInfo(cls):
        return{'scoreType':'points'}

    @classmethod
    def getSettings(cls, sessionType):
        return [("Epic Mode", {'default': False}),
                ("Enable Running", {'default': True}),
                ("Enable Jumping", {'default': True}),
                ("Play To: ", {
                    'choices': [
                        ('1 point', 1),
                        ('11 points', 11),
                        ('21 points', 21),
                        ('45 points', 45),
                        ('100 points', 100)
                        ],
                    'default': 21})]
    @classmethod
    def getSupportedMaps(cls, sessionType):
        return ['Courtyard']

    @classmethod
    def supportsSessionType(cls, sessionType):
        return True if issubclass(sessionType, bs.TeamsSession) else False

    def __init__(self,settings):
        bs.TeamGameActivity.__init__(self,settings)
        if self.settings['Epic Mode']: self._isSlowMotion = True
        self.info = bs.NodeActor(bs.newNode('text',
                                                   attrs={'vAttach': 'bottom',
                                                          'hAlign': 'center',
                                                          'vrDepth': 0,
                                                          'color': (0,.2,0),
                                                          'shadow': 1.0,
                                                          'flatness': 1.0,
                                                          'position': (0,0),
                                                          'scale': 0.8,
                                                          'text': "Created by MattZ45986 on Github",
                                                          }))
        self.possession = True
        self.heldLast = None
        self._bots = bs.BotSet()
        self.hoop = Hoop((0,5,-8))
        self._scoredis = bs.ScoreBoard()
        self.referee = Referee

        bs.gameTimer(10,bs.Call(self._bots.spawnBot,self.referee,pos=(-6,3,-6),spawnTime=1))
    def onTransitionIn(self):
        bs.TeamGameActivity.onTransitionIn(self,music='Sports')

    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)
        s = self.settings
        for player in self.players:
            player.actor.connectControlsToPlayer(enableBomb=False, enableRun = s["Enable Running"], enableJump = s["Enable Jumping"])
        self.respawnBall()
        self.teams[0].gameData['score'] = 0
        self.teams[1].gameData['score'] = 0
        self._scoredis.setTeamValue(self.teams[0],self.teams[1].gameData['score'])
        self._scoredis.setTeamValue(self.teams[1],self.teams[1].gameData['score'])
        self.updateScore()
        self.checkEnd()

    def respawnBall(self):
        self.basketball = BasketBomb(position=(0,5,0)).autoRetain()

    def handleMessage(self, m):
        if isinstance(m, bs.SpazBotDeathMessage):
            if m.killerPlayer in self.teams[0].players:
                results = bs.TeamGameResults()
                results.setTeamScore(self.teams[0],0)
                results.setTeamScore(self.teams[1],100)
                self.end(results=results)
                bs.screenMessage("Don't take it out on the ref!", color=(1,0,0))
            elif m.killerPlayer in self.teams[1].players:
                results = bs.TeamGameResults()
                results.setTeamScore(self.teams[1],0)
                results.setTeamScore(self.teams[0],100)
                self.end(results=results)
                bs.screenMessage("Don't take it out on the ref!", color=(0,0,1))
        elif isinstance(m, bs.PlayerSpazDeathMessage):
            if m.killed:
                if m.spaz.getPlayer() in self.teams[0].players: team = self.teams[0]
                elif m.spaz.getPlayer() in self.teams[1].players: team = self.teams[1]
                if m.killerPlayer not in team.players:
                    bs.screenMessage("FOUL", color=(1,0,0))
                    self.giveFoulShots(m.spaz)
            else: self.respawnPlayer(m.spaz.getPlayer())

        else: bs.TeamGameActivity.handleMessage(self, m)

    def giveFoulShots(self, player):
        pass
    def handleShot(self, ball):
        if ball.node.position[0] > -1.5 and ball.node.position[0] < 1.5:
            if ball.node.position[1] > 4 and ball.node.position[1] < 5:
                if ball.node.position[2] > -9 and ball.node.position[2] < -8:
                    bs.screenMessage("Score!")
                    if self.possession: self.teams[0].gameData['score'] += 2
                    else: self.teams[1].gameData['score'] += 2
                    self.updateScore()
                    ball.node.delete()
                    self.respawnBall()
    def updateScore(self):
        for team in self.teams:
            self._scoredis.setTeamValue(team,team.gameData['score'])
        self.checkEnd()

    def checkEnd(self):
        for team in self.teams:
            i = 0
            if team.gameData['score'] >= self.settings['Play To: ']: self.endGame()
            for player in team.players:
                if player.isAlive(): i = 1
            if i == 0: self.endGame()
