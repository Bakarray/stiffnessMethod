import tkinter as tk
import Beams
from tkinter import ttk

length = 0
node_num = 0
load_num = 0
moment_num = 0
node_data = []
loads = []
moments = []


# on click of load button
def load_btn_click(master, input_frame):
    # create a window for entering the load details
    loads_btn_window = tk.Toplevel(master)
    loads_btn_window.title('Load details')

    # create an empty array to hold the load details
    loadings = []
    applied_moments = []
    moment_pos_entry = []
    moment_mag_entry = []

    # create entry fields for the load and moment data
    load_num_label = tk.Label(loads_btn_window, text='Number of load(s) on the beam:')
    load_num_label.grid(row=0, column=0, padx=10, pady=10)
    load_num_entry = tk.Entry(loads_btn_window)
    load_num_entry.insert(0, '0')
    load_num_entry.grid(row=0, column=1, padx=10, pady=10)

    moment_num_label = tk.Label(loads_btn_window, text='Number of point moment(s) on the beam:')
    moment_num_label.grid(row=1, column=0, padx=10, pady=10)
    moment_num_entry = tk.Entry(loads_btn_window)
    moment_num_entry.insert(0, '0')
    moment_num_entry.grid(row=1, column=1, padx=10, pady=10)

    # after getting the number of loads, get basic info about each load
    def get_load_info():
        global load_num, moment_num, loads
        current_type = []
        type_entry = []
        detail_buttons = []

        # store the number of loads
        loads_submit_btn1.grid_forget()
        load_num = int(load_num_entry.get())
        moment_num = int(moment_num_entry.get())

        # get the basic info about each load
        for i in range(load_num):
            current_type.append(tk.StringVar())
            type_label = tk.Label(load_info_frame, text=f"Load{i + 1}   type:")
            type_label.grid(row=i, column=0, padx=5, pady=5)

            type_entry.append(ttk.Combobox(load_info_frame,
                                           values=['Point_Load', 'Uniformly_distributed_load'],
                                           state='readonly', textvariable=current_type[i]))
            type_entry[i].current(0)
            type_entry[i].grid(row=i, column=1, padx=5, pady=5)

            detail_buttons.append(tk.Button
                                  (load_info_frame, text='add details', bg='grey', fg='white',
                                   command=lambda idx=i: get_load_details(detail_buttons, idx,
                                                                          current_type[idx].get())))
            detail_buttons[i].grid(row=i, column=2, padx=5, pady=5)

            loadings.append({'type': current_type[i].get()})

        # get basic info about each moment
        for i in range(moment_num):
            moment_mag_label = tk.Label(load_info_frame, text=f"Moment{i + 1}   Magnitude:")
            moment_mag_label.grid(row=load_num + i, column=0, padx=5, pady=5)
            moment_mag_entry.append(tk.Entry(load_info_frame))
            moment_mag_entry[i].insert(0, '0')
            moment_mag_entry[i].grid(row=load_num + i, column=1, padx=5, pady=5)

            moment_pos_label = tk.Label(load_info_frame, text=f"Position:")
            moment_pos_label.grid(row=load_num + i, column=2, padx=5, pady=5)
            moment_pos_entry.append(tk.Entry(load_info_frame))
            moment_pos_entry[i].insert(0, '0')
            moment_pos_entry[i].grid(row=load_num + i, column=3, padx=5, pady=5)

            applied_moments.append("")

        # Second details button to submit all info about the loads and moments
        load_submit_btn2 = tk.Button(load_info_frame, text='Submit', bg='grey', fg='white',
                                     command=lambda: submit_load_details())
        load_submit_btn2.grid(row=load_num + moment_num, column=0, columnspan=2, padx=5, pady=5)

    def submit_load_details():
        global loads

        load_index = 0
        for load in loadings:
            load_data_label = tk.Label(input_frame, text=f'Load {load_index + 1}:')
            load_data_label.grid(row=load_index, column=0, padx=5, pady=5)

            if load['type'] == 'p':
                loads.append({'type': load['type'], 'magnitude': float(load['magnitude'].get()),
                              'position': float(load['position'].get())})

                type_label = tk.Label(input_frame, text=f"Type: Point load")
                type_label.grid(row=load_index, column=1, padx=5, pady=5)

                magnitude_label = tk.Label(input_frame, text=f"Magnitude: {float(load['magnitude'].get())}")
                magnitude_label.grid(row=load_index, column=2, padx=5, pady=5)

                position_label = tk.Label(input_frame, text=f"Position: {float(load['position'].get())}")
                position_label.grid(row=load_index, column=3, padx=5, pady=5)

            elif load['type'] == 'd':
                loads.append({'type': load['type'], 'unit_load': float(load['unit_load'].get()),
                              'start': float(load['start'].get()), 'end': float(load['end'].get())})

                type_label = tk.Label(input_frame, text=f"Type: Distributed load")
                type_label.grid(row=load_index, column=1, padx=5, pady=5)

                unit_load_label = tk.Label(input_frame, text=f"Unit load: {float(load['unit_load'].get())}")
                unit_load_label.grid(row=load_index, column=2, padx=5, pady=5)

                start_pos_label = tk.Label(input_frame, text=f"Start: {float(load['start'].get())}")
                start_pos_label.grid(row=load_index, column=3, pady=5, padx=5)

                end_pos_label = tk.Label(input_frame, text=f"End: {float(load['end'].get())}")
                end_pos_label.grid(row=load_index, column=4, pady=5, padx=5)

            load_index += 1

        for moment_index in range(len(applied_moments)):
            applied_moments[moment_index] = {'magnitude': moment_mag_entry[moment_index].get(),
                                             'position': moment_pos_entry[moment_index].get()}

            moments.append({'position': float(applied_moments[moment_index]['position']),
                            'magnitude': float(applied_moments[moment_index]['magnitude'])})

            moment_data_label = tk.Label(input_frame, text=f'Applied moment {moment_index + 1}:')
            moment_data_label.grid(row=moment_index + load_num, column=0, padx=5, pady=5)

            magnitude_label = tk.Label(input_frame,
                                       text=f"Magnitude: {float(applied_moments[moment_index]['magnitude'])}")
            magnitude_label.grid(row=moment_index + load_num, column=1, padx=5, pady=5)

            position_label = tk.Label(input_frame, text=f"Position: {float(applied_moments[moment_index]['position'])}")
            position_label.grid(row=moment_index + load_num, column=2, padx=5, pady=5)

        loads_btn_window.destroy()

    def get_load_details(btn, idx, current_type):
        global load_num
        btn[idx].grid_forget()

        if current_type == 'Point_Load':
            loadings[int(idx)].update({'type': 'p', 'magnitude': '', 'position': ''})
            # create a label and entry box for the point load magnitude
            magnitude_label = tk.Label(load_info_frame, text='Magnitude (kn):')
            magnitude_label.grid(row=idx, column=2, padx=5, pady=5)
            loadings[int(idx)]['magnitude'] = tk.Entry(load_info_frame)
            loadings[int(idx)]['magnitude'].insert(0, '0')
            loadings[int(idx)]['magnitude'].grid(row=idx, column=3, padx=5, pady=5)

            position_label = tk.Label(load_info_frame, text='Position (m):')
            position_label.grid(row=idx, column=4, padx=5, pady=5)
            loadings[int(idx)]['position'] = tk.Entry(load_info_frame)
            loadings[int(idx)]['position'].insert(0, '0')
            loadings[int(idx)]['position'].grid(row=idx, column=5, padx=5, pady=5)

        elif current_type == 'Uniformly_distributed_load':
            loadings[int(idx)].update({'type': 'd', 'unit_load': '', 'start': '', 'end': ''})
            # create labels and entry boxes for the distributed load magnitude and span length
            unit_load_label = tk.Label(load_info_frame, text='Unit_Load:')
            unit_load_label.grid(row=idx, column=2, padx=5, pady=5)
            loadings[int(idx)]['unit_load'] = tk.Entry(load_info_frame)
            loadings[int(idx)]['unit_load'].insert(0, '0')
            loadings[int(idx)]['unit_load'].grid(row=idx, column=3, padx=5, pady=5)

            start_pos_label = tk.Label(load_info_frame, text='Start_pos (m):')
            start_pos_label.grid(row=idx, column=4, padx=5, pady=5)
            loadings[int(idx)]['start'] = tk.Entry(load_info_frame)
            loadings[int(idx)]['start'].insert(0, '0')
            loadings[int(idx)]['start'].grid(row=idx, column=5, padx=5, pady=5)

            end_pos_label = tk.Label(load_info_frame, text='End_pos (m):')
            end_pos_label.grid(row=idx, column=6, padx=5, pady=5)
            loadings[int(idx)]['end'] = tk.Entry(load_info_frame)
            loadings[int(idx)]['end'].insert(0, '0')
            loadings[int(idx)]['end'].grid(row=idx, column=7, padx=5, pady=5)

    # button to submit the number of loads and moments
    loads_submit_btn1 = tk.Button(loads_btn_window, text='Submit', bg='grey', fg='white', command=get_load_info)
    loads_submit_btn1.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Create a frame for the load details
    load_info_frame = tk.Frame(loads_btn_window)
    load_info_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def nodes_btn_click(master, input_frame):
    position_entry = []
    support_entry = []
    settlement_entry = []

    def submit_details(num):
        global node_data
        node_data = []
        for i in range(num):
            node_data.append({'position': position_entry[i].get(), 'support': support_entry[i].get(),
                              'settlement': settlement_entry[i].get()})
            node_data_label = tk.Label(input_frame, text=f'Node {i + 1}:')
            node_data_label.grid(row=i, column=0, padx=5, pady=5)

            position_label = tk.Label(input_frame, text=f'Position: {position_entry[i].get()}')
            position_label.grid(row=i, column=1, padx=5, pady=5)

            support_label = tk.Label(input_frame, text=f'Support: {support_entry[i].get()}')
            support_label.grid(row=i, column=2, padx=5, pady=5)

            settlement_label = tk.Label(input_frame, text=f'Settlement: {settlement_entry[i].get()}')
            settlement_label.grid(row=i, column=4, padx=5, pady=5)

        nodes_btn_window.destroy()

    def get_node_details():
        global node_num, node_data

        nodes_submit_btn.grid_forget()
        node_num = int(node_num_entry.get())

        for i in range(node_num):
            # Node label
            node_label = tk.Label(support_info_frame, text=f'Details for node {i + 1}:')
            node_label.grid(row=i, column=0, padx=5, pady=5)

            # Position input
            position_label = tk.Label(support_info_frame, text='Position (m):')
            position_label.grid(row=i, column=1, padx=5, pady=5)
            position_entry.append(tk.Entry(support_info_frame))
            position_entry[i].insert(0, '0.0')
            position_entry[i].grid(row=i, column=2, padx=5, pady=5)

            # Support input
            support_label = tk.Label(support_info_frame, text='Support:')
            support_label.grid(row=i, column=3, padx=5, pady=5)
            support_entry.append(ttk.Combobox(support_info_frame, values=['Fixed', 'Pinned', 'Roller', 'Free'],
                                              state='readonly'))
            support_entry[i].current(3)
            support_entry[i].grid(row=i, column=4, padx=5, pady=5)

            # Settlement input
            settlement_label = tk.Label(support_info_frame, text='Settlement (m):')
            settlement_label.grid(row=i, column=5, padx=5, pady=5)
            settlement_entry.append(tk.Entry(support_info_frame))
            settlement_entry[i].insert(0, '0.0')
            settlement_entry[i].grid(row=i, column=6, padx=5, pady=5)

        details_submit_btn = tk.Button(nodes_btn_window, text='Submit', bg='grey', fg='white',
                                       command=lambda: submit_details(node_num))
        details_submit_btn.grid(row=node_num, column=0, columnspan=2, padx=5, pady=5)

    nodes_btn_window = tk.Toplevel(master)
    nodes_btn_window.title('Node details')

    node_num_label = tk.Label(nodes_btn_window, text='Number of nodes on the beam:')
    node_num_label.grid(row=0, column=0, padx=10, pady=10)
    node_num_entry = tk.Entry(nodes_btn_window)
    node_num_entry.insert(0, '0.0')
    node_num_entry.grid(row=0, column=1, padx=10, pady=10)

    nodes_submit_btn = tk.Button(nodes_btn_window, text='Submit', bg='grey', fg='white',
                                 command=get_node_details)
    nodes_submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Create a frame for the support details
    support_info_frame = tk.Frame(nodes_btn_window)
    support_info_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


def beam_btn_click(master, input_label):
    beam_btn_window = tk.Toplevel(master)
    beam_btn_window.title('Beam Details')

    length_label = tk.Label(beam_btn_window, text='Total length of the beam:')
    length_label.grid(row=0, column=0, padx=10, pady=10)

    length_entry = tk.Entry(beam_btn_window)
    length_entry.insert(0, '0.0')
    length_entry.grid(row=0, column=1, padx=10, pady=10)

    def submit_length():
        global length
        length = float(length_entry.get())
        beam_btn_window.destroy()
        # Update the user_input_frame with the value entered by the user
        input_label.config(text=f"Length: {length} meters")

    len_submit_btn = tk.Button(beam_btn_window, text='Submit', bg='grey', fg='white', command=submit_length)
    len_submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


# on click of beam analysis button
def start_beam_analysis():
    beam_analysis_window = tk.Toplevel(window)
    beam_analysis_window.title('Beam info')

    # Get the screen size and make window full screen
    screen_width = beam_analysis_window.winfo_screenwidth()
    screen_height = beam_analysis_window.winfo_screenheight()
    beam_analysis_window.geometry(f"{screen_width}x{screen_height}+0+0")

    def analyze_beam():
        Beams.perform_beam_analysis(length, node_num, load_num, moment_num, node_data, loads, moments)

    # Positioning all the buttons and labels on screen
    model_label = tk.Label(beam_analysis_window, text="Model")
    model_label.grid(column=0, row=0, padx=5, pady=5)

    beam_btn = tk.Button(beam_analysis_window, text='Beam', bg='grey', fg='white', justify="center", width=20, height=5,
                         command=lambda: beam_btn_click(beam_analysis_window, length_input))
    beam_btn.grid(column=0, row=1, padx=5, pady=5)

    nodes_btn = tk.Button(beam_analysis_window, text='Nodes', bg='grey', fg='white', justify="center",
                          width=20, height=5, command=lambda: nodes_btn_click(beam_analysis_window, nodes_input_frame))
    nodes_btn.grid(column=0, row=2, padx=5, pady=5)

    loads_label = tk.Label(beam_analysis_window, text="Loads and Moments")
    loads_label.grid(column=1, row=0, padx=5, pady=5)

    loads_btn = tk.Button(beam_analysis_window, text='Loads', bg='grey', fg='white', justify="center",
                          width=20, height=5, command=lambda: load_btn_click(beam_analysis_window, loads_input_frame))
    loads_btn.grid(column=1, row=1, padx=5, pady=5, rowspan=2)

    beam_analysis_window.columnconfigure(0, weight=1)
    beam_analysis_window.columnconfigure(1, weight=1)

    # Create a LabelFrame to display user input
    user_input_label = tk.Label(beam_analysis_window, text='Beam Details')
    user_input_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # To display user input on the home screen
    length_input = tk.Label(beam_analysis_window, text='Length: ')
    length_input.grid(row=4, column=0, padx=5, pady=5)

    nodes_input_frame = tk.LabelFrame(beam_analysis_window, text='Nodes: ')
    nodes_input_frame.grid(row=5, column=0, padx=5, pady=5)

    loads_input_frame = tk.LabelFrame(beam_analysis_window, text='Loads')
    loads_input_frame.grid(row=6, column=0, padx=5, pady=5)

    moment_input_frame = tk.LabelFrame(beam_analysis_window, text='Point moment')
    moment_input_frame.grid(row=7, column=0, padx=5, pady=5)

    analyze_button = tk.Button(beam_analysis_window, text="Analyze", bg='grey', fg='white', command=analyze_beam)
    analyze_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)


# main window
window = tk.Tk()
window.geometry('400x400')
window.title('Structural Analysis')

# Start button on main window for BEAM analysis
button1 = tk.Button(window, text='Beam Analysis', width=20, height=5, bg='grey', fg='white',
                    command=start_beam_analysis)
button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()
