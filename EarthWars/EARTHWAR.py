# -------------------------EARTHWAR-------------------------#
"""Name: EARTHWAR
   Python ver: 2.7
   Author: Innocent M Sakala
   Alias: Xenorm
   Start: 30/10/16 #Finish: 12/11/17
   Email: innocentmsakala@gmail.com"""

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/



import pygame,sys,math,time,random
from pygame.locals import *


clock=pygame.time.Clock(); seconds=0
pygame.mixer.pre_init(44100, 16, 2, 3072) # setup mixer to avoid sound lag
pygame.init()


w = 1200   #screen width
h = 600   #screen height
screen = pygame.display.set_mode((w, h),FULLSCREEN,32) #display screen
pygame.display.set_caption('EARTHWARS by Xenorm 2016')
hero = pygame.image.load("earthwars_resources\heroshipl.png").convert_alpha()
blt= pygame.image.load("earthwars_resources\dong.png").convert_alpha()
background=pygame.image.load("earthwars_resources\deep_space2.jpg").convert()
alien001=pygame.image.load("earthwars_resources\zaragon.png").convert_alpha()
explosiongreen=pygame.image.load("earthwars_resources\explosiondg003.png").convert_alpha()
heroexplode=pygame.image.load("earthwars_resources\explosiondg001.png").convert_alpha()
alien002=pygame.image.load("earthwars_resources\kabaraya.png").convert_alpha()
albomb=pygame.image.load("earthwars_resources\karakena.png").convert_alpha()
albexp=pygame.image.load("earthwars_resources\podibombex.png").convert_alpha()
fbombe=pygame.image.load("earthwars_resources\eshbomb.png").convert_alpha()
fbombe2=pygame.image.load("earthwars_resources\dabomb.png").convert_alpha()
fbexp=pygame.image.load("earthwars_resources\FR_explosion_10.png").convert_alpha()
bosa1=pygame.image.load("earthwars_resources\elaz3.png").convert_alpha()
bsbomb=pygame.image.load("earthwars_resources\lokubom.png").convert_alpha()
thanks=pygame.image.load("earthwars_resources\MyLogosecond.jpg").convert()

mainhero = pygame.transform.scale(hero, (35,35))
bullet=pygame.transform.scale(blt,(5,5))
albombe=pygame.transform.scale(albomb,(15,15))
alien1=pygame.transform.scale(alien001,(45,45))
fighter=pygame.transform.scale(alien002,(25,25))
fbomb1=pygame.transform.scale(fbombe,(8,8))
fbomb2=pygame.transform.scale(fbombe2,(10,10))
fbexplode=pygame.transform.scale(fbexp,(270,270))
bossbomb=pygame.transform.scale(bsbomb,(12,12))
imageturned=hero; myscreen=screen

laserfire=pygame.mixer.Sound("earthwars_resources\LASER1.WAV")
heroexplodesound=pygame.mixer.Sound("earthwars_resources\explosion2.WAV")
alien1explode=pygame.mixer.Sound("earthwars_resources\saucerexplode.WAV")
healthloss=pygame.mixer.Sound("earthwars_resources\sparks.WAV")
fighterexplode=pygame.mixer.Sound("earthwars_resources\smallexp.wav")
fbexs=pygame.mixer.Sound("earthwars_resources\podipipireema.wav")
laserfire.set_volume(0.08); alien1explode.set_volume(0.5)
healthloss.set_volume(0.02); heroexplodesound.set_volume(0.1)
fighterexplode.set_volume(0.4); fbexs.set_volume(0.3)

rotate=90; angle_rad=math.radians(rotate);
score=[0,0,0,0,0,0]#hunthous, tenthous,thous,huns,tens,ones
scorestr=str(score[0])+str(score[1])+str(score[2])+\
           str(score[3])+str(score[4])+str(score[5])
realscore=int(scorestr)
gamespeed=100; gamecounter=0; game_paused=False
kalaya=0
red=[255,0,0]
bossrotate=bosa1
# All Hero info in Hinfo list
# 0-heroexpldsound, 1-x, 2-y, 3-expldx, 4-expldy, 5-resethero, 6-hvel, 7-maxhvel
# 8-hero size, 9-if moving forward True flag, 10-rotatevalue befor w was pressed
#11-newvelocity
Hinfo=[False,(w/2),(h-mainhero.get_width()),0,0,False,0,3,35,False,0,0,4]
vitals=[150,6,225] #health, lives, fade
bullets=[]
aliens1=[]; aliens1limit=25; aliens1delay=0; aliens1delaylimit=35
albombs=[]; albmx=albmy=0
bsbombs=[]
#engineex=[0,0]
fablts=[];fbblts=[]; bombalaunch=bombblaunch=0
smallboss1=[False,0,0,0,0,0,100,0]
smallboss2=[False,0,0,0,0,0,100,0]
bossinfo=[False,0,0,0,0,0,1000]
# event list flags for all event activation
# 0-alien1 1-albom 2-smallboss1 3- smallboss2 4-boss1
eventlist=[False, False, False, False, False]
text="It was in 3145 that Earth was taken fromus by the Kroggs from a distant \
unheard of Galaxy. Now we live in exile on one  of the moons of Jupiter. Over \
the past  few centuries we started rebuilding our lost civilisation and now the \
final     battle is about to begin. The Kroggs arecoming with a new plan to \
annihilate oursun so all life forms on all planets in the solar system will \
be wiped out. It  is your task to defend the Solar System.YOU ARE OUR LAST \
AND ONLY HOPE.........."

smallfiles=[]
sentl=40 # length of a sentence in characters
color=(200,25,200)
intro=True
def makefiles(bigfile,smallfiles):
    a=0;y=h+25
    for i in xrange (len(text)//sentl):
        appendfile=bigfile[a:a+sentl]
        smallfiles.append([appendfile,y+a])
        a+=40                              
    if len(text)%sentl>0:
        x=smallfiles[-1][1]
        x+=40
        smallfiles.append([bigfile[-(len(text)%sentl):-1],x])
    return smallfiles
    
def story_to_screen(textfile):
    font = pygame.font.Font(None,28)
    textpic = font.render(textfile[0], 0, color)
    a=textpic.get_rect()
    screen.blit(textpic,((w-a[2])/2,textfile[1]))# bottom center
    textfile[1]-=2

def game_over():
    for x in xrange(4000):
        screen.blit(thanks,(w/2-(324),50))
        pygame.display.update()
    pygame.quit()
    sys.exit()
    pygame.mouse.set_visible(True)
def update_all(Hinfo):
    update_score(score,scorestr,realscore)
    update_game_text()
    if vitals[0]>0:
        screen.blit(imageturned, (Hinfo[1], Hinfo[2]))
    fighter_bombs(fablts,fbomb1,8,2,5)
    fighter_bombs(fbblts,fbomb2,10,5,0)
    bombs(albombs, albombe,albexp,1.8,15,15,25)
    bombs(bsbombs, bossbomb,albexp,1.1,40,40,50)
    pygame.display.update()
    screen.blit(background,(0,0))   # copy background to screen

def update_score(score,scorestr,realscore):
    if score[5]>=10: score[5]=0; score[4]+=1
    if score[4]>=10: score[4]=0; score[3]+=1
    if score[3]>=10: score[3]=0; score[2]+=1
    if score[2]>=10: score[2]=0; score[1]+=1
    if score[1]>=10: score[1]=0; score[0]+=1
    scorestr=str(score[0])+str(score[1])+\
           str(score[2])+str(score[3])+str(score[4])+str(score[5])
    realscore=int(scorestr)
def update_game_text():
    font = pygame.font.Font(None, 36)
    text = font.render("Score:", 2, red)
    screen.blit(text, [2,0])# print text->score, vitals[1]
    text = font.render(scorestr, 2, red)
    screen.blit(text, [80,1])# print score
    life=pygame.transform.scale(hero,(25,25))
    for i in xrange (vitals[1]):
        screen.blit(life,(w-(25*(i+1)),2))
    pygame.draw.rect(screen, (128,0,0), [2, h-(300), 25,300],4)# vitals[0] bar border
    if vitals[2]<0: vitals[2]=1
    pygame.draw.rect(screen, (255,vitals[2],0), [6, h-vitals[0]*2+4, 19,295],0)# vitals[0] bar

def getAngle(x1,y1,x2,y2):
    # Return value is 0 for right, 90 for up, 180 for left\
    #, and 270 for down (and all values between 0 and 360)
    ydiff = y1 - y2
    xdiff = x1 - x2
    angleinrad = math.atan2(xdiff,ydiff) # get the angle in radians
    angleindeg = math.degrees(angleinrad) # convert to degrees
    return angleindeg, angleinrad

def rot_center(image, angle): # use a square image
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def hero_explode():
    if vitals[0]<=0:
        screen.blit(heroexplode,(Hinfo[1]-32,Hinfo[2]-32)\
                    ,Rect((Hinfo[3], Hinfo[4]),(100,100)))
        Hinfo[3]+=100
        if Hinfo[3]>=600:
            Hinfo[3]=0
            Hinfo[4]+=100
        if Hinfo[4]>=600:
            Hinfo[3], Hinfo[4]=0,0; Hinfo[5]=True; vitals[0]=1; vitals[2]=1
            vitals[1]-=1; Hinfo[6]=0; rotate=90; Hinfo[1],Hinfo[2]=w/2, h-50
            angle_rad=math.radians(rotate)
            imageturned=rot_center(mainhero,rotate)
            Hinfo[0]=True

def explode(i,whoexplds):# i=saucers_list pos, x y=saucer Hinfo[1] poy
    screen.blit(explosiongreen,(whoexplds[i][3]-27,whoexplds[i][4]-27),\
                Rect((whoexplds[i][6],whoexplds[i][7] ),(100,100)))
    whoexplds[i][6]+=100
    if whoexplds[i][6]>=600:
        whoexplds[i][6]=0
        whoexplds[i][7]+=100
    if whoexplds[i][7]>=600:
        whoexplds[i][4]=h+100
        whoexplds[i][0]=True
        whoexplds[i][5]=0
        whoexplds[i][2]=h+100

# USE THE FUNCTION BELOW FOR ALL BOMBS
#hl-vitals[0] loss
def bombs(amolist,image1,image2,firerate,w,h,hl):
    if len(amolist)>0:
        for i in xrange (len(amolist)):
            if amolist[i][0]>0 and amolist[i][6]==False:
                screen.blit(image1,(amolist[i][1],amolist[i][2]))
                amolist[i][1]+=math.cos(amolist[i][3])*constant*firerate
                amolist[i][2]-=math.sin(amolist[i][3])*constant*firerate
                bomb_rect=pygame.Rect(amolist[i][1],amolist[i][2],w,h)
                hero_rect=pygame.Rect(Hinfo[1],Hinfo[2],Hinfo[8], Hinfo[8])
                amolist[i][0]-=1
                if bomb_rect.colliderect(hero_rect):
                    fbexs.play()
                    vitals[0]-=hl
                    vitals[2]-=hl*1.5
                    amolist[i][0]=0
            if amolist[i][0]<=0 and amolist[i][6]==False:
# bomb life over so call explosion routine
                screen.blit(image2,(amolist[i][1]-10,amolist[i][2]-10),\
                            Rect((amolist[i][3],amolist[i][4]),(40,40)))
                amolist[i][4]+=40
                if amolist[i][4]>=280:
                    amolist[i][4]=0
                    amolist[i][5]+=40
                if amolist[i][5]>=80:
                    amolist[i][6]=True
                    amolist[i][1]=w=100 # away from screen area
        if amolist[-1][0]<=0 and amolist[-1][6]==True:
                 amolist.pop()

def shoot(amolist,image,firerate):
    # bullets[i]=[life, x, y, rotation angle] rotation angle inserted at time of
    #               0   1  2      3           bullet creation and adding to list
    if len(amolist)>0:
        for i in xrange (len(amolist)):
            if amolist[i][0]>0:
                amolist[i][1]+=math.cos(amolist[i][3])*constant*firerate
                amolist[i][2]-=math.sin(amolist[i][3])*constant*firerate
                screen.blit(image,(amolist[i][1],amolist[i][2]))
                amolist[i][0]-=1
    
def fighters(whichship,fbulletlist,score):

    screen.blit(fighter, (whichship[1], whichship[2]))
    whichship[1]+=math.cos(math.radians(whichship[2])/math.pi)*(constant)
    whichship[2]-=math.sin(math.radians(-whichship[1])/math.pi*5)*(constant)
    if whichship[1]>=w-fighter.get_width():
        whichship[1]=0
    if whichship<0:
        whichship[1]=w
    hero_rect=pygame.Rect(Hinfo[1],Hinfo[2],Hinfo[8],Hinfo[8])
    fighter_rect=pygame.Rect(whichship[1],whichship[2],25,25)
    if fighter_rect.colliderect(hero_rect):
        vitals[0]-=10
        vitals[2]-=8*1.5
        healthloss.play()
#check if we shot the fighter and reduce vitals[0]
    if len(bullets)>0:
        for i in xrange (len(bullets)):
            bullet_rect=pygame.Rect(bullets[i][1], bullets[i][2],6,6)
            if bullet_rect.colliderect(fighter_rect):
                bullets[i][0]=0
                whichship[6]-=1
                score[4]+=1 #tens
#make the fighter bombs ready for launch
    if whichship[6]>=0:
        if len(fbulletlist)<=100:
            if whichship[5]>=random.randrange(8,15):
                fbulletlist.insert(0,[500,whichship[1],whichship[2],0,0,0,0,False])
                whichship[5]=0
    if whichship[6]<=0:
        whichship[0]=False
        whichship[6]=100
        whichship[7]=0
    whichship[5]+=1

def fighter_bombs(fblist,spritelist, size,score1,score2):
    global w
#launch the small bombs which home in on the hero
    if len(fblist)>0:
        for i in xrange(len(fblist)):
            if fblist[i][0]>0:
                x=Hinfo[1]-fblist[i][1]; y=Hinfo[2]-fblist[i][2]
                fblist[i][1]+=math.cos(math.atan2 (y,x))*(constant/1.6)*2
                fblist[i][2]+=math.sin(math.atan2 (y,x))*(constant/1.6)*2
                screen.blit(spritelist,(fblist[i][1], fblist[i][2]))
                bomb_rect=pygame.Rect(fblist[i][1], fblist[i][2],size, size)
                hero_rect=pygame.Rect(Hinfo[1],Hinfo[2],Hinfo[8],Hinfo[8])
                fblist[i][0]-=1
                if bomb_rect.colliderect(hero_rect):
                    vitals[0]-=25
                    vitals[2]-=25*1.5
                    fblist[i][0]=0
                    fbexs.play()
                    fblist[i][3]=fblist[i][1]# put current x here for explosion
                    fblist[i][4]=fblist[i][2]# put current y here for explosion
                    fblist[i][1]=w+100 # move bomb away from screen

            fb_rect=pygame.Rect(fblist[i][1], fblist[i][2], 10,10)
            for j in xrange (len(bullets)):
                bullet_rect=pygame.Rect(bullets[j][1], bullets[j][2],6,6)
                if bullet_rect.colliderect(fb_rect):
                    fbexs.play()
                    fblist[i][3]=fblist[i][1]# put current x here for explosion
                    fblist[i][4]=fblist[i][2]# put current y here for explosion
                    fblist[i][1]=w+100 # move bomb away from screen
                    score[4]+=1
                    fblist[i][0]=0
                    bullets[j][0]=0
                    fblist[i][7]=True
                    
            if fblist[i][0]<=0:
                screen.blit(fbexplode,(fblist[i][3]-5,fblist[i][4]-5),\
                        Rect((fblist[i][5],fblist[i][6]),(45,45)))
                fblist[i][5]+=45
                if fblist[i][5]>=270:
                    fblist[i][5]=0
                    fblist[i][6]+=45
                if fblist[i][6]>=270:
                    fblist[i][7]=True
                    
#remove the used bomb from the list
        if fblist[-1][7]==True:
            fblist.pop()

imageturned=rot_center(mainhero,rotate)
m=makefiles(text,smallfiles)# this is the text file broken into segments
num=len(smallfiles) # this is the number of lines we to print to the screen
pygame.mouse.set_visible(False)
while True:#------------------------ Main Game Loop----------------------#
    while intro==True:
        pygame.event.pump()
        keys=pygame.key.get_pressed()       #get key pressed
        if keys[pygame.K_q]: #PAUSE GAME
            intro=False
        for i in xrange(len(smallfiles)):
            story_to_screen(smallfiles[i])
            if smallfiles[len(smallfiles)-1][1]<-50:
                intro=False       
        pygame.display.update()
        screen.blit(background,(0,0))
    
    timegone=clock.tick(40)
    timegone_sec=timegone/1000.0
    constant=gamespeed*timegone_sec
    scorestr=str(score[0])+str(score[1])+str(score[2])\
               +str(score[3])+str(score[4])+str(score[5])
    realscore=int(scorestr)
    smallboss1[7]+=.5
    smallboss2[7]+=.5

    kalaya+=timegone_sec
    seconds=int(kalaya)
    gamecounter+=1
    if realscore>2000 and score <4000:
        aliens1delaylimit=40
    vitals[0]+=0.05 # hero auto healing function
    vitals[2]+=0.05*1.5
    if vitals[0]==150:
        vitals[0]=150
        vitals[2]=225
# set the eventlist flags to trigger events happening
    if gamecounter==50:
        eventlist[0]=True # bring on the aliens##    if realscore> 2000:

    if realscore>= 2000:
        eventlist[1]=True # bring on the albombs
        aliens1limit=60
        aliens1delaylimit=25
        
    if realscore>= 4000 and realscore <=10000:
        eventlist[2]=True # bring on the smallboss1
        eventlist[1]=False# stop the albombs
        eventlist[0]=False# stop the aliens
        eventlist[3]=False
        eventlist[4]=False
        bossinfo[0]=False
        
    if realscore>= 6000 and realscore <=10000:
        eventlist[3]=True # bring on the smallboss2
        eventlist[0]=False# stop the aliens1
        eventlist[1]=False# stop the albombs
        eventlist[4]=False
        bossinfo[0]=False
         
    if realscore>= 8000 and realscore <=10000: # bring the alien ships and albombs
        eventlist[0]=True# bring the aliens1
        eventlist[1]=True# bring the albombs
        eventlist[4]=False
        bossinfo[0]=False
         
    if realscore>= 10000:
        eventlist[4]=True# bring on the BAD BOSS1
        eventlist[3]=False# stop the smallboss2
        eventlist[2]=False# stop the smallboss1
        eventlist[1]=False# stop the aliens1
        eventlist[0]=False# stop the albombs
        smallboss1[0]=False
        smallboss2[0]=False
        
    if eventlist[2]==True and smallboss1[0]==False:
        smallboss1[0]=True
        smallboss1[1]=random.randint(w/2, w-w/3)
        smallboss1[2]=random.randint(h/3, h-h/3)
    if smallboss1[0] is True and smallboss1[7]>50:
        fighters(smallboss1,fablts,score)

    if eventlist[3]==True and smallboss2[0]==False:
        smallboss2[0]=True
        smallboss2[1]=random.randint(w/3, w/2)
        smallboss2[2]=random.randint(h/3, h-h/3)
    if smallboss2[0] is True and smallboss2[7]>90:
        fighters(smallboss2,fbblts,score)

    pygame.event.pump()
    keys=pygame.key.get_pressed()       #get key pressed
    if (keys[pygame.K_ESCAPE]): # exit game
        game_over()
    for event in pygame.event.get():
        if event.type==QUIT:
            game_over()

# move hero
    if vitals[0]<=0:
        if Hinfo[0]==True:
            heroexplodesound.play()
            Hinfo[0]=False
        hero_explode()
    if Hinfo[5]==True:
        vitals[0]+=5
        vitals[2]+=5*1.5
    if vitals[0]>=150: # max health
        vitals[0]=150
        vitals[2]=225 # colour fade amount
        Hinfo[5]=False
    if vitals[0]>0:
        if (keys[pygame.K_a])or (keys[pygame.K_LEFT]):#rotate left
            rotate+=4
        if (keys[pygame.K_d])or (keys[pygame.K_RIGHT]):#rotate right
            rotate-=4
        if (keys[pygame.K_w])or (keys[pygame.K_UP]):#accellerate (to max velocity) and move forward
            Hinfo[9]=True
            Hinfo[6]+=.01
            if Hinfo[6]>=Hinfo[7]:
                Hinfo[6]=Hinfo[7]
            Hinfo[11]+=Hinfo[6]
            if Hinfo[11]>=Hinfo[12]:
                Hinfo[11]=Hinfo[12]
        else:
            Hinfo[9]=False
            Hinfo[6]-=.01
            Hinfo[6]<=0
            Hinfo[6]=0
            Hinfo[11]-=.04
            if Hinfo[11]<0:
                Hinfo[11]=0
        if (keys[pygame.K_s])or (keys[pygame.K_DOWN]):#reverse
            Hinfo[11]-=.01
            if Hinfo[11]<=0:
                Hinfo[11]=0
        imageturned=rot_center(mainhero,rotate)
        if Hinfo[9]==True:
            Hinfo[10]=rotate

        angle_rad=math.radians(Hinfo[10])
        Hinfo[1]+=Hinfo[11]*math.cos(angle_rad)*(constant)
        Hinfo[2]-=Hinfo[11]*math.sin(angle_rad)*(constant)
        angle=math.radians(rotate)
        if Hinfo[2]>h:
            Hinfo[2]=0-hero.get_height()
        if Hinfo[2]<0-hero.get_height():
            Hinfo[2]=h
        if Hinfo[1]<0-hero.get_width():
            Hinfo[1]=w
        if Hinfo[1]>w:
            Hinfo[1]=0-hero.get_width()
# put a bullet in the list if spacebar pressed
    if gamecounter%3==0:# slows down adding bullets so slows down firing
        if (keys[pygame.K_SPACE]) and vitals[0]>0:
            bltx=(Hinfo[1]-3)+mainhero.get_width()/2
            blty=(Hinfo[2]-3)+mainhero.get_height()/2
            bltangle=math.radians(rotate)
            bltlife=25
            bullets.insert(0,[bltlife,bltx, blty,bltangle, False])
            laserfire.play()
# if bullet list not empty then shoot!
    if len(bullets)>0:
        shoot(bullets, bullet,4)
        for i in xrange (len(bullets)):
            if bullets[i][0]>0:
                bullet_rect=pygame.Rect(bullets[i][1],bullets[i][2],6,6)
# check for collision with boss1
                if bossinfo[0]==True:
                    boss1_rect=pygame.Rect(bossinfo[1], bossinfo[2],90,90)
                    if bullet_rect.colliderect(boss1_rect):
                        score[5]+=1 # ones
                        score[4]+=1 # tens
                        bossinfo[6]-=.5
# check if any bullet hits any alien
                if len (aliens1)>0:
                    for j in xrange (len(aliens1)):
                        if aliens1[j][5]>0:
                            alien1_rect=pygame.Rect(aliens1[j][1]\
                                                    , aliens1[j][2],45,45)
                            if bullet_rect.colliderect(alien1_rect):
                                bullets[i][0]=0
                                aliens1[j][5]-=8
                                score[5]+=1
# if alien life 0 take out of screen and prepare for explosion
                        if aliens1[j][5]<=0 and aliens1[j][0]==True:
                            alien1explode.play()
                            score[3]+=1
                            aliens1[j][0]=False
                            aliens1[j][3]=aliens1[j][1] # get the last Hinfo[1] and
                            aliens1[j][4]=aliens1[j][2] # Hinfo[2] of expld alien and
                            aliens1[j][1]=w+100 # move alien out of screen x
                            aliens1[j][5]=0

    if len(bullets)>0 and bullets[-1][0]<=0:#bullet life over so remove from list
        bullets.pop()

# if conditions correct add alien to list
    if eventlist[0]==True:
        aliens1delay+=1

    if gamecounter>75 and len(aliens1)<=aliens1limit \
       and aliens1delay==aliens1delaylimit:
        aliens1.insert(0,[True,random.randint(0,(w-60)),-60,0, 0,100,0,0,0])
        #                  0    1                         2 3  4  5  6 7 8
    if len(aliens1)>0:
        for i in xrange(len(aliens1)):
            if eventlist[1]==True: # shoot bombs if score if higher than this
                bombcorridor=pygame.Rect(aliens1[i][1],aliens1[i][2]+ 60,60,300)
                hero_rect=pygame.Rect(Hinfo[1],Hinfo[2]\
                                      ,Hinfo[8],Hinfo[8])
                if bombcorridor.colliderect(hero_rect) and aliens1[i][6]<30:
                    aliens1[i][6]+=1
                    if aliens1[i][6]==3:# albomb shoot delay flag
                        aliens1[i][6]=-30
                        rotinfo=getAngle(aliens1[i][1],aliens1[i][2]\
                                         ,aliens1[i][1],Hinfo[2])
                        abx=aliens1[i][1]+18
                        aby=aliens1[i][2]+60
                        angle=math.radians(rotinfo[0]-90); life=40
                        albombs.insert(0,[life,abx,aby,-angle,0,0,False])

            if aliens1[i][2]<h and aliens1[i][5]>=0:
                screen.blit(alien1,(aliens1[i][1], aliens1[i][2]))
                aliens1[i][2]+=(constant*.5)

# if hero collides with alien1 reduce vitals[0]
                alien1_rect=pygame.Rect(aliens1[i][1], aliens1[i][2],60,60)
                hero_rect=pygame.Rect(Hinfo[1],Hinfo[2]\
                                      ,Hinfo[8],Hinfo[8])
                if alien1_rect.colliderect(hero_rect):
                    vitals[0]-=2
                    vitals[2]-=2*1.5
                    healthloss.play()

            if aliens1[i][2]<h and aliens1[i][5]<=0 and aliens1[i][0]==False:
                explode(i, aliens1)

            if aliens1[i][2]>=h and aliens1[i][0]==True:
                aliens1[i][0]=False
                aliens1[i][5]=0

    if len (aliens1)>0 and aliens1[-1][2]>=h and aliens1[-1][5]==0:
        aliens1.pop()
    if aliens1delay>aliens1delaylimit:
        aliens1delay=0

#-------------------------------------------------------#
#               THE FIRST ALIEN BAD BOSS                #
#-------------------------------------------------------#
    if eventlist[4]==True and bossinfo[0]==False:
        bossinfo[0]=True; bossinfo[1]=0-50-bosa1.get_width()/2; bossinfo[2]=h/2
    if bossinfo[0]==True:
        rotinfo=getAngle(bossinfo[1], bossinfo[2],Hinfo[1],Hinfo[2])
        bossangle=rotinfo[0]
        bossrad=rotinfo[1]
        bossrotate=rot_center(bosa1,bossangle)
        bossinfo[1]+=math.cos(bossangle)*constant*.5
        bossinfo[2]-=math.sin(bossangle)*constant*.5
        bossinfo[5]+=1
        if bossinfo[5]==25:# bossbomb shoot delay flag
            bossinfo[5]=-60
            abx=bossinfo[1]
            aby=bossinfo[2]
            bsbangle=math.radians(bossangle+90)
            bsblife=80
            bsbombs.insert(0,[bsblife,abx,aby,bsbangle,0,0,False])
        screen.blit(bossrotate,(bossinfo[1]-35,bossinfo[2]-35))
        # draw the boss energy level bar above boss and reduce if hit
        pygame.draw.rect(screen,(255,255,255),[bossinfo[1]-38\
                                           ,bossinfo[2]-38,103,10],2)
        pygame.draw.rect(screen,(255,0,0),[bossinfo[1]-35\
                                           ,bossinfo[2]-35,bossinfo[6]/10,6],0)

    update_all(Hinfo)

################################################################################

    if keys[pygame.K_p]: #PAUSE GAME
        pygame.image.save(screen,"earthwars_resources\myscreen.jpeg")
        myscreen=pygame.image.load("earthwars_resources\myscreen.jpeg").convert()
        game_paused=True
    if keys[pygame.K_h]: # cheat to increase vitals[0] to max anytime
        vitals[0]=150
        vitals[2]=225



#################### G A  M  E    P A U S E ####################
    while game_paused==True:
        font = pygame.font.Font(None, 100)
        a=random.randrange(0, 255)
        b=random.randrange(0,1)
        c=random.randrange(0,1)
        text = font.render("Paused.", 1, [a,b,c])
        textpos = text.get_rect()
        screen.blit(text,(w/2-(textpos[2]/2),h/2-textpos[3]/2))
        font = pygame.font.Font(None, 40)
        text = font.render("Hit SPACE to continue", 1, red)
        textpos = text.get_rect()
        screen.blit(text,(w/2-(textpos[2]/2),h/2+textpos[3]))
        update_all(Hinfo)
        screen.blit(myscreen,(0,0))
        pygame.event.pump()
        key=pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
                game_paused=False

#################### G A  M  E    O  V  E  R ####################
#                         replay or quit
    while vitals[1]<=0 or bossinfo[6]<=0:
        font = pygame.font.Font(None, 50)
        if bossinfo[6]<=0:
            akuru="YOU WON THE WAR! YOU ARE A HERO!'"
        else:
            akuru="THE WAR WAS LOST!"
        text = font.render(akuru, 1, red)
        textpos = text.get_rect()
        screen.blit(text,(w/2-(textpos[2]/2),h/2-textpos[3]/2))
        font = pygame.font.Font(None, 30)
        text = font.render("Hit ESC to Quit!", 1, red)
        textpos = text.get_rect()
        screen.blit(text,(w/2-(textpos[2]/2),h/2+textpos[3]))
        text = font.render("Hit r to try again", 1, red)
        textpos = text.get_rect()
        screen.blit(text,(w/2-(textpos[2]/2),360))
        update_all(Hinfo)
        screen.blit(myscreen,(0,0))
        pygame.event.pump()
        key=pygame.key.get_pressed()
        if key[pygame.K_r]:
            rotate=90; angle_rad=math.radians(rotate);
            score=[0,0,0,0,0,0]
            scorestr=str(score[0])+str(score[1])+str(score[2])+\
                       str(score[3])+str(score[4])+str(score[5])
            realscore=int(scorestr)
            gamespeed=150; gamecounter=0; game_paused=False
            red=[255,0,0]; kalaya=0
            bossrotate=bosa1
            Hinfo=[False,(w/2),(h-mainhero.get_width()),0,0,False,0,3,35,False,0,0,4,False]
            vitals=[150,5,225]
            bullets=[]
            aliens1=[]; aliens1limit=25; aliens1delay=0; aliens1delaylimit=35
            albombs=[]; albmx=albmy=0
            bsbombs=[]
            fablts=[];fbblts=[]; bombalaunch=bombblaunch=0
            smallboss1=[False,0,0,0,0,0,100,0]
            smallboss2=[False,0,0,0,0,0,100,0]
            bossinfo=[False,0,0,0,0,0,1000]
            eventlist=[False, False, False, False, False]
            angle_rad=math.radians(rotate)
            imageturned=rot_center(mainhero,rotate)
        if key[pygame.K_ESCAPE]:
            game_over()

