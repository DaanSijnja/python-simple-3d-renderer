import math as mth
import numpy as np

def CreateRotationMatrix(roll,pitch,yaw):
    a = roll*mth.pi/180
    b = pitch*mth.pi/180
    c = yaw*mth.pi/180

    rotMat = [
                [ mth.cos(a)*mth.cos(b), mth.cos(a)*mth.sin(b)*mth.sin(c) - mth.sin(a)*mth.cos(c), mth.cos(a)*mth.sin(b)*mth.cos(c) + mth.sin(a)*mth.sin(c),0],
                [ mth.sin(a)*mth.cos(b), mth.sin(a)*mth.sin(b)*mth.sin(c) + mth.cos(a)*mth.cos(c), mth.sin(a)*mth.sin(b)*mth.cos(c) - mth.cos(a)*mth.sin(c),0],
                [ -mth.sin(b), mth.cos(b)*mth.sin(c), mth.cos(b)*mth.cos(c) , 0],
                [ 0, 0, 0, 1 ],
            ]
    
    return np.array(rotMat)

def CreateScaleMatrix(xScale,yScale,zScale):

    scaleMat = [
                [xScale,0,0,0],
                [0,yScale,0,0],
                [0,0,zScale,0],
                [0,0,   0,  1]
               ]

    return np.array(scaleMat)

def CreateTransformMatrix(xTransform,yTransform,zTransform):

    transMat = [
                [0,0,0,xTransform],
                [0,0,0,yTransform],
                [0,0,0,zTransform],
                [0,  0,   0,    1]
               ]

    return np.array(transMat)

def CreateShearMatrix(xShear,yShear,zShear):
    pass

def DotProduct(matrixA,matrixB):
    return np.dot(matrixA,matrixB)