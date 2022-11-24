import math
import numpy as np
from sympy import symbols, Eq, solve

# Creating a list of nodes and members of the truss
truss_nodes = []
truss_members = []


# Classes to hold the properties of every node and span of the truss structure
class Node:
    def __init__(self, x_coord=1, y_coord=1, x_restraint="", y_restraint="", x_dof=1, y_dof=1, x_displacement="",
                 y_displacement="", x_force="", y_force="", settlement=1):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_restraint = x_restraint
        self.y_restraint = y_restraint
        self.x_dof = x_dof
        self.y_dof = y_dof
        self.x_displacement = x_displacement
        self.y_displacement = y_displacement
        self.x_force = x_force
        self.y_force = y_force
        self.settlement = settlement


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


# Getting node and member information
node_count = int(input("How many nodes are there in your Truss? "))
member_count = int(input("How many members are there in your Truss? "))

for i in range(node_count):
    truss_nodes.append("")
    truss_nodes[i] = Node()
    truss_nodes[i].x_restraint = input(f"is the node {i+1} restrained in the x direction? (yes) or (no): ")
    truss_nodes[i].y_restraint = input(f"is the node {i+1} restrained in the y direction? (yes) or (no): ")

for i in range(member_count):
    truss_members.append("")
    truss_members[i] = Members()

# Getting the area and EI values of every member
constant_area = input("Are the cross-sectional areas of all members constant? (yes) or (no) ")
constant_ei_value = input("Are the EI values of all members constant? (yes) or (no) ")

# Displacement in a particular direction is zero, when the support prevents movement in that direction
# Otherwise, displacement in a particular direction is unknown

# Setting the default values of nodal displacements and forces as unknowns
for i in range(node_count):
    truss_nodes[i].x_displacement, truss_nodes[i].y_displacement, truss_nodes[i].x_force, truss_nodes[i].y_force = \
        symbols(f"Dx[{i+1}] Dy[{i+1}] Qx[{i+1}] Qy[{i+1}]")

unknowns = []  # To contain the unknown forces we have to solve for at the end

# Getting settlement and nodal force data
for i in range(node_count):
    loaded_node = input(f"Is there any external force acting on node {i + 1}? (yes) or (no): ")
    node_settlement = input(f"Is there any settlement at the node {i + 1}? (yes) or (no): ")

    if truss_nodes[i].x_restraint == "yes" and truss_nodes[i].y_restraint == "yes":
        unknowns.append(truss_nodes[i].x_force)
        unknowns.append(truss_nodes[i].y_force)
        if node_settlement == "yes":
            truss_nodes[i].x_displacement = int(input(f"What is the value of settlement in the x direction at node"
                                                      f" {i + 1}? "))
            truss_nodes[i].y_displacement = int(input(f"What is the value of settlement in the y direction at node"
                                                      f" {i + 1}? "))
        elif node_settlement == "no":
            truss_nodes[i].x_displacement = 0
            truss_nodes[i].y_displacement = 0

    elif truss_nodes[i].x_restraint == "yes" and truss_nodes[i].y_restraint == "no":
        unknowns.append(truss_nodes[i].x_force)
        unknowns.append(truss_nodes[i].y_displacement)
        if node_settlement == "yes":
            truss_nodes[i].x_displacement = int(input(f"What is the value of settlement in the x direction at node"
                                                      f" {i + 1}? "))
        elif node_settlement == "no":
            truss_nodes[i].x_displacement = 0

        if loaded_node == "yes":
            truss_nodes[i].y_force = int(input(f"What is the value of the external force in the y direction at node"
                                               f" {i + 1}? "))

        elif loaded_node == "no":
            truss_nodes[i].y_force = 0

    elif truss_nodes[i].y_restraint == "yes" and truss_nodes[i].x_restraint == "no":
        unknowns.append(truss_nodes[i].y_force)
        unknowns.append(truss_nodes[i].x_displacement)
        if node_settlement == "yes":
            truss_nodes[i].y_displacement = int(input(f"What is the value of settlement in the y direction at node"
                                                      f" {i + 1}? "))
        elif node_settlement == "no":
            truss_nodes[i].y_displacement = 0
        if loaded_node == "yes":
            truss_nodes[i].x_force = int(input(f"What is the value of the external force in the x direction at node"
                                               f" {i + 1}? "))
        elif loaded_node == "no":
            truss_nodes[i].x_force = 0

    elif truss_nodes[i].x_restraint == "no" and truss_nodes[i].y_restraint == "no":
        unknowns.append(truss_nodes[i].x_displacement)
        unknowns.append(truss_nodes[i].y_displacement)
        if loaded_node == "yes":
            truss_nodes[i].x_force = int(input(f"What is the value of the external force in the x direction at node"
                                               f" {i + 1}? "))
            truss_nodes[i].y_force = int(input(f"What is the value of the external force in the y direction at node"
                                               f" {i + 1}? "))
        elif loaded_node == "no":
            truss_nodes[i].x_force = 0
            truss_nodes[i].y_force = 0

# Including every node and member into lists, and making them an instance of their respective classes
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

# Adding all the members stiffness matrices to get the structural stiffness matrix
struct_stiffness_matrix = np.zeros((2 * node_count, 2 * node_count))
for i in range(member_count):
    struct_stiffness_matrix = np.add(struct_stiffness_matrix, truss_members[i].stiffness_matrix)


# Creating the one-column displacement matrix
displacement_matrix = []
T_displacement_matrix = []  # Transposed displacement matrix
for i in range(node_count):
    displacement_matrix.append(truss_nodes[i].x_displacement)
    displacement_matrix.append(truss_nodes[i].y_displacement)
for element in displacement_matrix:
    T_displacement_matrix.append([element])

stiffness_x_displacement_matrix = np.matmul(struct_stiffness_matrix, T_displacement_matrix)

final_equations = []

for i in range(node_count):
    equation1 = Eq(stiffness_x_displacement_matrix[(2*(i+1))-2, 0], truss_nodes[i].x_force)
    equation2 = Eq(stiffness_x_displacement_matrix[(2*(i+1))-1, 0], truss_nodes[i].y_force)

    final_equations.append(equation1)
    final_equations.append(equation2)

# gives the unknown forces and displacement in the structure
solution = solve(tuple(final_equations), tuple(unknowns))

print(solution)
print(unknowns)