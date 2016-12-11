#import statsmodels.api as sm
#import pandas
#from patsy import dmatrices
from Functions import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from numpy import *
import sys, os
import math
sys.path.append("Data")
if sys.platform == 'win32':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
import GL, Objects
import copy

pygame.init()

font = pygame.font.SysFont("Times New Roman", 72, True, True)
pygame.display.set_caption('Pente - v.4.0.0 - Ian Mallett - 2007')
surface = pygame.display.set_mode((800,640),OPENGL|DOUBLEBUF)
GL.resize((800,640))
GL.init()
Textures = glGenTextures(8)
Objects.main(Textures)

view_angle_x = 90.0
view_angle_y = 0.0
view_distance = 1.0

pieces = []
last_white_piece_played = [None,None]
last_black_piece_played = [None,None]
white_pieces_captured = 0
black_pieces_captured = 0

cursor_pos = [0.0, 0.0, 0.0] #x, y, z
mouse_pressing = False
player_turn = "Black"

#[1s,2s,3s,4s,5s,captures]
w = 2
h = 6
bwCount = [[0 for x in range(h)] for y in range(w)]

array = zeros((19,19)) #0 = nothing, 1 = white, 2 = black

weights = []



def evaluationFunction(player,array):
    global weights
    bwCount = detectAB(array)
    #if bwCount[0][5] > 0 or bwCount[1][5] > 0:
     #   print bwCount
    #non = 0.0
    score = 0
    # if player == 1:
    #     non = 2
    # else:
    #     non = 1
    # if player == 1:
    #     for x in range(0,5):
    #         score += bwCount[0][x]*weights[x+1] - bwCount[1][x]*weights[x+7] + weights[0]
    # else:
    #     for x in range(0,5):
    #         score += bwCount[1][x]*weights[x+7] - bwCount[0][x]*weights[x+1] + weights[0]

    
    # if player == 1:
    #     for x in range(0,5):
    #         score += bwCount[0][x]*random.random() - bwCount[1][x]*random.random() + random.random()
    # else:
    #     for x in range(0,5):
    #         score += bwCount[1][x]*random.random() - bwCount[0][x]*random.random() + random.random()

    
    # for x in range(0,5):
    #     score += bwCount[1][x]*weights[x+6] - bwCount[0][x]*weights[x+1]
    # score += weights[0]

    # if player != 1:
    #     score = 1 - score

    est = 0
    #print weights
    for x in range(0,3):
        #print x
        est += bwCount[1][x]*weights[x+3] + bwCount[0][x]*weights[x]
        
        #print bwCount[1][x],weights[x+4],bwCount[0][x], weights[x]
        #print bwCount[1][x]*weights[x+4] - bwCount[0][x]*weights[x]
    #print weights[8]
    est += weights[6]
    #print "est: ",est
    est = est * -1
    score = 1 / (1 + math.exp(est))
    if player == 1:
        score = 1 - score
    
    
    return score


def generateSuccessor(player, action, gameState):
    global last_white_piece_played, last_black_piece_played 
    
    
    temp = copy.deepcopy(gameState)
    #print temp
    #print action
    temp[action] = player
    if player == 1:
        last_white_piece_played = [action[0]+1,action[1]+1]
    else:
        last_black_piece_played = [action[0]+1,action[1]+1]
    return temp




def minimax(gameState,player):
    global bwCount
    depth = 1
    bestMove = []
    hScore = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    actions = getLegalActions(player,gameState)
    successor = []
    #print "Game"
    #print gameState
    #print "Successor"
    #succesor = generateSuccessor(player,(1,1),gameState)
    #print succesor
    for action in actions:
        #print "action: ", action
        successor = generateSuccessor(player,action,gameState)
        #print last_black_piece_played
        #print last_white_piece_played
        
        #print successor
        nplayer = 0.0
        if player == 1:
            nplayer = 2
        else:
            nplayer = 1
        score = MinValueAB(nplayer, depth, successor,alpha,beta)
        #print score
        if (score > hScore):
            hScore = score
            bestMove = action
        if hScore >= beta:
            #print "Max"
            return bestMove
        alpha = max(hScore, alpha)
    #print bestMove
    return bestMove


def MaxValueAB(player,depth,gameState,alpha,beta):
    global bwCount
    if depth <=0 or bwCount[0][4] > 0 or bwCount[1][4] > 0:
        return evaluationFunction(player,gameState)

    hScore = float("-inf")

    actions = getLegalActions(player,gameState)

    for action in actions:
        successor = generateSuccessor(player,action,gameState)
        nplayer = 0
        if player == 1:
            nplayer = 2
        else:
            nplayer = 1
            
        score = MinValueAB(nplayer,depth,successor,alpha,beta)

        hScore = max(hScore,score)
        if hScore >= beta:
            #print "Max"
            return hScore
        alpha = max(alpha,hScore)

    return hScore

def MinValueAB(player,depth,gameState,alpha,beta):

    lScore = float("inf")

    nplayer = 0.0
    if player == 1:
        nplayer = 2
    else:
        nplayer = 1
    actions = getLegalActions(player,gameState)

    for action in actions:
        successor = generateSuccessor(player,action,gameState)
        score = MaxValueAB(nplayer,(depth - 1),successor,alpha,beta)
        lScore = min(score,lScore)
        if lScore <= alpha:
            #print "Min"
            return lScore
        beta = min(beta,lScore)

    #if lScore == float("inf"):
     #   lScore = evaluationFunction(player,gameState)
    return lScore


def get_ComInput(array):
    global last_white_piece_played, last_black_piece_played, player_turn

   # for event in pygame.event.get():
    #    if event.type == QUIT or keystate[K_ESCAPE]:
     #       pygame.quit();  sys.exit()
    #print array
    temp = array
    if player_turn == "White":
        action = minimax(temp,1)
        #print "White"
        
        array[action[0],action[1]] = 1.0
        #print array
        #last_white_piece_played = [action[0]+1,action[1]+1]
        player_turn = "Black"
    else:
        action = minimax(temp,2)
        #print array
        #print "Black"
        array[action[0],action[1]] = 2.0
        #print array
        #last_black_piece_played = [action[0]+1,action[1]+1]
        player_turn = "White"
    #print array
    #print last_white_piece_played
    #print last_black_piece_played
    return array

    
    

# def load_info():
#     captured_white_surface = font.render("Black has captured " + str(white_pieces_captured/2) + "/5 pairs of White's pieces.", True, (255,255,255))
#     captured_black_surface = font.render("White has captured " + str(black_pieces_captured/2) + "/5 pairs of Black's pieces.", True, (255,255,255))
#     captured_white_surface_data = pygame.image.tostring(captured_white_surface, "RGBA", 1)
#     captured_black_surface_data = pygame.image.tostring(captured_black_surface, "RGBA", 1)
#     glBindTexture(GL_TEXTURE_2D, Textures[5]) #captured_white_surface
#     glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, captured_white_surface.get_width(), captured_white_surface.get_height(), 0,
#                   GL_RGBA, GL_UNSIGNED_BYTE, captured_white_surface_data )
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
#     glBindTexture(GL_TEXTURE_2D, Textures[6]) #captured_black_surface
#     glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, captured_black_surface.get_width(), captured_black_surface.get_height(), 0,
#                   GL_RGBA, GL_UNSIGNED_BYTE, captured_black_surface_data )
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
# load_info()


def draw(array):
    #CLEAR ALL----------------------------------------
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #BASIC CAMERA VIEW--------------------------------
    glTranslatef(0.0, 0.0, -51.0*view_distance)
    glRotatef(view_angle_x, 1.0, 0.0, 0.0)
    glRotatef(view_angle_y, 0.0, 1.0, 0.0)
    #BOARD--------------------------------------------
    glCallList(1)
    #PIECES-------------------------------------------
    zpos = -9
    for z in array:
        xpos = -9
        for x in array:
            on = array[zpos+9-1,xpos+9-1]
            if on != 0.0:
                glPushMatrix()
                glTranslatef(xpos*2.10176, 0.25, zpos*2.10176)
                if on == 1.0:  glCallList(2)
                elif on == 2.0:  glCallList(3)
                glPopMatrix()
            xpos += 1
        zpos += 1
    #CURSOR-------------------------------------------
    glPushMatrix()
    glTranslatef(round(cursor_pos[0]/2.10176)*2.10176, cursor_pos[1], round(cursor_pos[2]/2.10176)*2.10176)
    glCallList(4)
    glPopMatrix()
    #HUD----------------------------------------------
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(-0.255, 0.194, -0.5)
    glBindTexture(GL_TEXTURE_2D, Textures[5])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(0.0,  0.0,  0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.18, 0.0,  0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.18, 0.01, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  0.01, 0.0)
    glEnd();
    glTranslatef(0.0, -0.01, 0.0)
    glBindTexture(GL_TEXTURE_2D, Textures[6])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(0.0,  0.0,  0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.18, 0.0,  0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.18, 0.01, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.0,  0.01, 0.0)
    glEnd();

    glDisable(GL_TEXTURE_2D)
    glColor4f(0.5,0.5,0.5,0.5)

    glBegin(GL_QUADS)
    glVertex3f(-0.001, -0.0015, 0.0)
    glVertex3f( 0.181, -0.0015, 0.0)
    glVertex3f( 0.181,  0.02, 0.0)
    glVertex3f(-0.001,  0.02, 0.0)
    glEnd();
    
    glColor4f(1.0,1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)

    glPopMatrix()
    #DRAW TO SCREEN-----------------------------------
    pygame.display.flip()

#def get_input_from_AI():



def get_input(array):
    global view_angle_x, view_angle_y, view_distance, cursor_pos, player_turn, mouse_pressing, last_white_piece_played, last_black_piece_played
    keystate = pygame.key.get_pressed()
    m_pos = pygame.mouse.get_pos()
    m_press = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit();  sys.exit()
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    winX = m_pos[0]
    winY = float(viewport[3]) - m_pos[1]
    winZ = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    posX, posY, posZ = gluUnProject(winX, winY, winZ, modelview, projection, viewport)
    cursor_pos = [posX, 0.01, posZ]
    if cursor_pos[0] < -19:  cursor_pos[0] = -19
    elif cursor_pos[0] > 19:  cursor_pos[0] = 19
    if cursor_pos[2] < -19:  cursor_pos[2] = -19
    elif cursor_pos[2] > 19:  cursor_pos[2] = 19
    if m_press[0]:
        if not mouse_pressing:
            mouse_pressing = True
            if array[round(cursor_pos[2]/2.10176)+9-1,round(cursor_pos[0]/2.10176)+9-1] == 0.0:
                if player_turn == "White":
                    array[round(cursor_pos[2]/2.10176)+9-1,round(cursor_pos[0]/2.10176)+9-1] = 1
                    last_white_piece_played = [round(cursor_pos[0]/2.10176)+9,round(cursor_pos[2]/2.10176)+9]
                    player_turn = "Black"
                else:
                    array[round(cursor_pos[2]/2.10176)+9-1,round(cursor_pos[0]/2.10176)+9-1] = 2
                    last_black_piece_played = [round(cursor_pos[0]/2.10176)+9,round(cursor_pos[2]/2.10176)+9]
                    player_turn = "White"
    else:  mouse_pressing = False
    if keystate[K_UP] and view_angle_x < 90:  view_angle_x += 1.0
    if keystate[K_DOWN] and view_angle_x > 0:  view_angle_x -= 1.0
    if keystate[K_LEFT]:  view_angle_y += 1.0
    if keystate[K_RIGHT]:  view_angle_y -= 1.0
    if keystate[K_PAGEUP] and view_distance < 2.0:  view_distance += .03
    if keystate[K_PAGEDOWN] and view_distance > 0.5:  view_distance -= .03
    if keystate[K_END]:  view_distance = 1.0;  view_angle_y = 0.0;  view_angle_x = 90.0
    return array



def detectAB(array):
    global last_white_piece_played, last_black_piece_played, black_pieces_captured, white_pieces_captured

    White_pieces_captured = 0
    Black_pieces_captured = 0
    
    #print last_black_piece_played
    
    #print last_white_piece_played
    
    w = 2
    h = 6
    bwCount = [[0 for x in range(h)] for y in range(w)]
    
    for y in range(0,5):
        bwCount[0][y] = 0
        bwCount[1][y] = 0
    zpos = -9
    for z in array:
        xpos = -9
        for x in array:
            on = array[zpos+9-1,xpos+9-1]
            #print zpos+9-1,xpos+9-1
            c = int(on) - 1
            if on != 0.0:
                #In a column
                if array[zpos+9-1-1,xpos+9-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1-2,xpos+9-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1-3,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1-4,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1-5,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                                elif array[zpos+9-1-0,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                            elif array[zpos+9-1-0,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+1,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                        elif array[zpos+9-1-0,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+1,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+2,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                    elif array[zpos+9-1-0,xpos+9-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+1,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+2,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+3,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                elif array[zpos+9-1-0,xpos+9-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1+1,xpos+9-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+2,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+3,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+4,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                #In a row
                if array[zpos+9-1,xpos+9-1-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1,xpos+9-1-2] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1,xpos+9-1-3] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1-4] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1-5] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                                elif array[zpos+9-1,xpos+9-1-0] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                            elif array[zpos+9-1,xpos+9-1-0] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1+1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                        elif array[zpos+9-1,xpos+9-1-0] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1+1] == on:
                                bwCount[c][3] += 1
                                #print "zpos: ", zpos+9-1
                                #print "xpos: ", xpos+9+2
                                #print "on: ", on
                                if array[zpos+9-1,xpos+9+2] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                    elif array[zpos+9-1,xpos+9-1-0] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1,xpos+9-1+1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1+2] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1+3] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                elif array[zpos+9-1,xpos+9-1-0] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1,xpos+9-1+1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1,xpos+9-1+2] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1+3] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1+4] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                #Diagonal w/ - slope
                if array[zpos+9-1-1,xpos+9-1-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1-2,xpos+9-1-2] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1-3,xpos+9-1-3] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1-4,xpos+9-1-4] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1-5,xpos+9-1-5] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                                elif array[zpos+9-1-0,xpos+9-1-0] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                            elif array[zpos+9-1-0,xpos+9-1-0] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+1,xpos+9-1+1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                        elif array[zpos+9-1-0,xpos+9-1-0] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+1,xpos+9-1+1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+2,xpos+9-1+2] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                    elif array[zpos+9-1-0,xpos+9-1-0] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+1,xpos+9-1+1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+2,xpos+9-1+2] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+3,xpos+9-1+3] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                elif array[zpos+9-1-0,xpos+9-1-0] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1+1,xpos+9-1+1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+2,xpos+9-1+2] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+3,xpos+9-1+3] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+4,xpos+9-1+4] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                #Diagonal w/ + slope
                if array[zpos+9-1-1,xpos+9-1+1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1-2,xpos+9-1+2] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1-3,xpos+9-1+3] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1-4,xpos+9-1+4] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1-5,xpos+9-1+5] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                                elif array[zpos+9-1-0,xpos+9-1+0] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                            elif array[zpos+9-1-0,xpos+9-1+0] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+1,xpos+9-1-1] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                        elif array[zpos+9-1-0,xpos+9-1+0] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+1,xpos+9-1-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+2,xpos+9-1-2] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                    elif array[zpos+9-1-0,xpos+9-1+0] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+1,xpos+9-1-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+2,xpos+9-1-2] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+3,xpos+9-1-3] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                elif array[zpos+9-1-0,xpos+9-1+0] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1+1,xpos+9-1-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+2,xpos+9-1-2] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+3,xpos+9-1-3] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+4,xpos+9-1-4] == on:
                                    bwCount[c][4] += 1
                                    #we_have_a_winner(on)
                #Capture
                # if ((([xpos+9,zpos+9] == last_white_piece_played) and (on == 1.0)) or (([xpos+9,zpos+9] == last_black_piece_played) and (on == 2.0))):
                #     opposite_of_on = (1.0-(on-1.0))+1.0
                #     #Down
                #     if array[zpos+9-1-1,xpos+9-1] == opposite_of_on:
                #         if array[zpos+9-1-2,xpos+9-1] == opposite_of_on:
                #             if array[zpos+9-1-3,xpos+9-1] == on:
                #                 array[zpos+9-1-1,xpos+9-1] = 0.0
                #                 array[zpos+9-1-2,xpos+9-1] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     #Right
                #     if array[zpos+9-1,xpos+9-1-1] == opposite_of_on:
                #         if array[zpos+9-1,xpos+9-1-2] == opposite_of_on:
                #             if array[zpos+9-1,xpos+9-1-3] == on:
                #                 array[zpos+9-1,xpos+9-1-1] = 0.0
                #                 array[zpos+9-1,xpos+9-1-2] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     #Up
                #     if array[zpos+9-1+1,xpos+9-1] == opposite_of_on:
                #         if array[zpos+9-1+2,xpos+9-1] == opposite_of_on:
                #             if array[zpos+9-1+3,xpos+9-1] == on:
                #                 array[zpos+9-1+1,xpos+9-1] = 0.0
                #                 array[zpos+9-1+2,xpos+9-1] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     #Left
                #     if array[zpos+9-1,xpos+9-1+1] == opposite_of_on:
                #         if array[zpos+9-1,xpos+9-1+2] == opposite_of_on:
                #             if array[zpos+9-1,xpos+9-1+3] == on:
                #                 array[zpos+9-1,xpos+9-1+1] = 0.0
                #                 array[zpos+9-1,xpos+9-1+2] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     #Right Up Diagonal
                #     if array[zpos+9-1+1,xpos+9-1-1] == opposite_of_on:
                #         if array[zpos+9-1+2,xpos+9-1-2] == opposite_of_on:
                #             if array[zpos+9-1+3,xpos+9-1-3] == on:
                #                 array[zpos+9-1+1,xpos+9-1-1] = 0.0
                #                 array[zpos+9-1+2,xpos+9-1-2] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     #Left Down Diagonal
                #     if array[zpos+9-1-1,xpos+9-1+1] == opposite_of_on:
                #         if array[zpos+9-1-2,xpos+9-1+2] == opposite_of_on:
                #             if array[zpos+9-1-3,xpos+9-1+3] == on:
                #                 array[zpos+9-1-1,xpos+9-1+1] = 0.0
                #                 array[zpos+9-1-2,xpos+9-1+2] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     #Left Up Diagonal
                #     if array[zpos+9-1+1,xpos+9-1+1] == opposite_of_on:
                #         if array[zpos+9-1+2,xpos+9-1+2] == opposite_of_on:
                #             if array[zpos+9-1+3,xpos+9-1+3] == on:
                #                 array[zpos+9-1+1,xpos+9-1+1] = 0.0
                #                 array[zpos+9-1+2,xpos+9-1+2] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     #Right Down Diagonal
                #     if array[zpos+9-1-1,xpos+9-1-1] == opposite_of_on:
                #         if array[zpos+9-1-2,xpos+9-1-2] == opposite_of_on:
                #             if array[zpos+9-1-3,xpos+9-1-3] == on:
                #                 array[zpos+9-1-1,xpos+9-1-1] = 0.0
                #                 array[zpos+9-1-2,xpos+9-1-2] = 0.0
                #                 if on == 1.0:  Black_pieces_captured += 2
                #                 else:  White_pieces_captured += 2
                #                 load_info()
                #     if on == 1.0:  last_white_piece_played = [None,None]
                #     else:  last_black_piece_played = [None,None]
            xpos += 1
        zpos += 1
    #bwCount[1][5] = white_pieces_captured
    #bwCount[0][5] = black_pieces_captured
    #if white_pieces_captured == 10:  #we_have_a_winner(2.0)
    #if black_pieces_captured == 10:  #we_have_a_winner(1.0)
    #bwCount[0][0] = bwCount[0][0] / 4
    #bwCount[1][0] = bwCount[1][0] / 4
    return bwCount







def detect(array):
    global last_white_piece_played, last_black_piece_played, white_pieces_captured, black_pieces_captured, bwCount

    for y in range(0,5):
        bwCount[0][y] = 0
        bwCount[1][y] = 0
    
    zpos = -9
    for z in array:
        xpos = -9
        for x in array:
            on = array[zpos+9-1,xpos+9-1]
            #print zpos+9-1,xpos+9-1
            c = int(on) - 1
            if on != 0.0:
                #In a column
                if array[zpos+9-1-1,xpos+9-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1-2,xpos+9-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1-3,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1-4,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1-5,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                                elif array[zpos+9-1-0,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                            elif array[zpos+9-1-0,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+1,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                        elif array[zpos+9-1-0,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+1,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+2,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                    elif array[zpos+9-1-0,xpos+9-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+1,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+2,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+3,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                elif array[zpos+9-1-0,xpos+9-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1+1,xpos+9-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+2,xpos+9-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+3,xpos+9-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+4,xpos+9-1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                #In a row
                if array[zpos+9-1,xpos+9-1-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1,xpos+9-1-2] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1,xpos+9-1-3] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1-4] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1-5] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                                elif array[zpos+9-1,xpos+9-1-0] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                            elif array[zpos+9-1,xpos+9-1-0] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1+1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                        elif array[zpos+9-1,xpos+9-1-0] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1+1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9+2] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                    elif array[zpos+9-1,xpos+9-1-0] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1,xpos+9-1+1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1+2] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1+3] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                elif array[zpos+9-1,xpos+9-1-0] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1,xpos+9-1+1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1,xpos+9-1+2] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1,xpos+9-1+3] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1,xpos+9-1+4] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                #Diagonal w/ - slope
                if array[zpos+9-1-1,xpos+9-1-1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1-2,xpos+9-1-2] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1-3,xpos+9-1-3] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1-4,xpos+9-1-4] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1-5,xpos+9-1-5] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                                elif array[zpos+9-1-0,xpos+9-1-0] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                            elif array[zpos+9-1-0,xpos+9-1-0] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+1,xpos+9-1+1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                        elif array[zpos+9-1-0,xpos+9-1-0] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+1,xpos+9-1+1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+2,xpos+9-1+2] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                    elif array[zpos+9-1-0,xpos+9-1-0] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+1,xpos+9-1+1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+2,xpos+9-1+2] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+3,xpos+9-1+3] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                elif array[zpos+9-1-0,xpos+9-1-0] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1+1,xpos+9-1+1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+2,xpos+9-1+2] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+3,xpos+9-1+3] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+4,xpos+9-1+4] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                #Diagonal w/ + slope
                if array[zpos+9-1-1,xpos+9-1+1] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1-2,xpos+9-1+2] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1-3,xpos+9-1+3] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1-4,xpos+9-1+4] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1-5,xpos+9-1+5] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                                elif array[zpos+9-1-0,xpos+9-1+0] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                            elif array[zpos+9-1-0,xpos+9-1+0] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+1,xpos+9-1-1] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                        elif array[zpos+9-1-0,xpos+9-1+0] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+1,xpos+9-1-1] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+2,xpos+9-1-2] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                    elif array[zpos+9-1-0,xpos+9-1+0] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+1,xpos+9-1-1] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+2,xpos+9-1-2] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+3,xpos+9-1-3] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                elif array[zpos+9-1-0,xpos+9-1+0] == on:
                    bwCount[c][0] += 1
                    if array[zpos+9-1+1,xpos+9-1-1] == on:
                        bwCount[c][1] += 1
                        if array[zpos+9-1+2,xpos+9-1-2] == on:
                            bwCount[c][2] += 1
                            if array[zpos+9-1+3,xpos+9-1-3] == on:
                                bwCount[c][3] += 1
                                if array[zpos+9-1+4,xpos+9-1-4] == on:
                                    bwCount[c][4] += 1
                                    we_have_a_winner(on)
                #Capture
                # if ((([xpos+9,zpos+9] == last_white_piece_played) and (on == 1.0)) or (([xpos+9,zpos+9] == last_black_piece_played) and (on == 2.0))):
                #     opposite_of_on = (1.0-(on-1.0))+1.0
                #     #Down
                #     if array[zpos+9-1-1,xpos+9-1] == opposite_of_on:
                #         if array[zpos+9-1-2,xpos+9-1] == opposite_of_on:
                #             if array[zpos+9-1-3,xpos+9-1] == on:
                #                 array[zpos+9-1-1,xpos+9-1] = 0.0
                #                 array[zpos+9-1-2,xpos+9-1] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     #Right
                #     if array[zpos+9-1,xpos+9-1-1] == opposite_of_on:
                #         if array[zpos+9-1,xpos+9-1-2] == opposite_of_on:
                #             if array[zpos+9-1,xpos+9-1-3] == on:
                #                 array[zpos+9-1,xpos+9-1-1] = 0.0
                #                 array[zpos+9-1,xpos+9-1-2] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     #Up
                #     if array[zpos+9-1+1,xpos+9-1] == opposite_of_on:
                #         if array[zpos+9-1+2,xpos+9-1] == opposite_of_on:
                #             if array[zpos+9-1+3,xpos+9-1] == on:
                #                 array[zpos+9-1+1,xpos+9-1] = 0.0
                #                 array[zpos+9-1+2,xpos+9-1] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     #Left
                #     if array[zpos+9-1,xpos+9-1+1] == opposite_of_on:
                #         if array[zpos+9-1,xpos+9-1+2] == opposite_of_on:
                #             if array[zpos+9-1,xpos+9-1+3] == on:
                #                 array[zpos+9-1,xpos+9-1+1] = 0.0
                #                 array[zpos+9-1,xpos+9-1+2] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     #Right Up Diagonal
                #     if array[zpos+9-1+1,xpos+9-1-1] == opposite_of_on:
                #         if array[zpos+9-1+2,xpos+9-1-2] == opposite_of_on:
                #             if array[zpos+9-1+3,xpos+9-1-3] == on:
                #                 array[zpos+9-1+1,xpos+9-1-1] = 0.0
                #                 array[zpos+9-1+2,xpos+9-1-2] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     #Left Down Diagonal
                #     if array[zpos+9-1-1,xpos+9-1+1] == opposite_of_on:
                #         if array[zpos+9-1-2,xpos+9-1+2] == opposite_of_on:
                #             if array[zpos+9-1-3,xpos+9-1+3] == on:
                #                 array[zpos+9-1-1,xpos+9-1+1] = 0.0
                #                 array[zpos+9-1-2,xpos+9-1+2] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     #Left Up Diagonal
                #     if array[zpos+9-1+1,xpos+9-1+1] == opposite_of_on:
                #         if array[zpos+9-1+2,xpos+9-1+2] == opposite_of_on:
                #             if array[zpos+9-1+3,xpos+9-1+3] == on:
                #                 array[zpos+9-1+1,xpos+9-1+1] = 0.0
                #                 array[zpos+9-1+2,xpos+9-1+2] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     #Right Down Diagonal
                #     if array[zpos+9-1-1,xpos+9-1-1] == opposite_of_on:
                #         if array[zpos+9-1-2,xpos+9-1-2] == opposite_of_on:
                #             if array[zpos+9-1-3,xpos+9-1-3] == on:
                #                 array[zpos+9-1-1,xpos+9-1-1] = 0.0
                #                 array[zpos+9-1-2,xpos+9-1-2] = 0.0
                #                 if on == 1.0:  black_pieces_captured += 2
                #                 else:  white_pieces_captured += 2
                #                 load_info()
                #     if on == 1.0:  last_white_piece_played = [None,None]
                #     else:  last_black_piece_played = [None,None]
            xpos += 1
        zpos += 1

    #bwCount[1][5] = white_pieces_captured
    #bwCount[0][5] = black_pieces_captured
        
    if white_pieces_captured == 10:  we_have_a_winner(2.0)
    if black_pieces_captured == 10:  we_have_a_winner(1.0)
    


    
    
def we_have_a_winner(on):
    global array, black_pieces_captured, white_pieces_captured, weights#,bwCount
    #print array
    bwCount = detectAB(array)
    #if bwCount [0][0] != 0:
    #    draw(array)
        
    #print bwCount
    # f = open('PenteData','a')
    # if on == 1.0:
    #     if bwCount[0][0] != 0:
    #         f.write('0')
    #         for x in range(0,5):
    #             f.write(',')
    #             f.write('%d'% bwCount[0][x])
    #         for x in range(0,5):
    #             f.write(',')
    #             f.write('%d'% bwCount[1][x])
    #         f.write('\n')
    #     WhiteWins.play()
    # else:
    #     if bwCount[1][0] != 0:
    #         f.write('1')
    #         for x in range(0,5):
    #             f.write(',')
    #             f.write('%d'% bwCount[0][x])
    #         for x in range(0,5):
    #             f.write(',')
    #             f.write('%d'% bwCount[1][x])
    #         f.write('\n')
    #     BlackWins.play()
    # f.close

    if on == 1.0:
        WhiteWins.play()
    else:
        BlackWins.play()
   
    draw(array)
    raw_input("press button... ")
    #weights = getWeights()
    #weights = logitWeights()
    #print weights
    array = zeros((19,19)) #0 = nothing, 1 = white, 2 = black
    black_pieces_captured = 0;  white_pieces_captured = 0
    

def main():
    global WhiteWins, BlackWins, bwCount, array, weights
    #array = zeros((19,19))
    try:  Music = pygame.mixer.Sound("Music/Music.wav");  Music.set_volume(0);  Music.play(-1)
    except:  Music = pygame.mixer.Sound("Music/Music.ogg");  Music.set_volume(0);  Music.play(-1)
    else:  pass
    WhiteWins = pygame.mixer.Sound("Data/WhiteWins.ogg")
    BlackWins = pygame.mixer.Sound("Data/BlackWins.ogg")
    #weights = getWeights()
    weights = logitWeights()
    #print weights
    #print type(weights[1])
    while True:

        if player_turn == "White":
            #raw_input("press button... ")
            array = get_ComInput(array)
            #raw_input("press button... ")
            #array = get_input(array)
            #print "Cplayer"
        else:
            array = get_ComInput(array)
            #array = get_input(array)
            #print "me"

        
        #array = get_ComInput(array)
        #print "Check"
        #print array
        #get_input(array)
        detect(array)
        #print "Black Count is: ",bwCount[1][0]
        draw(array)
        #raw_input("press button...")
        
        
if __name__ == '__main__': main()

