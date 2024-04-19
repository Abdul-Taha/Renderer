from cmath import cos, sin
import numpy as n
import turtle
import time
import trimesh
import os
file_name = "20mm_cube.stl"
Model = trimesh.load(os.path.join(os.path.dirname(__file__), file_name))

screen = turtle.Screen()
pen = turtle.Turtle()
pen.ht()
screen.tracer(False)

deg = 0
def rot_mtx(deg,vector,mtx):
    deg = n.radians(deg)
    if vector == 'x':
        return n.dot(n.matrix([[1,0,0],[0,cos(deg),-sin(deg)],[0,sin(deg),cos(deg)]]),mtx)
    if vector == 'y':
        return n.dot(n.matrix([[cos(deg),0,sin(deg)],[0,1,0],[-sin(deg),0,cos(deg)]]),mtx)
    if vector == 'z':
        return n.dot(n.matrix([[cos(deg),-sin(deg),0],[sin(deg),cos(deg),0],[0,0,1]]),mtx)

def proj_mtx(mtx):
     return n.dot(n.matrix([[1,0,0],[0,1,0]]),mtx)

def trans_mtx(x,y,z,mtx):
    hom_coords = n.ones((1, mtx.shape[1]))
    mtx = n.vstack([mtx, hom_coords])  
    translation_mtx = n.array([ [1, 0, 0, x],
                                [0, 1, 0, y],
                                [0, 0, 1, z],
                                [0, 0, 0, 1]]) 
    mtx = n.dot(translation_mtx, mtx) 
    return mtx[:-1]  

def scal_mtx(x, y, z, mtx):
    hom_coords = n.ones((1, mtx.shape[1])) 
    mtx = n.vstack([mtx, hom_coords])  
    scale_mtx = n.array([ [x, 0, 0, 0],
                          [0, y, 0, 0],
                          [0, 0, z, 0],
                          [0, 0, 0, 1]])  
    mtx = n.dot(scale_mtx, mtx) 
    return mtx[:-1]

vertices = []
edges = Model.vertices[Model.edges_unique]

for i in Model.vertices:
    vertices.append(n.matrix(i))

degx = -90
degy = 0
degz = 0

while True:
    degx += 0
    degy += 10
    degz += 0
    scale_factor  = 1
    for i in edges:
        p13Dcoords = rot_mtx(degx,'x',n.matrix(i[0]).reshape(3,1))
        p13Dcoords = rot_mtx(degy,'y',p13Dcoords.reshape(3,1))
        p13Dcoords = rot_mtx(degz,'z',p13Dcoords.reshape(3,1))
        p23Dcoords = rot_mtx(degx,'x',n.matrix(i[1]).reshape(3,1))
        p23Dcoords = rot_mtx(degy,'y',p23Dcoords.reshape(3,1))
        p23Dcoords = rot_mtx(degz,'z',p23Dcoords.reshape(3,1))

        p13Dcoords = trans_mtx(0, -10, 0, p13Dcoords)
        p13Dcoords = scal_mtx(scale_factor, scale_factor, scale_factor, p13Dcoords)

        p23Dcoords = trans_mtx(0, -10, 0, p23Dcoords)
        p23Dcoords = scal_mtx(scale_factor, scale_factor, scale_factor, p23Dcoords)

        x1 = int(proj_mtx(p13Dcoords.real.reshape((3,1)))[0][0].item())*10
        y1 = int(proj_mtx(p13Dcoords.real.reshape((3,1)))[1][0].item())*10
        x2 = int(proj_mtx(p23Dcoords.real.reshape((3,1)))[0][0].item())*10
        y2 = int(proj_mtx(p23Dcoords.real.reshape((3,1)))[1][0].item())*10
        pen.goto(x1,y1)
        pen.pendown()
        pen.dot(10)
        pen.goto(x2,y2)
        pen.dot(10)
        pen.penup()
    screen.update()
    time.sleep(0.05)
    pen.clear()