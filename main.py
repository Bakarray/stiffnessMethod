from sympy import symbols, Eq

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
# they include: FEM loads and moments, length, loading condition, load magnitude
for i in range(number_of_spans):
    beam_spans[i].span_length = int(input(f"what is the length of span {i + 1}"))
    beam_spans[i].loading_condition = input(f"what is the loading condition of span {i + 1}")
    if beam_spans[i].loading_condition != "none":
        beam_spans[i].load = int(input(f"What is the magnitude of the load on span {i + 1}"))

    # The EI values
    if constant_ei == "yes":
        beam_spans[i].ei_value = symbols('EI')
    elif constant_ei == "no":
        beam_spans[i].ei_value = int(input(f"what is the value of EI for span {i + 1}"))

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
        beam_spans[i].right_fem_z = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)/30
        beam_spans[i].left_fem_y = (beam_spans[i].load * beam_spans[i].span_length) / 6
        beam_spans[i].right_fem_y = (-1 * beam_spans[i].load * beam_spans[i].span_length) / 3

    elif beam_spans[i].loading_condition == 'VDL_L':
        beam_spans[i].left_fem_z = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
        beam_spans[i].right_fem_z = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length)/20
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

# The equations for each node will be put into this list and be solved simultaneously
final_equations = []
for i in range(number_of_nodes):
    # to get the support conditions at each node
    beam_nodes[i].support_condition = input(f"What is the support condition for node {i + 1}")

    # adding the x and y-axis equations for each node to the 'final_equations' list
    if i == 0:
        final_equations.append(Eq(((12 * beam_nodes[i].vertical_displacement/(beam_spans[i].span_length**3)) + (6 * beam_nodes[i].rotational_displacement/(beam_spans[i].span_length**2)) - (12 * beam_nodes[1+1].vertical_displacement/(beam_spans[i].span_length**3)) + (6 * beam_nodes[i+1].rotational_displacement/(beam_spans[i].span_length**2)))*beam_spans[i].ei_value + beam_spans[i].left_fem_y, beam_nodes[i].vertical_loading))
        final_equations.append(Eq(((6 * beam_nodes[i].vertical_displacement/(beam_spans[i].span_length**2)) + (4 * beam_nodes[i].rotational_displacement/beam_spans[i].span_length) - (6 * beam_nodes[1+1].vertical_displacement/(beam_spans[i].span_length**2)) + (2 * beam_nodes[i+1].rotational_displacement/beam_spans[i].span_length))*beam_spans[i].ei_value + beam_spans[i].left_fem_z, beam_nodes[i].moment))

    elif i == (number_of_nodes - 1):
        final_equations.append(Eq(((-12 * beam_nodes[i].vertical_displacement/(beam_spans[i-1].span_length**3)) + (-6 * beam_nodes[i].rotational_displacement/(beam_spans[i-1].span_length**2)) + (12 * beam_nodes[1+1].vertical_displacement/(beam_spans[i-1].span_length**3)) - (6 * beam_nodes[i+1].rotational_displacement/(beam_spans[i-1].span_length**2)))*beam_spans[i-1].ei_value + beam_spans[i-1].right_fem_y, beam_nodes[i].vertical_loading))
        final_equations.append(Eq(((6 * beam_nodes[i].vertical_displacement/(beam_spans[i-1].span_length**2)) + (2 * beam_nodes[i].rotational_displacement/beam_spans[i-1].span_length) - (6 * beam_nodes[1+1].vertical_displacement/(beam_spans[i-1].span_length**2)) + (4 * beam_nodes[i+1].rotational_displacement/beam_spans[i-1].span_length))*beam_spans[i-1].ei_value + beam_spans[i-1].right_fem_z, beam_nodes[i].moment))

    else:
        final_equations.append(Eq((((-12*beam_nodes[i-1].vertical_displacement/(beam_spans[i-1].span_length**3)) - (6*beam_nodes[i-1].rotational_displacement/(beam_spans[i-1].span_length**2)) + (12*beam_nodes[i].vertical_displacement/(beam_spans[i].span_length**3)))*beam_spans[i-1].ei_value) + )
