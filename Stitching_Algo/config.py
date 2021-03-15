#from stitching_edge import stitching_edge
from object_calc import object, New_Stitching_Edge
from transform import Transform_object2
import numpy as np
import cv2
#from Edge import find_central_stitch_point

object_data = ["Jayesh Front Cam/Data/RMPM_5966.txt", "Jayesh Front Cam/Data/RC_5964.txt", "Jayesh Front Cam/Data/RLI_5963.txt",\
               "Jayesh Front Cam/Data/RCI_5962.txt", "Jayesh Front Cam/Data/LCI_5962.txt", "Jayesh Front Cam/Data/LLI_5969.txt", "Jayesh Front Cam/Data/LC_5972.txt",\
                "Jayesh Front Cam/Data/LMPM_5977.txt"]#, "Jayesh Front Cam/Data/LPM2_1682.txt", "Jayesh Front Cam/Data/LM_1682.txt"]
Complete_data = ["Jayesh Front Cam/Data/RMPM_5966.txt", "Jayesh Front Cam/Data/RC_5964_Complete.txt", "Jayesh Front Cam/Data/RLI_5963_Complete.txt",\
               "Jayesh Front Cam/Data/RCI_5962_Complete.txt", "Jayesh Front Cam/Data/LCI_5962_Complete.txt", "Jayesh Front Cam/Data/LLI_5969_Complete.txt", "Jayesh Front Cam/Data/LC_5972_Complete.txt",\
                "Jayesh Front Cam/Data/LMPM_5977.txt"]
Trans = ["Jayesh Front Cam/Trans/RMPM","Jayesh Front Cam/Trans/RC", "Jayesh Front Cam/Trans/RLI", "Jayesh Front Cam/Trans/RCI", "Jayesh Front Cam/Trans/LCI",\
         "Jayesh Front Cam/Trans/LLI", "Jayesh Front Cam/Trans/LC", "Jayesh Front Cam/Trans/LMPM"]#, "Jayesh Front Cam/Trans/LPM2", "Jayesh Front Cam/Trans/LM"]
for obj in object_data:


        #edge = stitching_edge(o1_contour="Mold New/Data/RC_3_Contour.txt", o2_contour="Mold New/Data/Incisors_3_Contour.txt")
        #edge = Stitching_Edge(o1_data="Mold New/Data/LMPM_3_Contour.txt", o2_data="Mold New/Data/LC2_3_Contour.txt")
        
        #object1_edge = find_central_stitch_point(object_data="Jayendra/Data/LLI_3_Object.txt", side="right")
        #object2_edge = find_central_stitch_point(object_data="Jayendra/Data/LC1_3_Object.txt", side="left")
        if object_data.index(obj) == 0:
            edge = New_Stitching_Edge(object1_data=obj, object2_data=object_data[object_data.index(obj)+1])
            object1_edge, object2_edge = edge.find()
            object1 = object(stitching_edge=object1_edge, object_data=obj,\
                            pc_data=Complete_data[object_data.index(obj)], typ="regular", obj_all=edge.Object1_Final)
            object1.calculate()


            obj_1_txt = open(Trans[object_data.index(obj)] + ".txt", "w")
            obj_1_ply = open(Trans[object_data.index(obj)]+ ".ply", "w")
            #object1.Object_data.extend(object1_edge)
            diff = len(edge.Object1_Final) - len(object1.Object_cords)
            for r in range(diff):
                object1.Object_cords.append([0, 0])
            dataset = [value for value in zip(object1.Object_cords, edge.Object1_Final)]
            obj_1_ply.writelines("ply" + "\n" +
                                  "format ascii 1.0" + "\n" +
                                  "element vertex {}".format(len(dataset)) + "\n" +
                                  "property float32 x" + "\n" +
                                  "property float32 y" + "\n" +
                                  "property float32 z" + "\n" +
                                  "end_header" + "\n")
            for data in dataset:
                obj_1_txt.write("({}, {}):{},{},{}\n".format(data[0][0], data[0][1], data[1][0], data[1][1], data[1][2]))
                obj_1_ply.write("{} {} {}\n".format(data[1][0], data[1][1], data[1][2]))



            object2 = object(stitching_edge=object2_edge, object_data=object_data[object_data.index(obj)+1],\
                            pc_data=Complete_data[object_data.index(obj)+1] ,typ="regular", obj_all=edge.Object2_Final)
            object2.calculate()
            trans = Transform_object2(o1=object1.Matrix, xyz_1=object1.XYZ_cord1, o2=object2.Matrix, xyz_2=object2.XYZ_cord1,\
                                    object2_data=object2.P, object_cords=object2.Object_cords,\
                                    data_path=Trans[object_data.index(obj) + 1]+ str(".txt"), pc_path=Trans[object_data.index(obj) + 1]+ str(".ply"))
            trans.transform()
        elif object_data.index(obj) != 0 and object_data[-1] != obj:
            print(object_data.index(obj))
            edge = New_Stitching_Edge(object1_data=Trans[object_data.index(obj)] + str(".txt"), object2_data=object_data[object_data.index(obj)+1])
            object1_edge, object2_edge = edge.find()
            object1 = object(stitching_edge=object1_edge, object_data=Trans[object_data.index(obj)] + str(".txt"),\
                            pc_data=Trans[object_data.index(obj)] + str(".txt"), typ="regular", obj_all=edge.Object1_Final)
            object1.calculate()
            

            obj_1_txt = open(Trans[object_data.index(obj)] + ".txt", "w")
            obj_1_ply = open(Trans[object_data.index(obj)]+ ".ply", "w")
            object1.Object_data.extend(object1_edge)
            diff = len(object1.Object_data) - len(object1.Object_cords)
            for r in range(diff):
                object1.Object_cords.append([0, 0])
            dataset = [value for value in zip(object1.Object_cords, object1.Object_data)]
            obj_1_ply.writelines("ply" + "\n" +
                                  "format ascii 1.0" + "\n" +
                                  "element vertex {}".format(len(dataset)) + "\n" +
                                  "property float32 x" + "\n" +
                                  "property float32 y" + "\n" +
                                  "property float32 z" + "\n" +
                                  "end_header" + "\n")
            for data in dataset:
                obj_1_txt.write("({}, {}):{},{},{}\n".format(data[0][0], data[0][1], data[1][0], data[1][1], data[1][2]))
                obj_1_ply.write("{} {} {}\n".format(data[1][0], data[1][1], data[1][2]))

            object2 = object(stitching_edge=object2_edge, object_data=object_data[object_data.index(obj)+1],\
                            pc_data= Complete_data[object_data.index(obj)+1], typ="regular", obj_all=edge.Object2_Final)
            object2.calculate()
            trans = Transform_object2(o1=object1.Matrix, xyz_1=object1.XYZ_cord1, o2=object2.Matrix, xyz_2=object2.XYZ_cord1,\
                                    object2_data=object2.P, object_cords=object2.Object_cords,\
                                    data_path=Trans[object_data.index(obj) + 1]+ str(".txt"), pc_path=Trans[object_data.index(obj) + 1]+ str(".ply"))
            trans.transform()
        elif object_data[-1] == obj:
            break

        



def transformation(object2_data, xyz1, xyz2, trans_matrix, ply_path, txt_path, cords):
    transformed_data = open(txt_path, "w")
    O2_transformed = object2_data.dot(trans_matrix)
    xyz2_array = np.array(xyz2)
    xyz2 = np.matrix(xyz2_array)
    xyz_t = xyz2.dot(trans_matrix)
    x = xyz1[0]
    y = xyz1[1]
    z = xyz1[2]
    xt = xyz_t[0, 0]
    yt = xyz_t[0, 1]
    zt = xyz_t[0, 2]
    transformed = []
    for data in O2_transformed:
        '''
        In this loop x_t will be subtracted from x of each point & x_1 will be added.
        Similarly for y & z.
        Modified points will be written in the text file.
        '''
        x1 = data[0, 0] - xt + x
        y1 = data[0, 1] - yt + y
        z1 = data[0, 2] - zt + z
        transformed.append([x1, y1, z1])
    dataset = zip(cords, transformed)
    for data in dataset:
        if len(data)==2:
            transformed_data.write("({}, {}):{},{},{}\n".format(data[0][0], data[0][1], data[1][0], data[1][1], data[1][2]))
    #for data in transformed:
           # transformed_data.write("{}, {}, {}\n".format(data[0], data[1], data[2]))
    ply_file = open(ply_path, "w")
    ply_file.writelines("ply" + "\n" +
                              "format ascii 1.0" + "\n" +
                              "element vertex {}".format(len(transformed)) + "\n" +
                              "property float32 x" + "\n" +
                              "property float32 y" + "\n" +
                              "property float32 z" + "\n" +
                              "end_header" + "\n")
    for data in transformed:
        ply_file.write("{} {} {}\n".format(data[0], data[1], data[2]))

'''
file = open("Jayesh Front Cam/Data/img_5813_RPM1.txt", "r")
lines = [line.strip() for line in file.readlines()]
Object_Data = []
Objet_cords = []
for line in lines:
    data = line.replace("(", "").replace("):", ",").replace(" ", "").split(",")
    #data = line.replace("[", "").replace("]", "").replace(" ", "").split(",")
    if len(data) == 5:
        cord = []
        val = []
        cord.append(int(data[0]))
        cord.append(int(data[1]))
        val.append(float(data[2]))
        val.append(float(data[3]))
        val.append(float(data[4]))
        Object_Data.append(val)
        Objet_cords.append(cord)
    elif len(data) == 3:
        val = []
        val.append(float(data[0]))
        val.append(float(data[1]))
        val.append(float(data[2]))
        Object_Data.append(val)
object_arr = np.array(Object_Data)
object_matrix = np.matrix(object_arr)
print(object_matrix)
#transformation(object_matrix, object1.XYZ_cord1, object2.XYZ_cord1, trans.Transformation_matrix,\
             #"Jayesh Front Cam/Trans/LLI.ply", "Jayesh Front Cam/Trans/LLI.txt", Objet_cords)
'''