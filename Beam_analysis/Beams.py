from sympy import symbols, Eq, solve
import seaborn as sns
import matplotlib.pyplot as plt


def perform_beam_analysis(ui_length, ui_node_num, ui_load_num, ui_moment_num, ui_node_data, ui_loads, ui_moments):
    # Creating classes to hold information about each span and node on the continuous beam
    class Spans:
        def __init__(self, length=0, left_fem_y=0, right_fem_y=0, left_fem_z=0, right_fem_z=0, loads=None, moments=None,
                     ei_value=1, imposed_moments=0, total_loads=0):
            self.length = length  # length of the beam
            self.left_fem_y = left_fem_y  # reaction on the left node due to span loading
            self.right_fem_y = right_fem_y  # reaction on the right node due to span loading
            self.left_fem_z = left_fem_z  # moment on the left node due to span loading
            self.right_fem_z = right_fem_z  # moment on the right node due to span loading
            self.loads = [] if loads is None else loads
            self.moments = [] if moments is None else moments
            self.ei_value = ei_value
            self.imposed_moments = imposed_moments
            self.total_loads = total_loads

    class Nodes:
        def __init__(self, disp_y=0, disp_z=0, supp_type='', supp_rxn_y=0, supp_rxn_z=0, node_load=0, node_moment=0,
                     fem_rxn_y=0, fem_rxn_z=0, node_position=0, node_settlement=0):
            self.settlement = node_settlement  # settlement applied at the node
            self.disp_y = disp_y  # vertical displacement of node
            self.disp_z = disp_z  # rotational displacement of node
            self.supp_type = supp_type  # support type
            self.supp_rxn_y = supp_rxn_y  # vertical support reaction
            self.supp_rxn_z = supp_rxn_z  # rotational support reaction
            self.node_load = node_load  # point load applied on the node
            self.node_moment = node_moment  # moment applied on the node
            self.fem_rxn_y = fem_rxn_y  # vertical reaction resulting from member loading
            self.fem_rxn_z = fem_rxn_z  # rotational reaction resulting from member loading
            self.node_position = node_position  # position of the node along the beam

    # print(f"length = {ui_length}")
    # print(f"node num = {ui_node_num}")
    # print(f"load num = {ui_load_num}")
    # print(f"node data = {ui_node_data}")
    # print(f"load data = {ui_loads}")
    # print(f"moment num = {ui_moment_num}")
    # print(f"moment data - {ui_moments}")

    # Creating a list to hold all the instances of nodes and spans on the beam
    node = []
    span = []

    # Getting beam information from the user
    # beam_length = UI.length
    # node_num = UI.node_num
    beam_length = float(ui_length)
    node_num = int(ui_node_num)
    span_num = node_num - 1

    for i in range(node_num):
        node.append(Nodes())
        node[i].node_position = float(ui_node_data[i]['position'])
        node[i].supp_type = ui_node_data[i]['support']
        node[i].settlement = float(ui_node_data[i]['settlement'])

    # To get the length of every span (they exist between nodes)
    for i in range(span_num):
        span.append(Spans(loads=[], moments=[]))
        span[i].length = node[i + 1].node_position - node[i].node_position

    # beam_loads = []  # A list to hold all the loads on the beam
    # load_num = int(input("How many loads are on the beam: "))
    # if load_num:
    #     print("Load type (keyword): point load (p), uniformly distributed loading (d), or triangular loading (t) ")
    beam_loads = ui_loads
    load_num = int(ui_load_num)

    # gets and stores information about the span loadings  in the span class
    # Sign convention: Loadings acting upward is positive, loadings acting downward is negative
    for i in range(load_num):
        # beam_loads.append({'type': input(f"Load {i + 1} type: ")})  # Asks the user for the type of each load
        if beam_loads[i]['type'] == 'p':
            # load_position, magnitude = map(float, input(f"load {i + 1} (position (m), magnitude (kn)) ").split(','))
            # beam_loads[i].update({'position': load_position, 'magnitude': magnitude})

            for j in range(node_num):
                if beam_loads[i]['position'] == node[j].node_position:  # checks if the load is acting on a node
                    node[j].node_load = beam_loads[i]['magnitude']
                    break

            for j in range(span_num):
                if node[j + 1].node_position > beam_loads[i]['position'] > node[j].node_position:
                    span[j].loads.append(beam_loads[i])
                    break

        if beam_loads[i]['type'] == 'd':
            # print("Enter the (start position, end position, unit load) of the uniformly distributed load")
            # start_position, end_position, unit_load = map(int,
            # input(f"load {i + 1} (start (m), end (m), unit load (kn/m)): ").
            #                                               split(','))
            # beam_loads[i].update({'start': start_position, 'end': end_position, 'unit_load': unit_load})
            for j in range(span_num):
                if (node[j].node_position <= beam_loads[i]['start'] < node[j + 1].node_position) \
                        and (beam_loads[i]['end'] <= node[j + 1].node_position):  # if udl does not cross over the span
                    # span[j].loads.append(beam_loads[i])
                    span[j].loads.append({'type': 'd', 'start': beam_loads[i]['start'], 'end': beam_loads[i]['end'],
                                          'unit_load': beam_loads[i]['unit_load']})
                    break

                elif (node[j].node_position <= beam_loads[i]['start'] < node[j + 1].node_position) \
                        and (beam_loads[i]['end'] > node[j + 1].node_position):  # if the udl crosses ove the span
                    # beam_loads[i]['end'] = node[j + 1].node_position
                    # span[j].loads.append(beam_loads[i])
                    span[j].loads.append({'type': 'd', 'start': beam_loads[i]['start'],
                                          'end': node[j + 1].node_position, 'unit_load': beam_loads[i]['unit_load']})

                elif (beam_loads[i]['end'] >= node[j + 1].node_position) \
                        and (
                        beam_loads[i]['start'] < node[j].node_position):  # udl starts b4 the span and ends after it
                    # beam_loads[i]['start'] = node[j].node_position
                    # beam_loads[i]['end'] = node[j + 1].node_position
                    # span[j].loads.append(beam_loads[i])
                    span[j].loads.append({'type': 'd', 'start': node[j].node_position,
                                          'end': node[j + 1].node_position, 'unit_load': beam_loads[i]['unit_load']})

                elif (beam_loads[i]['end'] < node[j + 1].node_position) \
                        and (beam_loads[i]['start'] < node[j].node_position):  # udl starts before span and ends on it
                    # beam_loads[i]['start'] = node[j].node_position
                    # span[j].loads.append(beam_loads[i])
                    span[j].loads.append({'type': 'd', 'start': node[j].node_position, 'end': beam_loads[i]['end'],
                                          'unit_load': beam_loads[i]['unit_load']})

    # Gets and stores information about the point moments on the beam
    # Sign convention: clockwise moments = positive; anticlockwise = negative
    beam_moments = ui_moments  # A list to hold all the point moments on the beam
    moment_num = ui_moment_num
    if moment_num:
        # print("Enter the magnitude and position of the point moments")

        for i in range(moment_num):
            # magnitude, position = map(float,
            # input(f"point moment {i + 1} (magnitude (kn.m), position (m): ").split(","))
            # beam_moments.append({'position': position, 'magnitude': magnitude})

            for n in node:  # if point moment is acting on a node
                if beam_moments[i]['position'] == n.node_position:
                    n.node_moment = beam_moments[i]['magnitude']
                    break

            for j in range(node_num):  # if point moment is acting on a span
                if node[j].node_position > beam_moments[i]['position'] > node[j - 1].node_position:
                    span[j - 1].moments.append(beam_moments[i])
                    break

    # Calculating the fixed end moments and reactions on each span due to applied loads
    for i in range(span_num):
        for loading in span[i].loads:
            if loading['type'] == 'p':
                p = loading['magnitude']
                b = node[i + 1].node_position - loading['position']
                a = loading['position'] - node[i].node_position
                l = span[i].length

                span[i].right_fem_z += -1 * (p * a * a * b) / (l * l)
                span[i].left_fem_z += (p * b * b * a) / (l * l)

                span[i].imposed_moments += p * b
                span[i].total_loads += p

                span[i].left_fem_y = span[i].imposed_moments / span[i].length
                span[i].right_fem_y = span[i].total_loads - span[i].left_fem_y

            if loading['type'] == 'd':
                w = loading['unit_load']
                a = loading['start'] - node[i].node_position
                b = loading['end'] - node[i].node_position
                l = span[i].length

                span[i].right_fem_z += -1 * (w / (l ** 2)) * (
                        ((l / 3) * ((b ** 3) - (a ** 3))) - ((1 / 4) * ((b ** 4) - (a ** 4))))

                span[i].left_fem_z += (w / l ** 2) * (
                        (((l ** 2) / 2) * ((b ** 2) - (a ** 2))) - ((2 * l / 3) * ((b ** 3) - (a ** 3))) +
                        ((1 / 4) * ((b ** 4) - (a ** 4))))

                span[i].total_loads += w * (b - a)
                span[i].imposed_moments += span[i].total_loads * (((b - a) / 2) +
                                                                  (node[i + 1].node_position - loading['end']))

                span[i].left_fem_y = span[i].imposed_moments / span[i].length
                span[i].right_fem_y = span[i].total_loads - span[i].left_fem_y

        span[i].left_fem_y = round(span[i].left_fem_y, 2)
        span[i].right_fem_y = round(span[i].right_fem_y, 2)
        span[i].left_fem_z = round(span[i].left_fem_z, 2)
        span[i].right_fem_z = round(span[i].right_fem_z, 2)
    """
        print(f"left fem_y span[{i}]: {span[i].left_fem_y}")
        print(f"left fem_z span[{i}]: {span[i].left_fem_z}")
        print(f"right fem_y span[{i}]: {span[i].right_fem_y}")
        print(f"right fem_z span[{i}]: {span[i].right_fem_z}")
    """

    # Calculating the fixed end moments and reactions on each span due to applied moments
    for i in range(span_num):
        for moment in span[i].moments:
            m = moment['magnitude']
            a = moment['position'] - node[i].node_position
            b = node[i + 1].node_position - moment['position']
            l = span[i].length

            span[i].left_fem_z += (m * b / l ** 2) * ((2 * a) - b)
            span[i].right_fem_z += (m * a / l ** 2) * ((2 * b) - a)
            span[i].left_fem_y += (-6 * m * a * b) / l ** 3
            span[i].right_fem_y += (6 * m * a * b) / l ** 3

    # getting the reactions and moments at each node resulting from the member loadings
    for i in range(node_num):
        if i == 0:
            node[i].fem_rxn_y = span[i].left_fem_y
            node[i].fem_rxn_z = span[i].left_fem_z
        elif i == (node_num - 1):
            node[i].fem_rxn_y = span[i - 1].right_fem_y
            node[i].fem_rxn_z = span[i - 1].right_fem_z
        else:
            node[i].fem_rxn_y = span[i - 1].right_fem_y + span[i].left_fem_y
            node[i].fem_rxn_z = span[i - 1].right_fem_z + span[i].left_fem_z

        """print(f"moment at node [{i}] = {node[i].fem_rxn_z}")
        print(f"reaction at node [{i}] = {node[i].fem_rxn_y}")"""

    # The equations for each node will be put into the 'final_equations' list and be solved simultaneously
    # The equations will be solved for the members in the 'unknowns' list
    final_equations = []
    unknowns = []

    # getting the node reactions or displacements that are known and unknown
    for i in range(node_num):
        # to get the values of the displacement and forces at each of the nodes (known or unknown)
        if node[i].supp_type == 'Fixed':
            node[i].supp_rxn_y, node[i].supp_rxn_z = symbols(f"vertical_reaction_at_node_{i + 1} "
                                                             f"rotational_reaction_at_node_{i + 1}")
            unknowns.append(node[i].supp_rxn_y)
            unknowns.append(node[i].supp_rxn_z)

        elif node[i].supp_type == 'Pinned' or node[i].supp_type == 'Roller':
            node[i].supp_rxn_y, node[i].disp_z = symbols(f"vertical_reaction_at_node_{i + 1} "
                                                         f"rotational_displacement_at_node_{i + 1}")
            unknowns.append(node[i].supp_rxn_y)
            unknowns.append(node[i].disp_z)

        elif node[i].supp_type == 'Free':
            node[i].disp_y, node[i].disp_z = symbols(f"vertical_displacement_at_node_{i + 1} "
                                                     f"rotational_displacement_at_node_{i + 1}")
            unknowns.append(node[i].disp_y)
            unknowns.append(node[i].disp_z)

    # add moment caused by overhanging span to supp_rxn_z
    for i in range(len(node)):
        if i == 0 and node[i].supp_type == 'n':
            node[i + 1].supp_rxn_z -= node[i].node_load * span[i].length

            for load in span[i].loads:
                if load['type'] == 'p':
                    node[i + 1].supp_rxn_z -= load['magnitude'] * (node[i + 1].node_position - load['position'])
                elif load['type'] == 'd':
                    udl_width = load['end'] - load['start']
                    node[i + 1].supp_rxn_z -= load['unit_load'] * udl_width * udl_width / 2

        elif (i == len(node) - 1) and node[i].supp_type == 'n':
            node[i - 1].supp_rxn_z += node[i].node_load * span[i - 1].length

            for load in span[i - 1].loads:
                if load['type'] == 'p':
                    node[i - 1].supp_rxn_z += load['magnitude'] * (node[i + 1].node_position - load['position'])
                elif load['type'] == 'd':
                    udl_width = load['end'] - load['start']
                    node[i - 1].supp_rxn_z += load['unit_load'] * udl_width * udl_width / 2

    equation1 = ""
    equation2 = ""
    for i in range(node_num):
        # for the first node
        if i == 0:
            equation1 = Eq(((12 * node[i].disp_y / (span[i].length ** 3)) +
                            (6 * node[i].disp_z / (span[i].length ** 2)) -
                            (12 * node[i + 1].disp_y / (span[i].length ** 3)) +
                            (6 * node[i + 1].disp_z / (span[i].length ** 2))) * span[i].ei_value
                           + node[i].fem_rxn_y, (node[i].supp_rxn_y - node[i].node_load))
            equation2 = Eq(((6 * node[i].disp_y / (span[i].length ** 2)) +
                            (4 * node[i].disp_z / span[i].length) -
                            (6 * node[i + 1].disp_y / (span[i].length ** 2)) +
                            (2 * node[i + 1].disp_z / span[i].length)) * span[i].ei_value
                           + node[i].fem_rxn_z, (node[i].supp_rxn_z - node[i].node_moment))

        # for the last node
        elif i == (node_num - 1):
            equation1 = Eq((((-12 * node[i - 1].disp_y) / (span[i - 1].length ** 3)) +
                            (-6 * node[i - 1].disp_z / (span[i - 1].length ** 2)) +
                            (12 * node[i].disp_y / (span[i - 1].length ** 3)) -
                            (6 * node[i].disp_z / (span[i - 1].length ** 2))) * span[i - 1].ei_value
                           + node[i].fem_rxn_y, (node[i].supp_rxn_y - node[i].node_load))

            equation2 = Eq(((6 * node[i - 1].disp_y / (span[i - 1].length ** 2)) +
                            (2 * node[i - 1].disp_z / span[i - 1].length) -
                            (6 * node[i].disp_y / (span[i - 1].length ** 2)) +
                            (4 * node[i].disp_z / span[i - 1].length)) * span[i - 1].ei_value
                           + node[i].fem_rxn_z, (node[i].supp_rxn_z - node[i].node_moment))

        # for intermediate nodes
        else:
            equation1 = Eq((((-12 * node[i - 1].disp_y / (span[i - 1].length ** 3)) -
                             (6 * node[i - 1].disp_z / (span[i - 1].length ** 2)) +
                             (12 * node[i].disp_y / (span[i - 1].length ** 3)) -
                             (6 * node[i].disp_z / (span[i - 1].length ** 2))) * span[i - 1].ei_value)
                           + (((12 * node[i].disp_y / (span[i].length ** 3)) +
                               (6 * node[i].disp_z / (span[i].length ** 2)) -
                               (12 * node[i + 1].disp_y / (span[i].length ** 3)) +
                               (6 * node[i + 1].disp_z / (span[i].length ** 2))) * span[i].ei_value)
                           + node[i].fem_rxn_y, (node[i].supp_rxn_y - node[i].node_load))

            equation2 = Eq((((6 * node[i - 1].disp_y / (span[i - 1].length ** 2)) +
                             (2 * node[i - 1].disp_z / span[i - 1].length) -
                             (6 * node[i].disp_y / (span[i - 1].length ** 2)) +
                             (4 * node[i].disp_z / span[i - 1].length)) * span[i - 1].ei_value)
                           + (((6 * node[i].disp_y / (span[i].length ** 2)) +
                               (4 * node[i].disp_z / span[i].length) -
                               (6 * node[i + 1].disp_y / (span[i].length ** 2)) +
                               (2 * node[i + 1].disp_z / span[i].length)) * span[i].ei_value)
                           + node[i].fem_rxn_z, (node[i].supp_rxn_z - node[i].node_moment))

        final_equations.append(equation1)
        final_equations.append(equation2)

    solution = solve(tuple(final_equations), tuple(unknowns))

    def check_symbol(factor):
        return factor if type(factor) == int else solution.get(factor, 0)

    all_loads = []
    all_moments = []
    for i in range(node_num):
        y_displacement = check_symbol(node[i].disp_y)
        z_displacement = check_symbol(node[i].disp_z)
        y_reaction = check_symbol(node[i].supp_rxn_y)
        z_reaction = check_symbol(node[i].supp_rxn_z)

        all_loads += [{'type': 'rxn', 'position': node[i].node_position,
                       'magnitude': round(y_reaction, 3), 'node_load': node[i].node_load}]

        all_moments += [{'type': 'rxn', 'position': node[i].node_position,
                         'magnitude': round(z_reaction, 3), 'node_moment': node[i].node_moment}]

        # print(f"vertical displacement at node {i + 1} = {round(y_displacement, 3)}")
        # print(f"rotational displacement at node {i + 1} = {round(z_displacement, 3)}")
        print(f"vertical reaction at node {i + 1} = {round(y_reaction, 3)}")
        print(f"rotational reaction at node {i + 1} = {round(z_reaction, 3)}")

    for i in range(span_num):
        all_loads += span[i].loads
        all_moments += span[i].moments

    print(all_loads)
    print(all_moments)

    # Plotting the shear force and bending moment diagram
    sf_array = []
    x_array = []
    bm_array = []
    x2_array = []
    sf_label_coord = []
    bm_label_coord = []

    step = 0

    while step <= beam_length:
        forces_encountered = []
        imposed_moment = []

        for load in all_loads:
            if load['type'] == 'p' and load['position'] < round(step, 2):
                forces_encountered.append(-1 * load['magnitude'])
                imposed_moment.append(load['magnitude'] * (round(step, 2) - load['position']))

            if load['type'] == 'rxn' and load['position'] < round(step, 2):
                forces_encountered.append(load['magnitude'] - load['node_load'])
                imposed_moment.append(-1 * load['magnitude'] * (round(step, 2) - load['position']))

            if load['type'] == 'd' and load['start'] < round(step, 2):
                end = round(step, 2) if round(step, 2) < load['end'] else load['end']
                forces_encountered.append(-1 * load['unit_load'] * (end - load['start']))
                imposed_moment.append((load['unit_load'] * (end - load['start'])) *
                                      (((end - load['start']) / 2) + (round(step, 2) - end)))

        for moment in all_moments:
            if moment['position'] < round(step, 2):
                imposed_moment.append(moment['magnitude'])

        sf_array.append(sum(forces_encountered))
        x_array.append(round(step, 2))
        bm_array.append(sum(imposed_moment))
        x2_array.append(round(step, 2))

        # for sudden changes in shear force
        for load in all_loads:
            if load['type'] == 'p' and load['position'] == round(step, 2):
                forces_encountered.append(-1 * load['magnitude'])
                sf_label_coord.append((step, sum(forces_encountered)))  # sets the coordinate for labelling on the SFD
                bm_label_coord.append((step, sum(imposed_moment)))  # sets the coordinate for labelling on the BMD

            if load['type'] == 'rxn' and load['position'] == round(step, 2):
                forces_encountered.append(load['magnitude'] - load['node_load'])
                sf_label_coord.append((step, sum(forces_encountered)))  # sets the coordinate for labelling on the SFD
                bm_label_coord.append((step, sum(imposed_moment)))  # sets the coordinate for labelling on the BMD

            if load['type'] == 'd' and load['start'] == round(step, 2):
                forces_encountered.append(-1 * load['unit_load'] * (round(step, 2) - load['start']))

        # for sudden changes in moment
        for moment in all_moments:
            if moment['position'] == round(step, 2):
                imposed_moment.append(moment['magnitude'])

        sf_array.append(sum(forces_encountered))
        x_array.append(round(step, 2))
        bm_array.append(sum(imposed_moment))
        x2_array.append(round(step, 2))

        step += 0.1

    x_sf = x_array
    x_bm = x2_array
    y_sf = sf_array
    y_bm = bm_array
    span = beam_length

    sns.set_style('whitegrid')

    # Create the subplots
    fig, (ax_sf, ax_bm) = plt.subplots(2, 1, sharex='all', figsize=(8, 8))

    # Plot the shear force diagram on the first subplot
    ax_sf.plot(x_sf, y_sf, label='Shear Force', color='green')
    ax_sf.axhline(y=0, color='black', linewidth=1)
    ax_sf.set_ylabel('Shear Force (kN)')
    ax_sf.set_title('Shear Force and Bending Moment Diagrams')

    # Add shear force values as text annotations
    sf_points = sf_label_coord  # Example points to display shear force values
    print(sf_points)
    for point in sf_points:
        x, y = point
        if y < 0:
            va = 'top'
        else:
            va = 'bottom'
        ax_sf.text(x, y, '{:.2f}'.format(y), ha='center', va=va)

    # Plot the bending moment diagram on the second subplot
    ax_bm.plot(x_bm, y_bm, label='Bending Moment', color='blue')
    ax_bm.axhline(y=0, color='black', linewidth=1)
    ax_bm.set_xlabel('Distance (m)')
    ax_bm.set_ylabel('Bending Moment (kNm)')

    # Add bending moment values as text annotations
    bm_points = bm_label_coord  # Example points to display bending moment values
    for point in bm_points:
        x, y = point
        if y < 0:
            va = 'top'
        else:
            va = 'bottom'
        ax_bm.text(x, y, '{:.2f}'.format(y), ha='center', va=va)

    # Set the axis limits
    ax_sf.set_xlim([-1, span + 1])
    ax_bm.set_xlim([-1, span + 1])

    # Set the title and legend for the entire figure
    fig.suptitle('Shear Force and Bending Moment Diagrams')
    fig.legend()

    # Show the plot
    plt.show()

