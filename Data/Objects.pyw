import os, sys
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

pygame.init()

def main(Textures):
    BoardFile = os.path.join('Data', 'Grey Marble.gif')
    BoardSurface = pygame.image.load(BoardFile).convert()
    BoardData = pygame.image.tostring(BoardSurface, "RGBA", 1)

    WhiteMarbleFile = os.path.join('Data', 'White Marble.gif')
    WhiteMarbleSurface = pygame.image.load(WhiteMarbleFile).convert()
    WhiteMarbleData = pygame.image.tostring(WhiteMarbleSurface, "RGBA", 1)

    BlackMarbleFile = os.path.join('Data', 'Black Marble.gif')
    BlackMarbleSurface = pygame.image.load(BlackMarbleFile).convert()
    BlackMarbleData = pygame.image.tostring(BlackMarbleSurface, "RGBA", 1)
    
    GridFile = os.path.join('Data', 'Red Marble Grid.gif')
    GridSurface = pygame.image.load(GridFile).convert()
    GridData = pygame.image.tostring(GridSurface, "RGBA", 1)

    SelectFile = os.path.join('Data', 'Select.png')
    SelectSurface = pygame.image.load(SelectFile).convert_alpha()
    SelectData = pygame.image.tostring(SelectSurface, "RGBA", 1)

    glBindTexture(GL_TEXTURE_2D, Textures[0]) #Board (Grey Section)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, BoardSurface.get_width(), BoardSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, BoardData )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, Textures[1]) #White Stone
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, WhiteMarbleSurface.get_width(), WhiteMarbleSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, WhiteMarbleData )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, Textures[2]) #Black Stone
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, BlackMarbleSurface.get_width(), BlackMarbleSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, BlackMarbleData )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, Textures[3]) #Board (Red Section)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, GridSurface.get_width(), GridSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, GridData )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, Textures[4]) #Select Cursor
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, SelectSurface.get_width(), SelectSurface.get_height(), 0,
                  GL_RGBA, GL_UNSIGNED_BYTE, SelectData )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glGenLists(1)
    glNewList(1, GL_COMPILE)#Board
    glBindTexture(GL_TEXTURE_2D, Textures[0]) #Board (Grey Section)
    glBegin(GL_QUADS)
    #TOP BORDER
    #Quad 1
    glTexCoord2f(0.0, 0.0); glVertex3f(-21.0,  0.0, -21.0)
    glTexCoord2f(0.04167, 0.0); glVertex3f(-19, 0.0, -21.0)
    glTexCoord2f(0.04167, 1.0); glVertex3f(-19, 0.0, 21.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-21.0,  0.0, 21.0)
    #Quad 2
    glTexCoord2f(1.0, 0.0); glVertex3f(21.0,  0.0, -21.0)
    glTexCoord2f(0.95833, 0.0); glVertex3f(19, 0.0, -21.0)
    glTexCoord2f(0.95833, 1.0); glVertex3f(19, 0.0, 21.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(21.0,  0.0, 21.0)
    #Quad 3
    glTexCoord2f(0.04167, 0.95833); glVertex3f(-19, 0.0, 19)
    glTexCoord2f(0.95833, 0.95833); glVertex3f(19,  0.0, 19)
    glTexCoord2f(0.95833, 1.0); glVertex3f(19,  0.0, 21.0)
    glTexCoord2f(0.04167, 1.0); glVertex3f(-19, 0.0, 21.0)
    #Quad 4
    glTexCoord2f(0.04167, 0.04167); glVertex3f(-19, 0.0, -19)
    glTexCoord2f(0.95833, 0.04167); glVertex3f(19,  0.0, -19)
    glTexCoord2f(0.95833, 0.0); glVertex3f(19,  0.0, -21.0)
    glTexCoord2f(0.04167, 0.0); glVertex3f(-19, 0.0, -21.0)
    #SIDES
    #Left Side
    glTexCoord2f(0.14286, 0.0); glVertex3f(-21.0, -3.0, -21.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-21.0, 0.0, -21.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-21.0, 0.0, 21.0)
    glTexCoord2f(0.14286, 1.0); glVertex3f(-21.0, -3.0, 21.0)
    #Right Side
    glTexCoord2f(0.85714, 0.0); glVertex3f(21.0, -3.0, -21.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(21.0, 0.0, -21.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(21.0, 0.0, 21.0)
    glTexCoord2f(0.85714, 1.0); glVertex3f(21.0, -3.0, 21.0)
    #Bottom Side
    glTexCoord2f(0.85714, 0.0); glVertex3f(-21.0, -3.0, 21.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-21.0, 0.0, 21.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(21.0, 0.0, 21.0)
    glTexCoord2f(0.85714, 1.0); glVertex3f(21.0, -3.0, 21.0)
    #Top Side
    glTexCoord2f(0.85714, 0.0); glVertex3f(-21.0, -3.0, -21.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-21.0, 0.0, -21.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(21.0, 0.0, -21.0)
    glTexCoord2f(0.85714, 1.0); glVertex3f(21.0, -3.0, -21.0)
    #BOTTOM
    glTexCoord2f(0.0, 0.0); glVertex3f(-21.0, -3.0, -21.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(21.0,  -3.0, -21.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(21.0,  -3.0, 21.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-21.0, -3.0, 21.0)
    glEnd();
    #GRID
    glBindTexture(GL_TEXTURE_2D, Textures[3]) #Board (Red Section)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-19.0, 0.0, -19.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(19.0, 0.0, -19.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(19.0, 0.0, 19.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-19.0, 0.0, 19.0)
    glEnd();
    glEndList()

    glGenLists(1)
    glNewList(2, GL_COMPILE)#White Marble
    glBindTexture(GL_TEXTURE_2D, Textures[1]) #White Stone
    glPushMatrix()
    glScalef(1.0, 0.5, 1.0)
    Sphere = gluNewQuadric()
    gluQuadricTexture(Sphere, GL_TRUE)
    gluSphere(Sphere, 0.75, 80, 80)
    glPopMatrix()
    glEndList()

    glGenLists(1)
    glNewList(3, GL_COMPILE)#Black Marble
    glBindTexture(GL_TEXTURE_2D, Textures[2]) #Black Stone
    glPushMatrix()
    glScalef(1.0, 0.5, 1.0)
    Sphere = gluNewQuadric()
    gluQuadricTexture(Sphere, GL_TRUE)
    gluSphere(Sphere, 0.75, 80, 80)
    glPopMatrix()
    glEndList()
    
    glGenLists(1)
    glNewList(4, GL_COMPILE)#Select
    glBindTexture(GL_TEXTURE_2D, Textures[4]) #Select Cursor
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.175, 0.0, -2.175)
    glTexCoord2f(1.0, 0.0); glVertex3f(2.175, 0.0, -2.175)
    glTexCoord2f(1.0, 1.0); glVertex3f(2.175, 0.0, 2.175)
    glTexCoord2f(0.0, 1.0); glVertex3f(-2.175, 0.0, 2.175)
    glEnd();
    glEndList()
