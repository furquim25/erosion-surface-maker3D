#CORRIGIR ERRO NA LINHA 19. txt_reader(folderPath) está retornando None.
#Projeto erosao
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from natsort import natsorted, ns
import stl
from stl import mesh
#from mpl_toolkits.mplot3d import Axes3D

def main(input_folderPath,input_yInterval,input_resolution,input_stlCheck,input_levelingCheck,path_stl,list_of_axis_min_max,size_multiplier):
    #INPUT1 (Folder Path)
    try:
        folderPath = input_folderPath
        #Read the txt file and save the array to a variable.
        discreteFunctionsArray = txt_reader(folderPath)
        #print(discreteFunctionsArray)
        discreteFunctionsArray = heightLeveling(discreteFunctionsArray)
        #print ("###############AFTER###############")
        #print(discreteFunctionsArray)
        #INPUT5 (Leveling)
        if input_levelingCheck == True:
            discreteFunctionsArray = angleLeveling(discreteFunctionsArray)

        #discreteFunctionsArray=[ [[x1,y1],[x2y2,],[x3,y3]], [[x1,y2],[x2,y2],[x3,y3]]...]

    except:
        print ("error input 1")
        pass 

    #INPUT2 (y Interval)
    try:
        yInterval = float(input_yInterval)
        xyz = xyzArray(discreteFunctionsArray,yInterval)
    except:
        print ("error input 2")
        pass
    #INPUT3 (Resolution Interval)
    try:
        resolution = int(input_resolution)
        new_xyz = [[],[],[]]
        for i in range(0,(len(xyz[0])),resolution):
            new_xyz[0].append(xyz[0][i])
            new_xyz[1].append(xyz[1][i])
            new_xyz[2].append(xyz[2][i])
        totalPoints = len(xyz[0])
        xyz=new_xyz
        usedPoints = len(new_xyz[0])
    except:
        print ("error input 3")
        pass

    #INPUT4 (stl file option)
    try:
        generateStlOption = input_stlCheck
    except:
        print ("error input 4")
        pass    

    #Separete the array into three np variables (x,y,z).
    x = np.array(xyz[0])
    y = np.array(xyz[1])
    z = np.array(xyz[2])

    global load_message
    try:
        load_message = (f"Using {usedPoints} points of {totalPoints}. ({round((usedPoints*100/totalPoints),3)}%)")
    except:
        load_message = "Error"
    # Do the triangulation
    triang=triangulation(x,y)
    print("Triangulation Done")
    # Generate stl file
    if generateStlOption == True:
        generateStlFile(x,y,z,triang,path_stl)
    #plot a 3D graph.
    config_3D_graphic(x,y,z,triang,list_of_axis_min_max,size_multiplier)

def txt_reader(folderName):
    discreteFunctions=[]
    rugPoints=[]
    txtfiles = []
    datafolder = folderName
    for root, dirs, files in os.walk(datafolder):
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if (file_extension == ".txt"):
                txtfiles.append(file)
    txtfiles=natsorted(txtfiles, alg=ns.IGNORECASE)
    for x in txtfiles:
        f=open(datafolder + "/" + x)
        for line in f:
            try:
                point = [float(number) for number in (line.replace(",",".")).split(';')]
                rugPoints.append(point)
            except:
                continue
        discreteFunctions.append(rugPoints)
        rugPoints=[]
        f.close()
    print("Text Files Read Done")
    return discreteFunctions

def xyzArray(functions,yInterval):
    x=[]
    y=[]
    z=[]
    for i in range(len(functions)):
        for j in range(len(functions[i])):
            x.append(functions[i][j][0])
            y.append(i*yInterval)
            z.append(functions[i][j][1])        
    return [x,y,z]

def triangulation(x,y):
    triang=mtri.Triangulation(x, y)
    return triang

def generateStlFile(x,y,z,triang,path_stl):
    data = np.zeros(len(triang.triangles), dtype=mesh.Mesh.dtype)
    mobius_mesh = mesh.Mesh(data, remove_empty_areas=False)
    mobius_mesh.x[:] = x[triang.triangles]
    mobius_mesh.y[:] = y[triang.triangles]
    mobius_mesh.z[:] = z[triang.triangles]
    #mobius_mesh.save('erosion_surface.stl')
    mobius_mesh.save(path_stl)
    print("stl file Done")

def get_load_message():
    return load_message

def config_3D_graphic(x,y,z,triang,list_of_axis_min_max,size_multiplier):
    fig = plt.figure(figsize=(15*size_multiplier,5*size_multiplier),dpi=90)
    #Figure 1 (2D)
    ax = fig.add_subplot(1,2,1, projection='3d')
    surf=ax.plot_trisurf(triang, z, cmap='jet')
    #ax.scatter(x,y,z, marker='.', s=10, c="black", alpha=0.5)
    #ax.view_init(elev=60, azim=-45)
    ax.view_init(elev=60, azim=-45)
    ax.set_xlabel('X',labelpad=10)
    ax.set_ylabel('Y',labelpad=10)
    ax.set_zlabel('')

    if type(list_of_axis_min_max) == list:
        ax.set_xlim3d(list_of_axis_min_max[0][0], list_of_axis_min_max[0][1])
        ax.set_ylim3d(list_of_axis_min_max[1][0],list_of_axis_min_max[1][1])
        ax.set_zlim3d(list_of_axis_min_max[2][0],list_of_axis_min_max[2][1])

    #Figure 2 (3D)
    ax = fig.add_subplot(1,2,2, projection='3d')
    surf = ax.plot_trisurf(triang, z, cmap='jet')
    #ax.scatter(x,y,z, marker='.', s=100, c="red", alpha=1)
    ax.view_init(elev=89.99, azim=-90)
    ax.set_xlabel('X',labelpad=10)
    ax.set_ylabel('Y')
    ax.set_zlabel('')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_zticklabels([])

    plt.subplots_adjust(left=None, bottom=0.1, right=None, top=0.9, wspace=None, hspace=None)

def plot_3D_graphic():
    plt.show()

def heightLeveling(discreteFunctionsArray):
    #It assumes that all first points collected by the roughness meter are at the same height y=0 and it levels it.
    for rugPoints in discreteFunctionsArray:
        first_y_point = rugPoints[0][1]
        for point in rugPoints:
            point[1] = point[1] - first_y_point
    return discreteFunctionsArray

def angleLeveling(discreteFunctionsArray):
    for rugPoints in discreteFunctionsArray:
        X = np.array([], dtype='float')
        Y = np.array([], dtype='float')
        for point in rugPoints:
            X = np.append(X,point[0])
            Y = np.append(Y,point[1])

        # Alocação de espaço para os novos X e Y
        new_X = np.zeros((X.size), dtype='float')
        new_Y = np.zeros((Y.size), dtype='float')
        
        # Cálculo do ângulo médio de rotação usando nPairs pares de pontos
        nPairs = 10
        angle = 0
        for i in range(nPairs):
            angle += -np.arctan((Y[-(i + 1)] - Y[i])/(X[-(i + 1)] - X[i]))/nPairs

        # Cálculo dos novos valores de X e Y rotacionados
        # Pra essa etapa é importante que X e Y estejam na mesma unidade
        for i in range(len(X)):
            currentX = X[i] - X[0]
            currentY = Y[i] - Y[0]
            new_X[i] = currentX*np.cos(angle) - currentY*np.sin(angle)
            new_Y[i] = currentX*np.sin(angle) + currentY*np.cos(angle)
            
            rugPoints[i][0] = new_X[i]
            rugPoints[i][1] = new_Y[i]
    
    return discreteFunctionsArray    
        
            

        

#main("C:/Users/Rafael/Desktop/NIDF/Projeto Erosão/Projeto ESTÁGIO/DataTest2",1,1,True)
'''
Depends on the data
isBad = np.where((x<1) | (x>99) | (y<1) | (y>99), True, False)
mask = np.any(isBad[triang.triangles],axis=1)
triang.set_mask(mask)
'''

'''

#########Params#########
---yInterval--- 
Description: Interval on y axis between measurements taken by roughness meter.
Format: discreteFunctions = [ rugPoints1,rugPoint2... ]
yInterval = y

---rugPoints---
Description: Array contaning another array with the 2D cordinates of the points collected by the roughness meter after csv treatement.
Format: rugPoints = [[x1,z1],[x2,z2]...]
Where (x = horizontal axis) and (z = height)

---discreteFunctions--- 
Description: Receive rugPoints.
Format: discreteFunctions = [ rugPoints1,rugPoint2... ]
rugPoints1 = [[0,0],[1,1],[2,1],[3,1],[4,0]]
rugPoints2 = [[0,0],[1,1],[2,0.5],[3,1],[4,0]]
rugPoints3 = [[0,0],[1,1],[2,-1],[3,1],[4,0]]
rugPoints4 = [[0,0],[1,1],[2,0.5],[3,1],[4,0]]
rugPoints5 = [[0,0],[1,1],[2,1],[3,1],[4,0]]

discreteFunctions = [rugPoints1,rugPoints2,rugPoints3,rugPoints4,rugPoints5]
'''