'''
    Gemaakt door Daan Sijnja, Student Mechatronica Haagse Hogeschool Delft, Studentnummer: 20177747

    @Description:
        Vind het intressant om deze dingen uit te zoeken en precies uit te vogelen hoe het werkt
    
    @Note:
        Dit is nu nog vooral wat code om een paar dingentjes te laten zien mischien komt er later een versie waarmee je dingen kan instellen 
'''

import cv2 as cv                                                                                        # Importeer OpenCV voor het afbeelden
import numpy as np                                                                                      # Importeer Numpy voor het makkelijk maken van Matrixen (word niet super veel gebruikt)
import math as mth                                                                                      # Importeer Math voor het gebruik van sinusen en cosinusen
import random as rdm                                                                                    # Importeer Random voor Random generatie

#global constants
NO_INTERSECT = 0
DO_INTERSECT = 1
COLLINIAR = 2


class Line:
    def __init__(self,p1,p2,color):
        self.p1 = p1[:]
        self.p2 = p2[:]
        self.color = color
    
    def translate(self,trans_mat):
        p1_h = self.p1[:]
        p2_h = self.p2[:]
    
        self.p1 = matrix_point_vgm(p1_h,trans_mat)
        self.p2 = matrix_point_vgm(p2_h,trans_mat)

    def check_intersect(self,oLine):

        P0, P1, P2, P3 = self.p1, self.p2, oLine.p1, oLine.p2
        
        A = (P1[1] - P0[1], P3[1] - P2[1] )                                                             # X constanten voor lijn 1 en lijn 2
        B = (P0[0] - P1[0], P2[0] - P3[0] )                                                             # Y constanten voor lijn 1 en lijn 2
        C = (A[0]*P0[0] + B[0]*P0[1], A[1]*P3[0] + B[1]*P3[1] )                                         # Lijn constanten voor lijn 1 en lijn 2                                                             

        
        denominant = (A[0] * B[1] - A[1] * B[0])
        # nog uitzoeken hoe colliniar werkt https://www.youtube.com/watch?v=pugy8etUrCk rond 6:10
        if(denominant == 0):
            return NO_INTERSECT, 0, 0

        x_intersect = (B[1]*C[0] - B[0]*C[1]) / denominant
        y_intersect = (A[0]*C[1] - A[1]*C[0]) / denominant
        rx = [0,0]
        ry = [0,0]

        try:
            rx[0] = (x_intersect - P0[0]) / (P1[0] - P0[0])
        except:
            rx[0] = 0

        try:
            rx[1] = (x_intersect - P2[0]) / (P3[0] - P2[0])
        except:
            rx[1] = 0

        try:
            ry[0] = (y_intersect - P0[1]) / (P1[1] - P0[1])
        except:
            ry[0] = 0

        try:
            ry[1] = (y_intersect - P2[1]) / (P3[1] - P2[1])
        except:
            ry[1] = 0

        def check_on_line(rx,ry):
            return ((rx[0] >= 0 and rx[0] <= 1) or (ry[0] >= 0 and ry[0] <= 1)) and ((rx[1] >= 0 and rx[1] <= 1) or (ry[1] >= 0 and ry[1] <= 1))

        if(check_on_line(rx,ry)):
            return DO_INTERSECT, x_intersect, y_intersect

        return NO_INTERSECT, 0, 0

    def get_z_coord(self,x,y):

        x0, x1 = self.p1[0], self.p2[0]
        y0, y1 = self.p1[1], self.p2[1]
        z0, z1 = self.p1[1], self.p2[1]

        dir_vect = (abs(x1-x0),abs(y1-y0),abs(z1-z0))

        if(dir_vect[0] != 0):
            l = (x-x0)/dir_vect[0]
        else:
            if(dir_vect[1] != 0):
                l = (y-y0)/dir_vect[1]
            else:
                l = 0

        z = z0 + l*dir_vect[2]

        return z

    def midpoint(self):

        p1 = self.p1
        p2 = self.p2

        mX = (p1[0] + p2[0]) / 2
        mY = (p1[1] + p2[1]) / 2
        mZ = (p1[2] + p2[2]) / 2

        return mX, mY, mZ


def order_lines(lines):
    length_lines = len(lines)
    all_orderd = True
    for i in range(1,length_lines):
        
        if(lines[i].midpoint()[2] > lines[i-1].midpoint()[2] ):

            _ = lines[i]
            lines[i] = lines[i-1]
            lines[i-1] = _

            all_orderd = False
    
    if(all_orderd == False):
        return order_lines(lines)

    return lines

    
def combine_fig(figures):
    combined_fig = []                                                                                   # Lege lijst voor alle lijnen
  
    for figure in figures:                                                                              # For alle figuren in figures
        for line in figure:                                                                             # For alle lijnen in figuren
            combined_fig.append(line)                                                                # Voeg de lijn toe aan de lijst
    
    return combined_fig                                                                                 # Return de gecombineerde figuren lijst

def draw_fig(img,figs,color=(255,255,255),thickness=1,calulate_order=True):
    '''
        @Input:
            img: afbeelding of canvas waar de figuren op getekend moeten worden

            fig: het figuur wat er getekend worden

            color: de kleur dat het figuur in getekend moet worden 
                Standaard: (255, 255, 255)

            thickness: de dikte van de lijnen van het figuur
                Standaard: 1
        @Return:

            img: afbeelding of canvas met het figuur er op getekend 

        @Description:

    '''
    lines = combine_fig(figs)
    if(calulate_order != False):
        lines = order_lines(lines)
  
    h, w, c = img.shape
    
    for line in lines:

        p1 = line.p1[0:2]
        p2 = line.p2[0:2]
        color = line.color[:]        

        p1 = [int(p1[0])+(h//2),int(p1[1])+(w//2)]
        p2 = [int(p2[0])+(h//2),int(p2[1])+(w//2)]
        cv.line(img,p1,p2,color,thickness)
    #cv.circle(img,(int(x)+(h//2),int(y)+(w//2)),5,(255,255,255))
   
    return img

def matrix_point_vgm(p,m):
    new_point = [0,0,0,1]

    new_point[0] = round(p[0]*m[0][0] + p[1]*m[0][1] + p[2]*m[0][2] + new_point[3]*m[0][3],4)
    new_point[1] = round(p[0]*m[1][0] + p[1]*m[1][1] + p[2]*m[1][2] + new_point[3]*m[1][3],4)
    new_point[2] = round(p[0]*m[2][0] + p[1]*m[2][1] + p[2]*m[2][2] + new_point[3]*m[2][3],4)
    new_point[3] = round(p[0]*m[2][0] + p[1]*m[3][1] + p[2]*m[3][2] + new_point[3]*m[3][3],4)
    return new_point[:3]


def translate_fig(fig,trans_mat):
    for line in fig:
        line.translate(trans_mat)
    return fig


def perspective_fig(fig,plane,cam):
    d_plane_cam = cam[2] - plane[2]
    new_fig = []
    for line in fig:
        color = line.color
        p1 = line.p1[:]
        d_p1_cam = cam[2] - p1[2]

        p1[0] = round(p1[0]*abs(d_plane_cam/d_p1_cam),4)
        p1[1] = round(p1[1]*abs(d_plane_cam/d_p1_cam),4)

        p2 = line.p2[:]
        d_p2_cam = cam[2] - p2[2]

        p2[0] = round(p2[0]*abs(d_plane_cam/d_p2_cam),4)
        p2[1] = round(p2[1]*abs(d_plane_cam/d_p2_cam),4)

        new_fig.append(Line(p1,p2,color))

    return new_fig       


def create_rot_matrix(angle):
    a = angle[0]*mth.pi/180
    b = angle[1]*mth.pi/180
    c = angle[2]*mth.pi/180

    rot_mat = [
                [ mth.cos(a)*mth.cos(b), mth.cos(a)*mth.sin(b)*mth.sin(c) - mth.sin(a)*mth.cos(c), mth.cos(a)*mth.sin(b)*mth.cos(c) + mth.sin(a)*mth.sin(c),0],
                [ mth.sin(a)*mth.cos(b), mth.sin(a)*mth.sin(b)*mth.sin(c) + mth.cos(a)*mth.cos(c), mth.sin(a)*mth.sin(b)*mth.cos(c) - mth.cos(a)*mth.sin(c),0],
                [ -mth.sin(b), mth.cos(b)*mth.sin(c), mth.cos(b)*mth.cos(c) , 0],
                [ 0, 0, 0, 1 ],
            ]

    return rot_mat

def create_transform_matrix(x,y,z):
    trans_mat = [
                    [1,0,0,x],
                    [0,1,0,y],
                    [0,0,1,z],
                    [0,0,0,1]
                ]
    return trans_mat



def generate_cube(size,color):
    cube = [
        #voorkant
        Line([-size,-size,size],[size,-size,size],color),
        Line([size,-size,size],[size,size,size],color),
        Line([size,size,size],[-size,size,size],color),
        Line([-size,size,size],[-size,-size,size],color),
        #ribben voor naar achter
        Line([-size,-size,size],[-size,-size,-size],color),
        Line([size,-size,size],[size,-size,-size],color),
        Line([size,size,size],[size,size,-size],color),
        Line([-size,size,size],[-size,size,-size],color),
        ##achterkant
        Line([-size,-size,-size],[size,-size,-size],color),
        Line([size,-size,-size],[size,size,-size],color),
        Line([size,size,-size],[-size,size,-size],color),
        Line([-size,size,-size],[-size,-size,-size],color),
        ##midpoint
        Line([0,0,0],[0,0,0],color)
        ]

    return cube[:]

def generate_piramid(base,height):
    #height = int(height)
    triagle = [
        #base
        [[-base,-base,-height/2],[-base,base,-height/2]],
        [[-base,base,-height/2],[base,base,-height/2]],
        [[base,base,-height/2],[base,-base,-height/2]],
        [[base,-base,-height/2],[-base,-base,-height/2]],
        #top
        [[-base,-base,-height/2],[0,0,height/2]],
        [[-base,base,-height/2],[0,0,height/2]],
        [[base,base,-height/2],[0,0,height/2]],
        [[base,-base,-height/2],[0,0,height/2]],
        #midpoint
        [[0,0,0],[0,0,0]],
        ]
    
    return triagle[:]    

def generate_random_voxels(amount,cubic=(100,100,100)):
    voxels = []

    for i in range(amount):
        x = rdm.randrange(-cubic[0],cubic[0])
        y = rdm.randrange(-cubic[1],cubic[1])
        z = rdm.randrange(-cubic[2],cubic[2])

        p = [x,y,z]
        voxels.append([p,p])

    return voxels[:]

'''Alles voor de Cube demo'''
cube_1 = generate_cube(125,(255,255,0))
cube_2 = generate_cube(87,(255,0,255))
cube_3 = generate_cube(50,(0,255,255))

def demo_cube(canvas):
    global cube_1
    global cube_2
    global cube_3

    werkvlak = canvas.copy()
    cube_1 = translate_fig(cube_1,create_rot_matrix((0.5,0.5,1)))
    cube_2 = translate_fig(cube_2,create_rot_matrix((0.5,1,0.5)))
    cube_3 = translate_fig(cube_3,create_rot_matrix((1,0.5,0.5)))
 
    cube1_pers = perspective_fig(cube_1,plane,camera)
    cube2_pers = perspective_fig(cube_2,plane,camera)
    cube3_pers = perspective_fig(cube_3,plane,camera)
    
    werkvlak = draw_fig(werkvlak,[cube1_pers,cube2_pers,cube3_pers],thickness=3)
    
    return werkvlak

'''Cube demo eind'''

'''Cube 4 demo'''

cube_red = generate_cube(50,(0,0,255))
cube_yellow = generate_cube(50,(0,255,255))
cube_green = generate_cube(50,(0,255,0))
cube_blue = generate_cube(50,(255,0,0))

t = 57

cube_red = translate_fig(cube_red,create_transform_matrix(t,t,t))
cube_yellow = translate_fig(cube_yellow,create_transform_matrix(-t,-t,t))
cube_green = translate_fig(cube_green,create_transform_matrix(t,-t,-t))
cube_blue = translate_fig(cube_blue,create_transform_matrix(-t,t,-t))

def demo_4_cubes(canvas):
    global cube_red
    global cube_yellow
    global cube_green
    global cube_blue
    angle = (0,5,1)
    cube_red = translate_fig(cube_red,create_rot_matrix(angle))
    cube_yellow = translate_fig(cube_yellow,create_rot_matrix(angle))
    cube_green = translate_fig(cube_green,create_rot_matrix(angle))
    cube_blue = translate_fig(cube_blue,create_rot_matrix(angle))

    cube_red_pers = perspective_fig(cube_red,plane,camera)
    cube_yellow_pers = perspective_fig(cube_yellow,plane,camera)
    cube_green_pers = perspective_fig(cube_green,plane,camera)
    cube_blue_pers = perspective_fig(cube_blue,plane,camera)
    
    werkvlak = draw_fig(canvas,[cube_red_pers,cube_yellow_pers,cube_green_pers,cube_blue_pers],thickness=3)
    
    return werkvlak

'''Cube 4 demo eind'''

'''Solar system demo'''
colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
satil = []

for i in range(31):
    satil.append([ Line([10,0,0],[-10,0,0],colors[i%len(colors)]),Line([7,20,0],[3,0,0],colors[i%len(colors)]), Line([-5,20,0],[-5,0,0],colors[i%len(colors)]), Line([7,20,0],[9,20,0],colors[i%len(colors)])])
    
    #generate_cube(10,colors[i%len(colors)])
offset = 20

for i in range(len(satil)):
    satil[i] = translate_fig(satil[i],create_transform_matrix(offset*i - offset*(len(satil)//2),0,0))

def demo_solar(canvas):
    
    global satil

    for i in range(len(satil)):
        satil[i] = translate_fig(satil[i],create_rot_matrix((abs((i+1)*0.5-0.5*(len(satil)//2+1)),0,0)))

    werkvlak = draw_fig(canvas,satil,thickness=3,calulate_order=False)

    return werkvlak

'''Solar system demo eind'''


'''Camera en projection plane'''
plane = [0,0,0]
camera = [0,0,-1000]

'''Assen'''
x_axis = [[[0,0,0],[1000,0,0]]]
y_axis = [[[0,0,0],[0,1000,0]]]
z_axis = [[[0,0,0],[0,0,1000]]]

'''werk canvas'''
canvas = np.zeros((640,640,3),np.uint8)


while True:
    werkvlak = canvas.copy()

    #werkvlak = demo_cube(werkvlak)
    #werkvlak = demo_4_cubes(werkvlak)
    werkvlak = demo_solar(werkvlak)
    cv.imshow('3d Renderer',werkvlak)


    k = cv.waitKey(30) & 0xff
    if (k == 27):
        break


cv.destroyAllWindows()







