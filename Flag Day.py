import bs
import random

# http://www.froemling.net/docs/bombsquad-python-api
#if you really want in-depth explanations of specific terms, go here ^



#This gives the API version to the game to make sure that we are using the right vocabulary
def bsGetAPIVersion():
    return 4

#This tells the game what kind of program this is
def bsGetGames():
    return [NewGame]

#this gives the game a unique code for our game in this case: "NewGame 124" (One of my other games was NewGame123) P.S. Don't change this half-way through making it
def bsGetLevels():
    return [bs.Level('NewGame 124',
                     displayName='${GAME}',
                     gameType=NewGame,
                     settings={},
                     previewTexName='courtyardPreview')]

#this is the class that will actually be saved to the game as a mini-game
class NewGame(bs.TeamGameActivity):

#gives it a name
    @classmethod
    def getName(cls):
        return 'Flag Day'

#Gives it how things are scored
    @classmethod
    def getScoreInfo(cls):
        return {'scoreType':'points'}

#Gives a description of the game
    @classmethod
    def getDescription(cls,sessionType):
        return 'Pick up flags to receive a prize.\nBut beware...'

#Gives which maps are supported, in this case only courtyard though you could probably try it with others, too
    @classmethod
    def getSupportedMaps(cls,sessionType):
        return ['Courtyard']

#Tells the game what kinds of seesions are supported by this mini-game
    @classmethod
    def supportsSessionType(cls,sessionType):
        return True if issubclass(sessionType,bs.FreeForAllSession) else False

#Tells the game what to do on the transition in
    def onTransitionIn(self):
        #Sets the music to "To the Death"
        bs.TeamGameActivity.onTransitionIn(self,music='ToTheDeath')

    def onBegin(self):
        #Do normal stuff: calls to the main class to operate everything that usually would be done
        bs.TeamGameActivity.onBegin(self)
        #Declare a set of bots (enemies) that we will use later
        self._bots = bs.BotSet()
        #make another scoreboard? IDK why I did this, probably to make it easier to refer to in the future
        self._scoredis = bs.ScoreBoard(label='Points')
        #for each team in the game's directory, give them a score of zero
        for team in self.teams:
            team.gameData['score'] = 0
        #Now we go ahead and put that on the scoreboard
        for team in self.teams:
            self._scoredis.setTeamValue(team,team.gameData['score'])
        #Make the initial flags
        self._flag1 = bs.Flag(position=(0,3,1),touchable=True,color=(0,0,1))
        self._flag2 = bs.Flag(position=(0,3,-5),touchable=True,color=(1,0,0))
        self._flag3 = bs.Flag(position=(3,3,-2),touchable=True,color=(0,1,0))
        self._flag4 = bs.Flag(position=(-3,3,-2),touchable=True,color=(1,1,1))
        self._flag5 = bs.Flag(position=(1.8,3,.2),touchable=True,color=(0,1,1))
        self._flag6 = bs.Flag(position=(-1.8,3,.2),touchable=True,color=(1,0,1))
        self._flag7 = bs.Flag(position=(1.8,3,-3.8),touchable=True,color=(1,1,0))
        self._flag8 = bs.Flag(position=(-1.8,3,-3.8),touchable=True,color=(0,0,0))
        self._flag9 = bs.Flag(position=(-10,5,5), touchable=True, color=(.5,.5,.5))

#This handles all the messages that the game throws at us
    def handleMessage(self,m):
        #If it's a flag picked up...
        if isinstance(m,bs.FlagPickedUpMessage):
            #Get the last player to hold that flag
            m.flag._lastPlayerToHold = m.node.getDelegate().getPlayer()
            #Get the last actor to hold that flag (If you are a player, then your body is the actor, think of it like that)
            self._player = m.node.getDelegate()
            #The person to last hold a flag gets the prize, not the person to hold that flag, note.
            self._prizeRecipient = m.node.getDelegate().getPlayer()
            #Call a method to kill the flags
            self.killFlags()
            self.givePrize(random.randint(1,8))
        #If a player died...
        if isinstance(m,bs.PlayerSpazDeathMessage):
            #give them a nice farewell
            guy = m.spaz.getPlayer()
            bs.screenMessage(str(guy.getName()) + " died!",color=guy.color)
            #check to see if we can end the game
            self.checkGame()

        #If a bot died...
        if isinstance(m,bs.SpazBotDeathMessage):
            #find out which team the last person to hold a flag was on
            team = self._prizeRecipient.getTeam()
            #give them their points
            team.gameData['score'] += self._badGuyCost
            #update the scores
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])



#a method to remake the flags
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

#a method to kill the flags
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

#a method to give the prize recipient a prize depending on what flag he took (not really).
    def givePrize(self, prize):

        if prize == 1:
            #Curse him aka make him blow up in 5 seconds
            self._prizeRecipient.actor.curse()
            #give them a nice message
            bs.screenMessage("You were", color=(1,0,0))
            bs.screenMessage("CURSED", color=(.1,.1,.1))
            #reset the flags
            self.resetFlags()
        if prize == 2:
            #Make them appear frozen
            self._prizeRecipient.actor.handleMessage(bs.FreezeMessage())
            #then actually freeze them :)
            self._prizeRecipient.actor.handleMessage(bs.ShouldShatterMessage())
            #Again a nice message
            bs.screenMessage("You were", color=(1,1,1))
            bs.screenMessage("FROZEN", color=(.7,.7,1))
            self.resetFlags()
        if prize == 3:
            team = self._prizeRecipient.getTeam()
            #Give them a nice 100 points
            team.gameData['score'] += 100
            #update the score
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])
            bs.screenMessage("!!!You won 100 points!!!", color=(0,.9,0))
            self.resetFlags()
        if prize == 4:
            team = self._prizeRecipient.getTeam()
            #give 'em ten points
            team.gameData['score'] += 10
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])
            bs.screenMessage("You won 10 points", color=(.1,1,.1))
            self.resetFlags()
        if prize == 5:
            #Make it rain bombs
            bs.screenMessage("BOMB RAIN!", color=(1,.5,.16))
            #Set positions for the bombs to drop
            for bzz in range(-5,6):
                for azz in range(-5,2):
                    #for each position make a bomb drop there
                    self.makeBomb(bzz,azz)
            self.resetFlags()
        if prize == 6:
            #makes killing a bas guy worth 50 points
            self._badGuyCost = 50
            bs.screenMessage("NINJA!", color=(.1,.1,.1))
            #spawn a ninja
            self._bots.spawnBot(bs.NinjaBotProShielded,pos=(0,2.5,-2))
            #give our player boxing gloves...
            self._player.equipBoxingGloves()
            #...and a shield
            self._player.equipShields()
            self.resetFlags()
        if prize == 7:
            #makes killing a bad guy worth ten points
            self._badGuyCost = 10
            bs.screenMessage("Lame Guys", color=(1,.5,.16))
            #makes a set of nine positions
            for a in range(-1,2):
                for b in range(-3,0):
                    #and spawns one in each position
                    self._bots.spawnBot(bs.ToughGuyBotLame,pos=(a,2.5,b))
                    #and we give our player boxing gloves and a shield
            self._player.equipBoxingGloves()
            self._player.equipShields()
            self.resetFlags()
        if prize == 8:
            bs.screenMessage("!JACKPOT!", color=(1,0,0))
            bs.screenMessage("!JACKPOT!", color=(0,1,0))
            bs.screenMessage("!JACKPOT!", color=(0,0,1))
            team = self._prizeRecipient.getTeam()
            #GIVE THEM A WHOPPING 500 POINTS!!!
            team.gameData['score'] += 500
            # and update the scores
            for team in self.teams:
                self._scoredis.setTeamValue(team,team.gameData['score'])
            self.resetFlags()

#called in prize #5
    def makeBomb(self,xpos,zpos):
        #makes a bomb at the given position then auto-retains it aka: makes sure it doesn't disappear because there is no reference to it
        b=bs.Bomb(position=(xpos, 12, zpos)).autoRetain()

#checks to see if we should end the game
    def checkGame(self):
        #set the amount of players alive to zero
        livingTeamCount = 0
        for team in self.teams:
            for player in team.players:
                if player.isAlive():
                    #if a player is actually alive then increase the number of players alive (When a player is in the process of dying they are still considered alive)
                    livingTeamCount += 1
                    break
        #if there is only one alive (actually dead), end the game since they (are dead and) done with the game
        if livingTeamCount == 1:
            self.endGame()

#called when ready to end the game
    def endGame(self):
        results = bs.TeamGameResults()
        #Set the results for the game to display at the end of the game
        for team in self.teams:
            results.setTeamScore(team, team.gameData['score'])
        #End the game with the given results
        self.end(results=results)

"""     So there you have it, one python mod for a professional game.
    It's not that hard when you get familiar with the terms of the game, but it takes a while to get the first one goin'
    It took me a week and a half of pretty intense problem solving when I started, and that was over the summer when I actually had time.
    So needless to say it will take a while and you can see for yourself how much code actually goes into one tiny mini-game,
    but I think you will get the hang of it if you want to pursue it.  If you do, feel free to ask me anything. :)
                                                                           - Matt
"""

















































