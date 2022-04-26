from sympy import symbols, Eq, solve

number_of_spans = int(input("how many spans does the beam have? "))
number_of_nodes = number_of_spans + 1
constant_ei = input("is the EI value constant for every span? (yes) or (no): ")


class Nodes:
    def __int__(self, rotational_displacement=0, vertical_displacement=0, support_condition="", vertical_loading=0,
                moment=0):
        self.rotational_displacement = rotational_displacement
        self.vertical_displacement = vertical_displacement
        self.support_condition = support_condition
        self.vertical_loading = vertical_loading
        self.moment = moment


beam_nodes = []
for i in range(number_of_nodes):
    beam_nodes.append("")
    beam_nodes[i] = Nodes()


class Spans:
    def __init__(self, span_length=0, loading_condition="", ei_value="", left_fem_y="", right_fem_y="", left_fem_z="",
                 right_fem_z="", load=0):
        self.ei_value = ei_value
        self.span_length = span_length
        self.loading_condition = loading_condition
        self.left_fem_y = left_fem_y
        self.left_fem_z = left_fem_z
        self.right_fem_y = right_fem_y
        self.right_fem_z = right_fem_z
        self.load = load


beam_spans = []
for i in range(number_of_spans):
    beam_spans.append("")
    beam_spans[i] = Spans()

# First, we need to get the span parameters needed for the final equations
# they include: FEM loads and moments, length, loading condition, load magnitude, and the EI_value
if constant_ei == "yes":
    for i in range(number_of_spans):
        beam_spans[i].ei_value = symbols("EI")
elif constant_ei == "no":
    print("The stiffness value varies for each span")
    for i in range(number_of_spans):
        beam_spans[i].ei_value = int(input(f"what is the EI value for span {i+1}: "))

# the fixed end moments are calculated based on the loading conditions
print("Key words for loading condition:"
      "\nNo loading on span (none)"
      "\nPoint load at center (P_C)"
      "\nPoint load at distance 'a' from left end and 'b' from the right end (P_X)"
      "\nTwo equal point loads, spaced at 1/3 of the total length from each other (P_C_2)"
      "\nThree equal point loads, spaced at 1/4 of the total length from each other (P_C_3)"
      "\nUniformly distributed load over the whole length (UDL)"
      "\nUniformly distributed load over half of the span on the right side (UDL/2_R)"
      "\nUniformly distributed load over half of the span on the left side (UDL/2_L)"
      "\nVariably distributed load, with highest point on the right end (VDL_R)"
      "\nVariably distributed load, with highest point on the left end (VDL_L)"
      "\nVariably distributed load, with highest point at the center (VDL_C)")

for i in range(number_of_spans):
    beam_spans[i].loading_condition = input(f"what is the loading condition of span {i + 1}? ")
    if beam_spans[i].loading_condition != "none":
        beam_spans[i].load = int(input(f"What is the magnitude of the load on span {i + 1}? "))
    else:
        beam_spans[i].load = 0

    beam_spans[i].span_length = int(input(f"what is the length of span {i + 1}? "))

    # The FEM loads(y) and moments(z)
    if beam_spans[i].loading_condition == 'UDL':
        beam_spans[i].left_fem_z = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 12
        beam_spans[i].right_fem_z = -1 * beam_spans[i].left_fem_z
        beam_spans[i].left_fem_y = (beam_spans[i].load * beam_spans[i].span_length) / 2
        beam_spans[i].right_fem_y = -1 * beam_spans[i].left_fem_y

    elif beam_spans[i].loading_condition == 'UDL/2_R':
        beam_spans[i].left_fem_z = (11 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[
            i].span_length) / 192
        beam_spans[i].right_fem_z = -1 * (5 * beam_spans[i].load * beam_spans[i].span_length *
                                          beam_spans[i].span_length) / 192
        beam_spans[i].left_fem_y = (beam_spans[i].load * beam_spans[i].span_length) / 8
        beam_spans[i].right_fem_y = (-3 * beam_spans[i].load * beam_spans[i].span_length) / 8

    elif beam_spans[i].loading_condition == 'UDL/2_L':
        beam_spans[i].left_fem_z = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[
            i].span_length) / 192
        beam_spans[i].right_fem_z = -1 * (11 * beam_spans[i].load * beam_spans[i].span_length *
                                          beam_spans[i].span_length) / 192
        beam_spans[i].left_fem_y = (3 * beam_spans[i].load * beam_spans[i].span_length) / 8
        beam_spans[i].right_fem_y = (-1 * beam_spans[i].load * beam_spans[i].span_length) / 8

    elif beam_spans[i].loading_condition == 'VDL_R':
        beam_spans[i].left_fem_z = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20
        beam_spans[i].right_fem_z = -1 * (
                    beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
        beam_spans[i].left_fem_y = (beam_spans[i].load * beam_spans[i].span_length) / 6
        beam_spans[i].right_fem_y = (-1 * beam_spans[i].load * beam_spans[i].span_length) / 3

    elif beam_spans[i].loading_condition == 'VDL_L':
        beam_spans[i].left_fem_z = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
        beam_spans[i].right_fem_z = -1 * (
                    beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20
        beam_spans[i].left_fem_y = (beam_spans[i].load * beam_spans[i].span_length) / 3
        beam_spans[i].right_fem_y = (-1 * beam_spans[i].load * beam_spans[i].span_length) / 6

    elif beam_spans[i].loading_condition == 'VDL_C':
        beam_spans[i].left_fem_z = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 96
        beam_spans[i].right_fem_z = -1 * beam_spans[i].left_fem_z
        beam_spans[i].left_fem_y = (beam_spans[i].load * beam_spans[i].span_length) / 4
        beam_spans[i].right_fem_y = -1 * beam_spans[i].left_fem_y

    elif beam_spans[i].loading_condition == "none":
        beam_spans[i].left_fem_z = 0
        beam_spans[i].right_fem_z = 0
        beam_spans[i].left_fem_y = 0
        beam_spans[i].right_fem_y = 0

# every node on the beam has an equation, and there are three equations for the first, last and intermediate nodes
# we also need to know the support condition for the nodes for later calculations

# The equations for each node will be put into the 'final_equations' list and be solved simultaneously
# The equations will be solved for the members in the 'unknowns' list
final_equations = []
unknowns = []

print('''Enter one of the following for support conditions
     "fixed" or "roller" or "pinned" or "joint"''')
for i in range(number_of_nodes):
    # to get the values of the displacement and forces at each of the nodes (known or unknown)
    beam_nodes[i].support_condition = input(f"What is the support condition for node {i + 1}? ")
    loaded_node = input(f"Is there any force or moment acting on node {i + 1}? (yes) or (no): ")
    if loaded_node == "yes":
        beam_nodes[i].vertical_loading = int(input(f"Magnitude of vertical force acting on node {i + 1}: "))
        beam_nodes[i].moment = int(input(f"Magnitude of moment acting on the node {i + 1}: "))
        beam_nodes[i].vertical_displacement = symbols(f"Dy_{i + 1}")
        beam_nodes[i].rotational_displacement = symbols(f"Dz_{i + 1}")
        unknowns.append(beam_nodes[i].vertical_displacement)
        unknowns.append(beam_nodes[i].rotational_displacement)

    elif loaded_node == "no" and beam_nodes[i].support_condition != "joint":
        beam_nodes[i].vertical_loading = symbols(f"Qy_{i + 1}")
        unknowns.append(beam_nodes[i].vertical_loading)
        beam_nodes[i].vertical_displacement = 0
        if beam_nodes[i].support_condition == "moment":
            beam_nodes[i].moment = symbols(f"Qz_{i + 1}")
            unknowns.append(beam_nodes[i].moment)
            beam_nodes[i].rotational_displacement = 0
        else:
            beam_nodes[i].moment = 0
            beam_nodes[i].rotational_displacement = symbols(f"Dz_{i + 1}")
            unknowns.append(beam_nodes[i].rotational_displacement)

    else:
        beam_nodes[i].vertical_loading = 0
        beam_nodes[i].moment = 0
        beam_nodes[i].vertical_displacement, beam_nodes[i].rotational_displacement = symbols(f"Dy_{i + 1} Dz_{i + 1}")
        unknowns.append(beam_nodes[i].vertical_displacement)
        unknowns.append(beam_nodes[i].rotational_displacement)

    # adding the x and y-axis equations for each node to the 'final_equations' list

for i in range(number_of_nodes):
    # for the first node
    if i == 0:
        final_equations.append(Eq(((12 * beam_nodes[i].vertical_displacement / (beam_spans[i].span_length ** 3)) +
                                   (6 * beam_nodes[i].rotational_displacement / (beam_spans[i].span_length ** 2)) - (
                                               12 * beam_nodes[1 + 1].vertical_displacement / (
                                                   beam_spans[i].span_length ** 3)) + (
                                               6 * beam_nodes[i + 1].rotational_displacement / (
                                                   beam_spans[i].span_length ** 2))) * beam_spans[i].ei_value +
                                  beam_spans[i].left_fem_y, beam_nodes[i].vertical_loading))
        final_equations.append(Eq(((6 * beam_nodes[i].vertical_displacement / (beam_spans[i].span_length ** 2)) + (
                    4 * beam_nodes[i].rotational_displacement / beam_spans[i].span_length) - (
                                               6 * beam_nodes[1 + 1].vertical_displacement / (
                                                   beam_spans[i].span_length ** 2)) + (
                                               2 * beam_nodes[i + 1].rotational_displacement / beam_spans[
                                           i].span_length)) * beam_spans[i].ei_value + beam_spans[i].left_fem_z,
                                  beam_nodes[i].moment))

    # for the last node
    elif i == (number_of_nodes - 1):
        final_equations.append(Eq(((-12 * beam_nodes[i].vertical_displacement / (
                    beam_spans[i - 1].span_length ** 3)) + (-6 * beam_nodes[i].rotational_displacement / (
                    beam_spans[i - 1].span_length ** 2)) + (12 * beam_nodes[1 + 1].vertical_displacement / (
                    beam_spans[i - 1].span_length ** 3)) - (6 * beam_nodes[i + 1].rotational_displacement / (
                    beam_spans[i - 1].span_length ** 2))) * beam_spans[i - 1].ei_value + beam_spans[i - 1].right_fem_y,
                                  beam_nodes[i].vertical_loading))
        final_equations.append(Eq(((6 * beam_nodes[i].vertical_displacement / (beam_spans[i - 1].span_length ** 2)) + (
                    2 * beam_nodes[i].rotational_displacement / beam_spans[i - 1].span_length) - (
                                               6 * beam_nodes[1 + 1].vertical_displacement / (
                                                   beam_spans[i - 1].span_length ** 2)) + (
                                               4 * beam_nodes[i + 1].rotational_displacement / beam_spans[
                                           i - 1].span_length)) * beam_spans[i - 1].ei_value + beam_spans[
                                      i - 1].right_fem_z, beam_nodes[i].moment))

    # for intermediate nodes
    else:
        final_equations.append(Eq((((-12 * beam_nodes[i - 1].vertical_displacement / (
                    beam_spans[i - 1].span_length ** 3)) - (6 * beam_nodes[i - 1].rotational_displacement / (
                    beam_spans[i - 1].span_length ** 2)) + (12 * beam_nodes[i].vertical_displacement / (
                    beam_spans[i - 1].span_length ** 3)) - (6 * beam_nodes[i].rotational_displacement / (
                    beam_spans[i - 1].span_length ** 2))) * beam_spans[i - 1].ei_value) + (((-12 * beam_nodes[
            i].vertical_displacement / (beam_spans[i].span_length ** 3)) + (6 * beam_nodes[
            i].rotational_displacement / (beam_spans[i].span_length ** 2)) - (12 * beam_nodes[
            i + 1].vertical_displacement / (beam_spans[i].span_length ** 3)) + (6 * beam_nodes[
            i].vertical_displacement / (beam_spans[i].span_length ** 2))) * beam_spans[i].ei_value + beam_spans[
                                                                                               i - 1].right_fem_y +
                                                                                           beam_spans[i].left_fem_y),
                                  beam_nodes[i].vertical_loading))
        final_equations.append(Eq((((6 * beam_nodes[i - 1].vertical_displacement / (
                    beam_spans[i - 1].span_length ** 3)) + (2 * beam_nodes[i - 1].rotational_displacement / beam_spans[
            i - 1].span_length) - (6 * beam_nodes[i].vertical_displacement / (beam_spans[i - 1].span_length ** 3)) + (
                                                4 * beam_nodes[i].rotational_displacement / (
                                                    beam_spans[i - 1].span_length ** 2))) * beam_spans[
                                       i - 1].ei_value) + (((6 * beam_nodes[i].vertical_displacement / (
                    beam_spans[i].span_length ** 2)) + (4 * beam_nodes[i].rotational_displacement / beam_spans[
            i].span_length) - (6 * beam_nodes[i + 1].vertical_displacement / (beam_spans[i].span_length ** 2)) + (
                                                                        2 * beam_nodes[i].vertical_displacement / (
                                                                            beam_spans[i].span_length ** 2))) *
                                                           beam_spans[i].ei_value + beam_spans[i - 1].right_fem_z +
                                                           beam_spans[i].left_fem_z), beam_nodes[i].moment))

solution = solve(tuple(final_equations), tuple(unknowns))

print(solution)
