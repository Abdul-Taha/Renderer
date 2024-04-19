from cmath import cos, sin
import numpy as n
import turtle
import time
import trimesh
import os

file_name = "20mm_cube.stl"    #Enter the name of the file
Model = trimesh.load(os.path.join(os.path.dirname(__file__), file_name))    #Get model data

screen = turtle.Screen()    #Start a screen instance
pen = turtle.Turtle()    #Create a turtle that will draw our model
pen.ht()    #Hide the visible turtle on the screen
screen.tracer(False)    #Turn off the animation for drawing

def rot_mtx(deg,axis,mtx):    #Create a function to rotate 3d coordinates
    deg = n.radians(deg)    #Convert from degrees to radians
    if axis == 'x':    #Check if the chosen axis is x
        return n.dot(n.matrix([[1,0,0],[0,cos(deg),-sin(deg)],[0,sin(deg),cos(deg)]]),mtx)    #Multiply the given matrix with a rotation matrix for the x axis involving the given degree
    if axis == 'y':    #Check if the chosen axis is y
        return n.dot(n.matrix([[cos(deg),0,sin(deg)],[0,1,0],[-sin(deg),0,cos(deg)]]),mtx)    #Multiply the given matrix with a rotation matrix for the y axis involving the given degree
    if axis == 'z':    #Check if the chosen axis is x
        return n.dot(n.matrix([[cos(deg),-sin(deg),0],[sin(deg),cos(deg),0],[0,0,1]]),mtx)    #Multiply the given matrix with a rotation matrix for the z axis involving the given degree

def proj_mtx(mtx):    #Create a function to turn 3d coordinates into 2d
     return n.dot(n.matrix([[1,0,0],[0,1,0]]),mtx)    #Multiply given matrix by a projection matrix

def trans_mtx(x,y,z,mtx):    #Create a function to translate 3d coordinates
    hom_coords = n.ones((1, mtx.shape[1]))    #Create homogenous coordinates
    mtx = n.vstack([mtx, hom_coords])   #Combine them with given matrix
    translation_mtx = n.array([ [1, 0, 0, x],    #Define the translation matrix
                                [0, 1, 0, y],
                                [0, 0, 1, z],
                                [0, 0, 0, 1]]) 
    mtx = n.dot(translation_mtx, mtx)     #Multiply the given matrix with translation matrix
    return mtx[:-1]  #Return matrix with the homogenous coordinates removed

def scal_mtx(x, y, z, mtx):    #Create a function to scale 3d coordinates
    hom_coords = n.ones((1, mtx.shape[1]))    #Create homogenous coordinates 
    mtx = n.vstack([mtx, hom_coords])      #Combine them with given matrix
    scale_mtx = n.array([ [x, 0, 0, 0],    #Define the scale matrix
                          [0, y, 0, 0],
                          [0, 0, z, 0],
                          [0, 0, 0, 1]])  
    mtx = n.dot(scale_mtx, mtx)     #Multiply the given matrix with scale matrix
    return mtx[:-1]    #Return matrix with the homogenous coordinates removed

degx = -90    #Change initial degrees
degy = 0
degz = 0

while True:
    degx += 0    #Choose how much to increase the degree by every loop
    degy += 10
    degz += 0
    scale_factor  = 1     #Choose scale factor
    for i in Model.vertices[Model.edges_unique] :    #Iterate through edges
        p13Dcoords = rot_mtx(degx,'x',n.matrix(i[0]).reshape(3,1))
        p13Dcoords = rot_mtx(degy,'y',p13Dcoords.reshape(3,1))
        p13Dcoords = rot_mtx(degz,'z',p13Dcoords.reshape(3,1))
        p23Dcoords = rot_mtx(degx,'x',n.matrix(i[1]).reshape(3,1))
        p23Dcoords = rot_mtx(degy,'y',p23Dcoords.reshape(3,1))
        p23Dcoords = rot_mtx(degz,'z',p23Dcoords.reshape(3,1))
        #Apply rotations
        
        p13Dcoords = trans_mtx(0, -10, 0, p13Dcoords)
        p13Dcoords = scal_mtx(scale_factor, scale_factor, scale_factor, p13Dcoords)
        p23Dcoords = trans_mtx(0, -10, 0, p23Dcoords)
        p23Dcoords = scal_mtx(scale_factor, scale_factor, scale_factor, p23Dcoords)
        #Apply translations
        
        x1 = int(proj_mtx(p13Dcoords.real.reshape((3,1)))[0][0].item())*10
        y1 = int(proj_mtx(p13Dcoords.real.reshape((3,1)))[1][0].item())*10
        x2 = int(proj_mtx(p23Dcoords.real.reshape((3,1)))[0][0].item())*10
        y2 = int(proj_mtx(p23Dcoords.real.reshape((3,1)))[1][0].item())*10
        #Convert to 2D coordinates
        
        pen.goto(x1,y1)
        pen.pendown()
        pen.dot(10)
        pen.goto(x2,y2)
        pen.dot(10)
        pen.penup()
        #Draw points and edge
    
    screen.update()    #Update screen
    time.sleep(0.05)    #Sleep 0.05 seconds
    pen.clear()    #Clear Screen
