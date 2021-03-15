import numpy as np


class Transform_object2:
    '''
    This class will calculate Transformation matrix & transform the object2 using that matrix
    And will save transformed objects point cloud data as well as the ply file.
    '''

    def __init__(self, o1, xyz_1, o2, xyz_2, object2_data, object_cords, data_path, pc_path):
        self.Object1_Matrix = o1
        self.xyz_object1 = xyz_1
        self.Object2_Matrix = o2
        self.xyz_object2 = xyz_2
        self.Object2_data = object2_data
        self.Object2_cords = object_cords
        self.Transformation_matrix = None
        self.Object2_transformed = []
        self.Transformed_data_path = data_path
        self.Transformed_PC_path = pc_path
        self.Transformed_dataset = []

    def transformation_matrix(self, o1_matrix, o2_matrix):
        o1 = o1_matrix
        o2 = o2_matrix
        o2_inv = np.linalg.inv(o2)
        transformation_matrix = o2_inv.dot(o1)
        self.Transformation_matrix = transformation_matrix
        return transformation_matrix

    def apply_transformation(self, data_path, object2_data, object2_cords, xyz1, xyz2, trans_matrix):
        transformed_data = open(data_path, "w")
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
        diff = len(transformed) - len(object2_cords)
        for r in range(diff):
            object2_cords.append([0, 0])
        dataset = [value for value in zip(object2_cords, transformed)]
        for data in dataset:
            transformed_data.write("({}, {}):{},{},{}\n".format(data[0][0], data[0][1], data[1][0], data[1][1], data[1][2]))
        self.Object2_transformed = transformed
        self.Transformed_dataset = dataset
        return dataset

    def write_transformed_pc(self, transformed_object, transform_ply_path):
        transformed_pc = open(transform_ply_path, "w")
        transformed_pc.writelines("ply" + "\n" +
                                  "format ascii 1.0" + "\n" +
                                  "element vertex {}".format(len(self.Object2_transformed)) + "\n" +
                                  "property float32 x" + "\n" +
                                  "property float32 y" + "\n" +
                                  "property float32 z" + "\n" +
                                  "end_header" + "\n")
        for data in transformed_object:
            transformed_pc.write("{} {} {}\n".format(data[0], data[1], data[2]))

    def transform(self):
        trans_matrix = self.transformation_matrix(self.Object1_Matrix, self.Object2_Matrix)
        trans_data = self.apply_transformation(data_path=self.Transformed_data_path, object2_data=self.Object2_data, object2_cords= self.Object2_cords,\
                                               xyz1=self.xyz_object1, xyz2=self.xyz_object2, trans_matrix=trans_matrix)
        self.write_transformed_pc(transform_ply_path=self.Transformed_PC_path, transformed_object=self.Object2_transformed)


