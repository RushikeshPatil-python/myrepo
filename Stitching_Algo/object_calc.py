import numpy as np
import math


class object:

    '''
    This class will calculate all the parameters of passed object required for transformation.
    Prameters:
    stitching_edge = Stitching edge of passed object.
    object_data = Text file of all the pixel coordinates on object.
    pc_data = Point cloud data of entire image.
    '''

    def __init__(self, stitching_edge, object_data, pc_data, typ, obj_all):
        self.Object_points = object_data
        self.Object_New = obj_all
        self.PC_Data = pc_data
        self.Stitching_edge = stitching_edge
        self.Object_Type = typ
        self.PC_Values = []
        self.Object_cords = []
        self.Object_data = []
        self.XYZ_cord1 = []
        self.P = None
        self.Matrix = None

    def find_obj_cords(self, Object_points):
        all_object_data = open(Object_points, "r")
        object_lines = [line.strip() for line in all_object_data.readlines()]
        object_cords = []
        object_data = []
        for line in object_lines:
            a = line.replace("(", "").replace("):", ",").replace(" ", "")
            b = a.split(",")
            if len(b) == 3:
                cord = []
                cord.append(int(b[0]))
                cord.append(int(b[1]))
                object_cords.append(cord)
            elif len(b) == 5:
                cord = []
                val = []
                cord.append(int(b[0]))
                cord.append(int(b[1]))
                object_cords.append(cord)
                val.append(float(b[2]))
                val.append(float(b[3]))
                val.append(float(b[4]))
                object_data.append(val)
            self.Object_cords = object_cords
            self.Object_data = object_data
        return object_cords

    def create_pc_list(self, PC_Data):
        point_cloud = open(PC_Data, "r")
        pc_lines = [line.strip() for line in point_cloud.readlines()]
        pc_values = []
        for value in pc_lines:
            a = value.replace("(", "")
            b = a.replace("):", ",")
            c = b.replace(" ", "")
            d = c.split(",")
            if len(d) >= 5:
                l = []
                l.append(int(d[0]))
                l.append(int(d[1]))
                l.append(float(d[2]))
                l.append(float(d[3]))
                l.append(float(d[4]))
                pc_values.append(l)

        self.PC_Values = pc_values
        return pc_values

    def lmn_calculation(self, stitching_edge, pc_values):
        A_data = stitching_edge
        print(A_data)
        '''
        for cord in stitching_edge:
            for val in pc_values:
                if cord[0] == val[0] and cord[1] == val[1]:
                    A_data.append(val[2:])
        '''
        self.XYZ_cord1 = A_data[0]
        A_array = np.array(A_data)
        print(A_array)
        A = np.matrix(A_array)
        print(A)
        B_data = [[cord[1], 1] for cord in stitching_edge]
        B_array = np.array(B_data)
        B = np.matrix(B_array)
        B_transpose = B.T  # B_transpose
        B_transpose_B = B_transpose.dot(B)  # B_transpose*B
        B_transpose_B_inv = np.linalg.inv(B_transpose_B)  # (B_transpose*B)^-1
        B_transpose_B_inv_B_transpose = B_transpose_B_inv.dot(B_transpose)  # (B_tarnspose*B)^-1.B_transpose
        S = B_transpose_B_inv_B_transpose.dot(A)  # (B_tarnspose*B)^-1.B_transpose.A
        lmn = [S[0, 0], S[0, 1], S[0, 2]]
        xyz = [S[1, 0], S[1, 1], S[1, 2]]
        return [lmn, xyz]

    def abc_calculation(self, object_cords, pc_values, object_data):
        P_data = object_data
        '''
        if len(object_data) == 0:
            for cord in object_cords:
                for val in pc_values:
                    if cord[0] == val[0] and cord[1] == val[1]:
                        P_data.append(val[2:])
        else:
            P_data = object_data
        '''
        P_array = np.array(P_data)
        P = np.matrix(P_array)
        self.P  = P
        ones = np.ones((len(P_data), 1))
        # a_b_c = (P_transpose*P)^-1*P_transpose*ones
        P_transpose = P.T
        P_transpose_P = P_transpose.dot(P)
        P_transpose_P_inv = np.linalg.inv(P_transpose_P)
        P_transpose_P_inv_P_transpose = P_transpose_P_inv.dot(P_transpose)
        a_b_c = P_transpose_P_inv_P_transpose.dot(ones)  # a_b_c is matrix of shape (3, 1)
        # a, b, c are the values from 1st, 2nd & 3rd row respectively
        abc = [a_b_c[0, 0], a_b_c[1, 0], a_b_c[2, 0]]
        return abc

    def uvw_calculation(self, lmn, xyz, abc):
        l, m, n = lmn[0], lmn[1], lmn[2]
        x0, y0, z0 = xyz[0], xyz[1], xyz[2]
        a, b, c = abc[0], abc[1], abc[2]
        u = (1 - c) * m - b * ((l * x0) + (m * y0) + (n * z0) - n)
        v = a * ((l * x0) + (m * y0) + (n * z0) - n) - (1 - c) * l
        w = (a * m) - (b * l)
        return [u, v, w]

    def create_o1(self, lmn, abc, uvw, typ):
        parameters = []
        if typ == "regular":
            parameters = [lmn, abc, uvw]
        elif typ == "surface":
            print("Surface")
            parameters = [lmn, uvw, abc]
        o1_list = []
        for param in parameters:
            sq_root = math.sqrt((param[0]**2) + (param[1]**2) + (param[2]**2))
            l = [param[0]/sq_root, param[1]/sq_root, param[2]/sq_root]
            o1_list.append(l)
        o1_array = np.array(o1_list)
        self.Matrix = np.matrix(o1_array)

    def calculate(self):
        self.find_obj_cords(Object_points=self.Object_points)
        self.create_pc_list(PC_Data=self.PC_Data)
        lmn_xyz = self.lmn_calculation(stitching_edge=self.Stitching_edge, pc_values=self.PC_Values)
        abc = self.abc_calculation(object_cords=self.Object_cords, pc_values=self.PC_Values,\
                                   object_data=self.Object_New)
        uvw = self.uvw_calculation(lmn=lmn_xyz[0], xyz=lmn_xyz[1], abc=abc)
        self.create_o1(lmn=lmn_xyz[0], abc=abc, uvw=uvw, typ=self.Object_Type)



class New_Stitching_Edge:

    def __init__(self, object1_data, object2_data):
        self.Object1_Data = object1_data
        self.Object2_Data = object2_data
        self.Obj1_Stitching_Edge = []
        self.Obj2_Stitching_Edge = []
        self.Object1_Final = []
        self.Object2_Final = []

    def prepar_list(self, object_data):
        obj_data = open(object_data, "r")
        obj_lines = [line.strip() for line in obj_data.readlines()]
        data = []
        for line in obj_lines:
            a = ""
            if "(" in line:
                a = line.replace("(", "").replace("):", ",").replace(" ", "").split(",")
            else:
                a = line.split(",")
            if len(a) == 3:
                val = []
                val.append(float(a[0]))
                val.append(float(a[1]))
                val.append(float(a[2]))
                data.append(val)
            elif len(a) == 5:
                val = []
                val.append(float(a[2]))
                val.append(float(a[3]))
                val.append(float(a[4]))
                data.append(val)
        return data

    def add_edge_obj1(self, obj1_data):
        print(obj1_data)
        max_x = max(p[0] for p in obj1_data)
        max_col = []
        for point in obj1_data:
            if point[0] == max_x:
                max_col.append(point)
        print(max_col)
        extreme_point = []
        height = max(p[1] for p in obj1_data) - min(p[1] for p in obj1_data)
        central_row = min(p[1] for p in obj1_data) + (height/2)
        if len(max_col) > 1:
            max_y = max(p[1] for p in max_col)
            for point in max_col:
                if point[1] == max_y:
                    print(point)
                    extreme_point = point
        else:
            extreme_point = max_col[0]
        print(extreme_point)
        #rows = [extreme_point[1] - 0.0006, extreme_point[1] - 0.0004, extreme_point[1] - 0.0002,\
                #extreme_point[1] + 0.0002, extreme_point[1] + 0.0004, extreme_point[1] + 0.0006]
        rows = [central_row - 0.0006, central_row - 0.0004, central_row - 0.0002, \
                central_row + 0.0002, central_row + 0.0004, central_row + 0.0006]
        stitching_edge1 = []
        for row in rows:
            stitching_edge1.append([max_x, row, extreme_point[2]])
            obj1_data.append([max_x, row, extreme_point[2]])
        print(stitching_edge1)
        self.Obj1_Stitching_Edge = stitching_edge1
        self.Object1_Final = obj1_data

    def add_edge_obj2(self, obj2_data):
        min_x = min(p[0] for p in obj2_data)
        min_col = []
        for point in obj2_data:
            if point[0] == min_x:
                min_col.append(point)
        extreme_point = []
        height = max(p[1] for p in obj2_data) - min(p[1] for p in obj2_data)
        central_row = min(p[1]for p in obj2_data) + (height/2)
        if len(min_col) > 1:
            max_y = max(p[1] for p in min_col)
            for point in min_col:
                if point[1] == max_y:
                    extreme_point = point
        else:
            extreme_point = min_col[0]
        #rows = [extreme_point[1] - 0.0006, extreme_point[1] - 0.0004, extreme_point[1] - 0.0002,\
               # extreme_point[1] + 0.0002, extreme_point[1] + 0.0004, extreme_point[1] + 0.0006]
        rows = [central_row - 0.0006, central_row - 0.0004, central_row - 0.0002, \
                central_row + 0.0002, central_row + 0.0004, central_row + 0.0006]
        stitching_edge2 = []
        for row in rows:
            stitching_edge2.append([min_x, row, extreme_point[2]])
            obj2_data.append([min_x, row, extreme_point[2]])
        print(stitching_edge2)
        self.Obj2_Stitching_Edge = stitching_edge2
        self.Object2_Final = obj2_data

    def find(self):
        O1 = self.prepar_list(self.Object1_Data)
        O2 = self.prepar_list(self.Object2_Data)
        self.add_edge_obj1(O1)
        self.add_edge_obj2(O2)
        return self.Obj1_Stitching_Edge, self.Obj2_Stitching_Edge
























































