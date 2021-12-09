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


def draw_fig(img,fig,color=(255,255,255),thickness=1):
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

    h, w, c = img.shape
    for line in fig:
        p1 = line[0][0:2]
        p2 = line [1][0:2]

        p1 = [int(p1[0])+(h//2),int(p1[1])+(w//2)]
        p2 = [int(p2[0])+(h//2),int(p2[1])+(w//2)]
        cv.line(img,p1,p2,color,thickness)

    return img

def matrix_point_vgm(p,m):
    new_point = [0,0,0,1]

    new_point[0] = p[0]*m[0][0] + p[1]*m[0][1] + p[2]*m[0][2] + new_point[3]*m[0][3]
    new_point[1] = p[0]*m[1][0] + p[1]*m[1][1] + p[2]*m[1][2] + new_point[3]*m[1][3]
    new_point[2] = p[0]*m[2][0] + p[1]*m[2][1] + p[2]*m[2][2] + new_point[3]*m[2][3]
    return new_point[:3]


def translate_fig(fig,trans_mat):
    new_fig = []
    for line in fig:
        p1_h = line[0][:]
        p2_h = line[1][:]

        p1 = matrix_point_vgm(p1_h,trans_mat)
        p2 = matrix_point_vgm(p2_h,trans_mat)

        new_fig.append([p1,p2])
        
    return new_fig


def perspective_fig(fig,plane,cam):
    d_plane_cam = cam[2] - plane[2]
    new_fig = []
    for line in fig:

        p1 = line[0][:]
        d_p1_cam = cam[2] - p1[2]

        p1[0] = p1[0]*abs(d_plane_cam/d_p1_cam)
        p1[1] = p1[1]*abs(d_plane_cam/d_p1_cam)

        p2 = line[1][:]
        d_p2_cam = cam[2] - p2[2]

        p2[0] = p2[0]*abs(d_plane_cam/d_p2_cam)
        p2[1] = p2[1]*abs(d_plane_cam/d_p2_cam)

        new_fig.append([p1,p2])

    return new_fig       


def create_rot_matrix(angle):
    a = angle[0]*mth.pi/180
    b = angle[1]*mth.pi/180
    c = angle[2]*mth.pi/180

    rot_mat = [
                [ mth.cos(a)*mth.cos(b), mth.cos(a)*mth.sin(b)*mth.sin(c) - mth.sin(a)*mth.cos(c), mth.cos(a)*mth.sin(b)*mth.cos(c) + mth.sin(a)*mth.sin(c),0],
                [ mth.sin(a)*mth.cos(b), mth.sin(a)*mth.sin(b)*mth.sin(c) + mth.cos(a)*mth.cos(c), mth.sin(a)*mth.sin(b)*mth.cos(c) - mth.cos(a)*mth.sin(c),0],
                [ -mth.sin(b), mth.cos(b)*mth.sin(c), mth.cos(b)*mth.cos(c),0],
                [ 0, 0, 0,1],
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



def generate_cube(size):
    cube = [
        #voorkant
        [[-size,-size,size],[size,-size,size]],
        [[size,-size,size],[size,size,size]],
        [[size,size,size],[-size,size,size]],
        [[-size,size,size],[-size,-size,size]],
        #ribben voor naar achter
        [[-size,-size,size],[-size,-size,-size]],
        [[size,-size,size],[size,-size,-size]],
        [[size,size,size],[size,size,-size]],
        [[-size,size,size],[-size,size,-size]],
        #achterkant
        [[-size,-size,-size],[size,-size,-size]],
        [[size,-size,-size],[size,size,-size]],
        [[size,size,-size],[-size,size,-size]],
        [[-size,size,-size],[-size,-size,-size]],
        #midpoint
        [[0,0,0],[0,0,0]],
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
cube_1 = generate_cube(125)
cube_2 = generate_cube(87)
cube_3 = generate_cube(50)

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

    werkvlak = draw_fig(werkvlak,cube1_pers,(255,255,0),2)
    werkvlak = draw_fig(werkvlak,cube2_pers,(255,0,255),2)
    werkvlak = draw_fig(werkvlak,cube3_pers,(0,255,255),2)

    return werkvlak

'''Cube demo eind'''


'''Camera en projection plane'''
plane = [0,0,0]
camera = [0,0,-1000]

'''Assen'''
x_axis = [[[0,0,0],[1000,0,0]]]
y_axis = [[[0,0,0],[0,1000,0]]]
z_axis = [[[0,0,0],[0,0,1000]]]

'''werk canvas'''
canvas = np.zeros((640,640,3),np.uint8)

voxels_1 = generate_random_voxels(50,(50,50,50))
voxels_2 = generate_random_voxels(75,(75,75,75))
voxels_3 = generate_random_voxels(100,(100,100,100))
a = 60

fig1 = generate_cube(a)
fig2 = generate_cube(a)
fig3 = generate_cube(a)
fig4 = generate_cube(a)
b = 70
fig1 = translate_fig(fig1,create_transform_matrix(b,b,-b))
fig2 = translate_fig(fig2,create_transform_matrix(-b,-b,-b))
fig3 = translate_fig(fig3,create_transform_matrix(b,-b,b))
fig4 = translate_fig(fig4,create_transform_matrix(-b,b,b))

while True:
    werkvlak = canvas.copy()
#
    fig1 = translate_fig(fig1,create_rot_matrix((1,1,1)))
    fig2 = translate_fig(fig2,create_rot_matrix((1,1,1)))
    fig3 = translate_fig(fig3,create_rot_matrix((1,1,1)))
    fig4 = translate_fig(fig4,create_rot_matrix((1,1,1)))    
    pers_fig1 = perspective_fig(fig1,plane,camera)
    pers_fig2 = perspective_fig(fig2,plane,camera)
    pers_fig3 = perspective_fig(fig3,plane,camera)
    pers_fig4 = perspective_fig(fig4,plane,camera)
    
    werkvlak = draw_fig(werkvlak,pers_fig1,(255,0,0),2)
    werkvlak = draw_fig(werkvlak,pers_fig2,(0,255,0),2)
    werkvlak = draw_fig(werkvlak,pers_fig3,(0,0,255),2)
    werkvlak = draw_fig(werkvlak,pers_fig4,(0,255,255),2)
    #werkvlak = demo_cube(werkvlak)


    cv.imshow('3d Renderer',werkvlak)

    k = cv.waitKey(30) & 0xff
    if (k == 27):
        break


cv.destroyAllWindows()







