#sam 
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys
import random
if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread
import math
# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["black"], 
                  pygame.color.THECOLORS["black"], 
                  pygame.color.THECOLORS["black"], 
                  pygame.color.THECOLORS["black"], 
                  pygame.color.THECOLORS["black"], 
                  pygame.color.THECOLORS["black"], 
                  pygame.color.THECOLORS["black"]]
class Totoro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.listOfTotoro = [
                        pygame.image.load("totoro1.jpg"),
                        pygame.image.load("totoro2.jpg"),
                        pygame.image.load("totoro3.jpg"),
                        pygame.image.load("totoro4.jpg"),
                        pygame.image.load("totoro5.jpg"),
                        pygame.image.load("totoro6.jpg"),
                        pygame.image.load("totoro7.jpg")]
        self._screen = pygame.display.set_mode((960, 540))
        self.currImage = 0

    def draw(self, surface):
        #Code for Totoro
        picture = self.listOfTotoro[self.currImage % len(self.listOfTotoro)]
        picture = pygame.transform.scale(picture, (1920, 1080))
        surface.blit(picture, (self.x,self.y),  area = None)
class Spirit1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = [pygame.image.load("Spirit1.png"),
        pygame.image.load("Spirit2.png"),
        pygame.image.load("Spirit3.png")]
        self.currImage = 0
        self.size = 100
    def draw(self, surface, x, y):
        #draws character 
        character1 = self.images[self.currImage% len(self.images)]
        character1 = pygame.transform.scale(character1, (self.size * 3, self.size * 3))
        surface.blit(character1, (self.x, self.y), area = None)
class Spirit2(Spirit1):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.images = [pygame.image.load("Spirit11.png"),
        pygame.image.load("Spirit12.png"),
        pygame.image.load("Spirit13.png")]
class Spirit3(Spirit1):
    def __init__(self,x, y):
        super().__init__(x,y)
        self.images = [pygame.image.load("Spirit111.png"),
        pygame.image.load("Spirit112.png"),
        pygame.image.load("Spirit113.png")]

class Broom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.upperCorner = 100
        self._screen = pygame.display.set_mode((1000, 700))
        self.lengthOfImage = 50
        self.currImage = 1 % self.lengthOfImage
    def draw(self, surface):
        if self.currImage > 50:
            self.currImage = 1
        string = "Cloud%d.jpg" %self.currImage
        image = pygame.image.load(string)
        picture = pygame.transform.scale(image, (4920, 4080))
        surface.blit(picture, (self.x,self.y),(100, self.upperCorner, 1920, 1080))
class littleTotoro(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("littleTotoro.png")
    def draw(self, surface):
        picture = pygame.transform.scale(self.image, (300,300))
        surface.blit(picture, (self.x, self.y), area = None)
    def intersects(self, x1, y1, x2, y2):
        if ((self.x > x1) and (self.x < x2) and (self.y > y1) and (self.y < y2)):
            return True
class sootSpirit1(littleTotoro):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.image = pygame.image.load("sootball1.png")
    def draw(self,surface):
        super().draw(surface)
        picture = pygame.transform.scale(self.image, (200, 200))
class sootSpirit2(sootSpirit1):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.image = pygame.image.load("sootball2.png")
class sootSpirit2(sootSpirit1):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.image = pygame.image.load("sootball3.png")

# #for the framework i took a lot of of example code from github
class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()
        self.size = 100
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()
        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        # here we will store skeleton data 
        self._bodies = None
        self.umbrella = pygame.image.load("umbrella.png")
        self.umbrella = pygame.transform.scale(self.umbrella, (self.size * 5, self.size * 5))
        self.Broom = Broom(10, 10)
        self.listOfJoints = [PyKinectV2.JointType_KneeLeft, 
        PyKinectV2.JointType_HipLeft,
        PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft,
        PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight,
        PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight,
        PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft,
        PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft,
        PyKinectV2.JointType_HandTipLeft, PyKinectV2.JointType_ThumbLeft,
        PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight,
        PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight,
        PyKinectV2.JointType_HandTipRight, PyKinectV2.JointType_ThumbRight,
        PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck,
        PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid,
        PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_ShoulderRight,
        PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_HipRight,
        PyKinectV2.JointType_HipLeft]
        self.spiritPoints = []
        self.TotoroMode = False
        self.CloudMode = False 
        self.spiritMode = False
        self.Totoro = Totoro(0,0)
        self.prevRightShoulderHeight = 0
        self.prevLeftShoulderHeight = 0
        self.curRightShoulderHeight = 0
        self.curLeftShoulderHeight = 0
        self.heightChange = 0
        self.broomImage = pygame.image.load("broom.png")
        self.broomImage = pygame.transform.scale(self.broomImage, (800, 300))
        self.gameMode = False
        self.TotoroGameMode = False
        self.BroomGameMode = False
        self.interactiveMode = False
        self.splashScreen = True
        self.listOfLittleTotoro = []
        self.listOfTotoroToDraw = []
        self.Score=0
        self.timerConstant = 50
        self.paused = False
        self.modeEnabled = False
    def drawBroom(self, surface, x, y):
        try:
            surface.blit(self.broomImage, (x- 100,y-50), area = None)
        except:
            pass
    def drawUmbrella(self, surface, x, y):
        try:
            surface.blit(self.umbrella, (x,y), area = None)
        except:
            pass
    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;
        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or 
            (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return
        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass
    def drawTricep(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;
        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return
        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        offset = (abs(start[0] - end[0])//2 , abs(start[1] - end[1])//2)
        try:
            pygame.draw.polygon(self._frame_surface, color, 
                ((start[0] - self.size//2, start[1]), 
                    (start[0] + self.size//2, start[1]), 
                    (end[0] + self.size//3, end[1]), 
                    (end[0] -self.size//2, end[1])))
            pygame.draw.circle(self._frame_surface, color, start, self.size//3, width = 0)
        except:
            return 
    def drawForearm(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or
         (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and
         (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color, 
                ((start[0] - self.size//3, start[1]),
             (start[0] + self.size//3, start[1]), 
             (end[0] + self.size//4, end[1]),
              (end[0] -self.size//4, end[1])))
            pygame.draw.circle(self._frame_surface, color, start, self.size//5)
        except:
            return 
    def drawThigh(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) 
            or (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        mid = (jointPoints[joint0].x, 
            (jointPoints[joint0].y + abs(jointPoints[joint0].y- jointPoints[joint1].y)//2))
        try:
            pygame.draw.polygon(self._frame_surface, color, 
                ((start[0] - self.size * 0.75, start[1]),
                 (start[0] + self.size *0.75, start[1]),
                  (end[0] + self.size//2, end[1]),
                   (end[0] -self.size//2, end[1])))
            pygame.draw.circle(self._frame_surface, color, 
                (int(end[0]), int(end[1])), self.size//2)
        except:
            return 
    def drawCalf(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color,((start[0] - self.size//3, start[1]),
             (start[0] + self.size//3, start[1]), (end[0] + self.size//4, end[1]), 
             (end[0] -self.size//4, end[1])))
            pygame.draw.circle(self._frame_surface, color, start, self.size//4, width = 0)
        except:
            return
    def drawNeck(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color, 
                ((start[0] - self.size//4, start[1]), 
                    (start[0] + self.size//4, start[1]), 
                    (end[0] + self.size//4, end[1]), 
                    (end[0] -self.size//4, end[1])))
        except:
            return
    def drawHead(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or 
            (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return
        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        offset = (jointPoints[joint1].y + jointPoints[joint1].y)//2
        middle = (jointPoints[joint0].x, jointPoints[joint1].y - offset//6)
        try:
            pygame.draw.circle(self._frame_surface, color, (int(end[0]), 
                int(middle[1])), int(self.size))
        except:
            return
    def drawUpperBody(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or 
            (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and
         (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color,
             ((start[0] - self.size * 1.4, start[1]),
             (start[0] + self.size * 1.4, start[1]), 
             (end[0] + self.size * 1.25, end[1]), 
             (end[0] -self.size * 1.25, end[1])))
        except:
            return
    def drawLowerBody(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or
         (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            
            pygame.draw.polygon(self._frame_surface, color,(
            (start[0] - self.size * 1.25, start[1]),
             (start[0] + self.size * 1.25, start[1]), 
             (end[0] + self.size, end[1]), 
             (end[0] -self.size, end[1])))
        except:
            return
    def drawShoulder(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or 
            (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.circle(self._frame_surface, color, 
                (int(end[0]), int(end[1])), self.size//2)
        except:
            return
    def drawHip(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or 
            (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color,(
                (start[0] - self.size, start[1]),
                (start[0] + self.size, start[1]),
                (end[0] + self.size, end[1]), 
                (end[0] -self.size, end[1])))
            pygame.draw.circle(self._frame_surface, color, 
                (int(end[0]), int(end[1])), self.size//2)
        except:
            return
    def drawFoot(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or
         (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and
         (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color,(
                (start[0] - self.size//3, start[1]),
             (start[0] + self.size//3, start[1]), 
             (end[0] + self.size//3, end[1]), 
             (end[0] -self.size//3, end[1])))
        except:
            return
    def drawThumb(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or
         (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color,(
            (start[0] - self.size//10, start[1]),
             (start[0] + self.size//10, start[1]),
              (end[0] + self.size//10, end[1]), 
             (end[0] -self.size//10, end[1])))
        except:
            return
    def drawHand(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or 
            (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color,(
                (start[0] - self.size//3, start[1]),
             (start[0] + self.size//3, start[1]),
              (end[0] + self.size//3, end[1]), 
             (end[0] -self.size//3, end[1])))
        except:
            return
    def drawWrist(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if ((joint0State == PyKinectV2.TrackingState_NotTracked) or
         (joint1State == PyKinectV2.TrackingState_NotTracked)): 
            return

        # both joints are not *really* tracked
        if ((joint0State == PyKinectV2.TrackingState_Inferred) and 
            (joint1State == PyKinectV2.TrackingState_Inferred)):
            return
        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        try:
            pygame.draw.polygon(self._frame_surface, color,(
                (start[0] - self.size//3, start[1]),
             (start[0] + self.size//3, start[1]), 
             (end[0] + self.size//3, end[1]), 
             (end[0] -self.size//3, end[1])))
        except:
            return
    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.drawHead(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.drawNeck(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.drawUpperBody(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.drawLowerBody(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.drawShoulder(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.drawShoulder(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);

        # Right Arm    
        self.drawTricep(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.drawForearm(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.drawWrist(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.drawHand(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.drawThumb(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.drawTricep(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.drawForearm(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.drawWrist(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.drawHand(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.drawThumb(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.drawThigh(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.drawCalf(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.drawFoot(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.drawThigh(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.drawCalf(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.drawFoot(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()
    def drawSplashScreen(self, surface, joints):
        surface.fill(pygame.color.THECOLORS["white"])
        pygame.draw.rect(surface,  pygame.color.THECOLORS["red"], (0,0,500,500))
        pygame.draw.rect(surface,  pygame.color.THECOLORS["purple"], (0, 600, 500, 500 ))
        pygame.draw.rect(surface, pygame.color.THECOLORS["pink"], (1300, 0, 1000, 1600))
        (LeftHandX, LeftHandY) = (self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].x, 
                                self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].y)
        myfont = pygame.font.SysFont("monospace", 60)
        label = myfont.render("Game1", 1, (0,0, 200))
        label1 = myfont.render("Game2", 1, (0,0, 200))
        label2 = myfont.render("InteractiveMode", 1, (0,0,200))
        surface.blit(label1, (0, 700))
        surface.blit(label, (0, 200))
        surface.blit(label2, (1300, 600))
        if self.modeEnabled == False:
            if LeftHandX > 0 and LeftHandX < 400 and LeftHandY > 0 and LeftHandY < 400:
                self.gameMode = True
                self.TotoroGameMode = True
                self.SplashScreenMode = False
                self.interactiveMode = False
                self.modeEnabled = True
            if LeftHandX > 0 and LeftHandX < 500 and LeftHandY > 600 and LeftHandY < 1100:
                self.gameMode = True
                self.BroomGameMode = True
                self.SplashScreenMode = False
                self.interactiveMode = False
                self.modeEnabled = True
            if LeftHandX > 1000 and LeftHandX < 1600 and LeftHandY > 0 and LeftHandY < 1600:
                self.interactiveMode = True
                self.SplashScreenMode = False
                self.gameMode = False
                self.modeEnabled = True
    
    def drawThingsToCollect(self, joints, surface):
        for thingToDraw in self.listOfLittleTotoro:
            thingToDraw.draw(self._frame_surface)
            intersection = thingToDraw.intersects(self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].x- 200, 
                                        self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].y - 300, 
                                        self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].x, 
                                        self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].y)
            if intersection:
                self.Score += 10
                self.listOfLittleTotoro.remove(thingToDraw)
        self.drawBroom(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].x - 200, 
                            self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].y- 100)
        pygame.draw.rect(surface, pygame.color.THECOLORS["white"], (800,720, 500, 100))
        myfont = pygame.font.SysFont("", 60)
        label = myfont.render("score %s" % self.Score, 1, (0,0, 200))
        surface.blit(label, (930, 750)) 
    def drawSpiritsOnJoints(self,joints, surface):
        while len(self.spiritPoints) < 3:
            newPoint = random.choice(self.listOfJoints)
            if newPoint not in self.spiritPoints:
                if (self._kinect.body_joints_to_color_space(joints)[newPoint].x - 500 > 0
                and self._kinect.body_joints_to_color_space(joints)[newPoint].y -500 > 0):
                    self.spiritPoints.append(newPoint) 
        first = Spirit1(self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[0]].x, 
                  self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[0]].y)
        second = Spirit2(self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[1]].x , 
                  self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[1]].y)
        third = Spirit3(self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[2]].x , 
                            self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[2]].y)   
        first.draw(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[0]].x - 500, 
                            self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[0]].y-500)
        first.currImage += 1
        second.draw(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[1]].x - 500, 
                            self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[1]].y-500)
        second.currImage += 1
        third.draw(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[2]].x- 500, 
                            self._kinect.body_joints_to_color_space(joints)[self.spiritPoints[2]].y-500)
        third.currImage += 1
    def legalBodies(self, bodyRange, joints):
        count = 0 
        for joint in self.listOfJoints:
            jointState = joints[joint].TrackingState;
            if (jointState == PyKinectV2.TrackingState_Inferred or
             jointState == PyKinectV2.TrackingState_NotTracked):
                count += 1
        if count > 2:
            return False
        return True
    def drawPauseScreen(self, surface):
        surface.fill(pygame.color.THECOLORS["white"])
        myfont = pygame.font.SysFont("monospace", 60)
        label = myfont.render("This is a Pause Screen, make sure you can be tracked", 1, (0,0, 200))
        surface.blit(label, (0, 700))         

    def drawInteractiveModeSplashScreen(self, surface):
        surface.fill(pygame.color.THECOLORS["white"])
        myfont = pygame.font.SysFont("monospace", 60)
        label = myfont.render("Touch your nose to reset the mode", 1, (0,0, 150))
        label2 = myfont.render("Raise right hand for Totoro", 1, (0,0, 150))
        label3 = myfont.render("Put left hand in front of right", 1, (0,0, 150))
        label4 = myfont.render("raise right knee above hip for spirits", 1, (0,0, 150))
        surface.blit(label, (0, 100))
        surface.blit(label2, (0, 300))   
        surface.blit(label3, (0, 500))   
        surface.blit(label4, (0, 700))  
    #got the run fucntion from a framework on github but not the actual drawing part 
    #like the other stuff like the bodies being None etc        
    def run(self):
        # -------- Main Program Loop -----------
        clockTimer = 0
        while not self._done:
            clockTimer += 1
            # --- Main event loop

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32) 
                elif event.type == pygame.KEYDOWN:
                    self.splashScreen = True
                    self.TotoroMode = False
                    self.CloudMode = False 
                    self.spiritMode = False 
                    self.interactiveMode = False 
                    self.gameMode = False
                    self.TotoroGameMode = False
                    self.BroomGameMode = False
                    self.paused = False
                    self.modeEnabled = False            
            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    joints = body.joints
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    if self.legalBodies(i, joints) == False:
                        self.drawPauseScreen(self._frame_surface)
                        self.paused = True                      
                    if not self.legalBodies(i, joints):
                        self.paused = False
                        self.drawSplashScreen(self._frame_surface, joints)
                        if not self.paused and self.interactiveMode:
                            self.drawInteractiveModeSplashScreen(self._frame_surface)
                            if (self.splashScreen and not self.interactiveMode 
                                and not self.TotoroGameMode and not self.BroomGameMode
                                and not self.paused):
                                self.drawSplashScreen(self._frame_surface, joints)
                            if joints[PyKinectV2.JointType_HandRight].Position.y > 0 and not self.spiritMode and not self.CloudMode:  
                                self.TotoroMode = True
                            if (joints[PyKinectV2.JointType_HandLeft].Position.x > 
                                    joints[PyKinectV2.JointType_HandRight].Position.x and not self.spiritMode and not self.TotoroMode):
                                self.CloudMode = True
                            #how to detect if someone is sitting or not
                            if (joints[PyKinectV2.JointType_KneeRight].Position.y > 
                            joints[PyKinectV2.JointType_HipRight].Position.y and not self.TotoroMode and not self.CloudMode):
                                self.spiritMode = True
                            if ((abs(joints[PyKinectV2.JointType_HandLeft].Position.x -joints[PyKinectV2.JointType_Head].Position.x) < 1/4)
                                and abs(joints[PyKinectV2.JointType_HandLeft].Position.y - joints[PyKinectV2.JointType_Head].Position.y)<1/4):
                                self.CloudMode = False
                                self.TotoroMode = False
                                self.spiritMode = False
                            if self.TotoroMode == True and self.spiritMode == False and self.CloudMode == False:
                                self.Totoro.draw(self._frame_surface)
                                self.Totoro.currImage += 1
                                self.drawUmbrella(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].x - 200, 
                                    self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].y- 300)
                            if self.TotoroMode == False and self.spiritMode == False and self.CloudMode == True:
                                if joints[PyKinectV2.JointType_ShoulderLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                        self.curLeftShoulderHeight = self._kinect.body_joints_to_color_space(joints)[JointType_ShoulderLeft].y
                                if joints[PyKinectV2.JointType_ShoulderRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                        self.curRightShoulderHeight = self._kinect.body_joints_to_color_space(joints)[JointType_ShoulderRight].y
                                self.heightChange = max(int(self.curRightShoulderHeight - self.prevRightShoulderHeight),
                                 int(self.curLeftShoulderHeight - self.prevLeftShoulderHeight)) 
                                self.drawBroom(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].x - 200, 
                                    self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].y- 100)
                                if math.isnan(self.heightChange):
                                    self.heightChange = 0
                                if self.Broom.upperCorner > 1920:
                                    self.Broom.upperCorner = 1920
                                elif self.Broom.upperCorner < 0:
                                    self.Broom.upperCorner = 0
                                self.Broom.upperCorner -= 1
                                self.Broom.upperCorner += self.heightChange
                                self.prevRightShoulderHeight = self.curRightShoulderHeight
                                self.prevLeftShoulderHeight = self.curLeftShoulderHeight
                                self.Broom.currImage += 1
                                self.Broom.draw(self._frame_surface)
                                self.drawBroom(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].x - 200, 
                            self._kinect.body_joints_to_color_space(joints)[JointType_HandLeft].y- 100)
                            if self.spiritMode and self.TotoroMode == False and self.CloudMode == False:
                                self.drawSpiritsOnJoints(joints, self._frame_surface)
                    if self.TotoroGameMode == True:
                        self.Totoro.draw(self._frame_surface)
                        self.Totoro.currImage += 1
                        self.drawUmbrella(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].x - 200, 
                                self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].y- 300)
                        joint_points = self._kinect.body_joints_to_color_space(joints)
                        if clockTimer % self.timerConstant == 0:
                            randomInt = random.randrange(150, 1700)
                            self.listOfLittleTotoro.append(littleTotoro(randomInt, 0))
                        elif clockTimer % 30 == 0:
                            randomInt = random.randrange(150, 1700)
                            self.listOfLittleTotoro.append(sootSpirit1(randomInt, 0))
                        for coordinates in self.listOfLittleTotoro:
                            coordinates.y += 10
                            if coordinates.y > 1000:
                                self.Score -= 10
                                self.listOfLittleTotoro.remove(coordinates) 
                        for thingToDraw in self.listOfLittleTotoro:
                            thingToDraw.y += 10
                            thingToDraw.draw(self._frame_surface)
                            intersection = thingToDraw.intersects(self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].x- 200, 
                                self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].y - 300, 
                                self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].x, 
                                self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].y)
                            if intersection:
                                self.Score += 10
                                self.listOfLittleTotoro.remove(thingToDraw)                 
                        self.drawUmbrella(self._frame_surface, self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].x - 200, 
                                self._kinect.body_joints_to_color_space(joints)[JointType_HandRight].y- 300)
                        myfont = pygame.font.SysFont("monospace", 50)
                        label = myfont.render("score %s" % self.Score, 1, (0,0, 200))
                        self._frame_surface.blit(label, (1270, 700))
                    if self.BroomGameMode and not self.interactiveMode and not self.TotoroGameMode:
                        if joints[PyKinectV2.JointType_ShoulderLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curLeftShoulderHeight = self._kinect.body_joints_to_color_space(joints)[JointType_ShoulderLeft].y
                        if joints[PyKinectV2.JointType_ShoulderRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.curRightShoulderHeight = self._kinect.body_joints_to_color_space(joints)[JointType_ShoulderRight].y
                            self.heightChange = max(int(self.curRightShoulderHeight - self.prevRightShoulderHeight),
                            int(self.curLeftShoulderHeight - self.prevLeftShoulderHeight)) 
                            if math.isnan(self.heightChange):
                                self.heightChange = 0
                            if self.Broom.upperCorner > 1920:
                                self.Broom.upperCorner = 1920
                            elif self.Broom.upperCorner < 0:
                                self.Broom.upperCorner = 0
                            self.Broom.upperCorner -= 1
                            self.Broom.upperCorner += self.heightChange
                            self.prevRightShoulderHeight = self.curRightShoulderHeight
                            self.prevLeftShoulderHeight = self.curLeftShoulderHeight
                            self.Broom.currImage += 1
                            self.Broom.draw(self._frame_surface)
                            if clockTimer % self.timerConstant == 0:
                                randomInt = random.randrange(150, 1700)
                                self.listOfLittleTotoro.append(littleTotoro(1920, randomInt))
                            elif clockTimer % 30 == 0:
                                randomInt = random.randrange(150, 1700)
                                self.listOfLittleTotoro.append(sootSpirit1(randomInt, 0))
                            for coordinates in self.listOfLittleTotoro:
                                coordinates.x -= 5
                                if coordinates.x < 10:
                                    self.Score -= 10
                                    self.listOfLittleTotoro.remove(coordinates)
                                self.drawThingsToCollect(joints, self._frame_surface)
                                self.SplashScreenMode = False                                     
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])
            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(30)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()

#i also took the run function and the final framework from the example code
__main__ = "Kinect v2 Body Game"
game = BodyGameRuntime();
game.run();
