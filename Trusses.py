import math
import numpy as np

# Creating a list of nodes and members of the truss
truss_nodes = []
truss_members = []


# Classes to hold the properties of every node and span of the truss structure
class Node:
    def __init__(self, x_coord=1, y_coord=1, support="", force=1, x_dof=1, y_dof=1):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.support = support
        self.force = force
        self.x_dof = x_dof
        self.y_dof = y_dof


class Members:
    def __init__(self, length=1.0, cos_theta_y=1.0, cos_theta_x=1.0, stiffness_matrix=np.zeros((2, 3)),
                 near_node=Node(), far_node=Node(), area=1.0, ei_value=1.0):
        self.length = length
        self.cos_theta_y = cos_theta_y
        self.cos_theta_x = cos_theta_x
        self.stiffness_matrix = stiffness_matrix
        self.near_node = near_node
        self.far_node = far_node
        self.area = area
        self.ei_value = ei_value


# Including every node and member into lists, and making them an instance of their respective classes
node_count = int(input("How many nodes are there in your Truss? "))
member_count = int(input("How many members are there in your Truss? "))
for i in range(node_count):
    truss_nodes.append("")
    truss_nodes[i] = Node()
for i in range(member_count):
    truss_members.append("")
    truss_members[i] = Members()

# Getting the area and EI values of every member
constant_area = input("Are the cross-sectional areas of all members constant? (yes) or (no) ")
constant_ei_value = input("Are the EI values of all members constant? (yes) or (no) ")

if constant_area == "no":
    for i in range(member_count):
        truss_members[i].area = float(input(f"What is the cross-sectional area of member {i + 1} on the truss? "))

if constant_ei_value == "no":
    for i in range(member_count):
        truss_members[i].area = float(input(f"what is the EI value of member {i + 1} on the truss? "))

# Getting the coordinates of every node from user
for i in range(node_count):
    truss_nodes[i].x_coord, truss_nodes[i].y_coord = \
        (float(x) for x in input(f"What are the (x,y) coordinates of node {i + 1}? ").split(','))

# Getting the near and far end nodes of every member in the structure
for i in range(member_count):
    nn = int(input(f"What is the near node number of member {i + 1} "))
    fn = int(input(f"What is the far node number of member {i + 1} "))
    truss_members[i].near_node = truss_nodes[nn - 1]
    truss_members[i].far_node = truss_nodes[fn - 1]

# Getting the degrees of freedom on each node
for i in range(node_count):
    truss_nodes[i].x_dof = (2 * (i + 1)) - 1
    truss_nodes[i].y_dof = (2 * (i + 1))

# To get the lengths and cosines of every member
for i in range(member_count):
    truss_members[i].length = \
        (math.sqrt((truss_members[i].far_node.x_coord - truss_members[i].near_node.x_coord) ** 2 +
                   (truss_members[i].far_node.y_coord - truss_members[i].near_node.y_coord) ** 2))

    truss_members[i].cos_theta_x = ((truss_members[i].far_node.x_coord - truss_members[i].near_node.x_coord) /
                                    truss_members[i].length)

    truss_members[i].cos_theta_y = ((truss_members[i].far_node.y_coord - truss_members[i].near_node.y_coord) /
                                    truss_members[i].length)

# fixing the elements of the member stiffness matrix
for j in range(member_count):
    truss_members[j].stiffness_matrix = np.zeros((2 * node_count, 2 * node_count))

    # row 1 of the member stiffness matrix
    truss_members[j].stiffness_matrix[truss_members[j].near_node.x_dof - 1, truss_members[j].near_node.x_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x ** 2)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].near_node.x_dof - 1, truss_members[j].near_node.y_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].near_node.x_dof - 1, truss_members[j].far_node.x_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x ** 2)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].near_node.x_dof - 1, truss_members[j].far_node.y_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    # row 1 completed, row 2 begins
    truss_members[j].stiffness_matrix[truss_members[j].near_node.y_dof - 1, truss_members[j].near_node.x_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].near_node.y_dof - 1, truss_members[j].near_node.y_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_y ** 2)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].near_node.y_dof - 1, truss_members[j].far_node.x_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].near_node.y_dof - 1, truss_members[j].far_node.y_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_y ** 2)) / truss_members[j].length), 3)

    # row 2 completed, row 3 begins
    truss_members[j].stiffness_matrix[truss_members[j].far_node.x_dof - 1, truss_members[j].near_node.x_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x ** 2)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].far_node.x_dof - 1, truss_members[j].near_node.y_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].far_node.x_dof - 1, truss_members[j].far_node.x_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x ** 2)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].far_node.x_dof - 1, truss_members[j].far_node.y_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    # row 3 completed, row 4 begins
    truss_members[j].stiffness_matrix[truss_members[j].far_node.y_dof - 1, truss_members[j].near_node.x_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].far_node.y_dof - 1, truss_members[j].near_node.y_dof - 1] = \
        round(((-1 * truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_y ** 2)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].far_node.y_dof - 1, truss_members[j].far_node.x_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_x * truss_members[j].cos_theta_y)) / truss_members[j].length), 3)

    truss_members[j].stiffness_matrix[truss_members[j].far_node.y_dof - 1, truss_members[j].far_node.y_dof - 1] = \
        round(((truss_members[j].area * truss_members[j].ei_value *
                (truss_members[j].cos_theta_y ** 2)) / truss_members[j].length), 3)

# Adding all the members stiffness matrices
struct_stiffness_matrix = np.zeros((2*node_count, 2*node_count))
for i in range(member_count):
    struct_stiffness_matrix = np.add(struct_stiffness_matrix, truss_members[i].stiffness_matrix)

# Creating the one-column displacement matrix


matrix_times_displacement = np.dot(A, B)
