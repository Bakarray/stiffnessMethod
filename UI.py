import tkinter as tk
from tkinter import ttk

length = None
node_num = None
load_num = None
moment_num = None
node_data = []
loads = []
moments = []


def load_btn_click(master):
    def get_load_details(btn, idx, current_type):
        target = btn[idx]
        target.grid_forget()

        if current_type == 'Point_Load':
            # create a label and entry box for the point load magnitude
            magnitude_label = tk.Label(load_info_frame, text='Magnitude (kn):')
            magnitude_label.grid(row=idx, column=3, padx=5, pady=5)
            magnitude_entry = tk.Entry(load_info_frame)
            magnitude_entry.grid(row=idx, column=4, padx=5, pady=5)

            position_label = tk.Label(load_info_frame, text='Position (m):')
            position_label.grid(row=idx, column=5, padx=5, pady=5)
            position_entry = tk.Entry(load_info_frame)
            position_entry.grid(row=idx, column=6, padx=5, pady=5)

        elif current_type == 'Point_Moment':
            # create a label and entry box for the point moment magnitude
            magnitude_label = tk.Label(load_info_frame, text='Magnitude (Kn.M):')
            magnitude_label.grid(row=idx, column=3, padx=5, pady=5)
            magnitude_entry = tk.Entry(load_info_frame)
            magnitude_entry.grid(row=idx, column=4, padx=5, pady=5)

            position_label = tk.Label(load_info_frame, text='Position (m):')
            position_label.grid(row=idx, column=5, padx=5, pady=5)
            position_entry = tk.Entry(load_info_frame)
            position_entry.grid(row=idx, column=6, padx=5, pady=5)

        elif current_type == 'Uniformly_distributed_load':
            # create labels and entry boxes for the distributed load magnitude and span length
            unit_load_label = tk.Label(load_info_frame, text='Unit_Load:')
            unit_load_label.grid(row=idx, column=3, padx=5, pady=5)
            unit_load_entry = tk.Entry(load_info_frame)
            unit_load_entry.grid(row=idx, column=4, padx=5, pady=5)

            start_pos_label = tk.Label(load_info_frame, text='Start_pos (m):')
            start_pos_label.grid(row=idx, column=5, padx=5, pady=5)
            start_pos_entry = tk.Entry(load_info_frame)
            start_pos_entry.grid(row=idx, column=6, padx=5, pady=5)

            end_pos_label = tk.Label(load_info_frame, text='End_pos (m):')
            end_pos_label.grid(row=idx, column=7, padx=5, pady=5)
            end_pos_entry = tk.Entry(load_info_frame)
            end_pos_entry.grid(row=idx, column=8, padx=5, pady=5)

    def get_load_info():
        global load_num, moment_num, loads
        current_type = []
        type_entry = []
        detail_buttons = []

        loads_submit_btn.grid_forget()
        load_num = int(load_num_entry.get())
        moment_num = int(moment_num_entry.get())
        for i in range(load_num):
            current_type.append(tk.StringVar())
            type_label = tk.Label(load_info_frame, text=f"load{i + 1}   type:")
            type_label.grid(row=i, column=0, padx=5, pady=5)

            type_entry.append(ttk.Combobox(load_info_frame,
                                           values=['Point_Load', 'Point_Moment', 'Uniformly_distributed_load'],
                                           state='readonly', textvariable=current_type[i]))
            type_entry[i].grid(row=i, column=1, padx=5, pady=5)

            detail_buttons.append(tk.Button
                                  (load_info_frame, text='add details', bg='grey', fg='white',
                                   command=lambda idx=i: get_load_details(detail_buttons, idx,
                                                                          current_type[idx].get())))
            detail_buttons[i].grid(row=i, column=2, padx=5, pady=5)

        for i in range(moment_num):
            moment_label = tk.Label(load_info_frame, text=f"Moment {i + 1} (kn.m)  ")
            moment_label.grid(row=load_num + i, column=0, padx=5, pady=5)
            moment_entry = tk.Entry(load_info_frame)
            moment_entry.grid(row=load_num + i, column=1, padx=5, pady=5)

        load_submit_btn = tk.Button(load_info_frame, text='Submit', bg='grey', fg='white')
        load_submit_btn.grid(row=load_num + moment_num, column=0, columnspan=2, padx=5, pady=5)

    loads_btn_window = tk.Toplevel(master)
    loads_btn_window.title('Load details')

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

    loads_submit_btn = tk.Button(loads_btn_window, text='Submit', bg='grey', fg='white', command=get_load_info)
    loads_submit_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Create a frame for the load details
    load_info_frame = tk.Frame(loads_btn_window)
    load_info_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def nodes_btn_click(master):
    position_entry = []
    support_entry = []
    settlement_entry = []

    def submit_details(num):
        global node_data
        node_data = []
        for i in range(num):
            node_data.append({'position': position_entry[i].get(), 'support': support_entry[i].get(),
                              'settlement': settlement_entry[i].get()})
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


def beam_btn_click(master):
    beam_btn_window = tk.Toplevel(master)
    beam_btn_window.title('Beam Details')

    length_label = tk.Label(beam_btn_window, text='Total length of the beam:')
    length_label.grid(row=0, column=0, padx=10, pady=10)

    length_entry = tk.Entry(beam_btn_window)
    length_entry.insert(0, '0.0')
    length_entry.grid(row=0, column=1, padx=10, pady=10)

    def close_window():
        global length
        length = float(length_entry.get())
        beam_btn_window.destroy()

    len_submit_btn = tk.Button(beam_btn_window, text='Submit', bg='grey', fg='white', command=close_window)
    len_submit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def start_beam_analysis():
    beam_analysis_window = tk.Toplevel(window)
    beam_analysis_window.geometry('600x400')
    beam_analysis_window.title('Beam info')

    model_label = tk.Label(beam_analysis_window, text="Model")
    model_label.grid(column=0, row=0, padx=5, pady=5)

    beam_btn = tk.Button(beam_analysis_window, text='Beam', bg='grey', fg='white', justify="center", width=20, height=5,
                         command=lambda: beam_btn_click(beam_analysis_window))
    beam_btn.grid(column=0, row=1, padx=5, pady=5)

    nodes_btn = tk.Button(beam_analysis_window, text='Nodes', bg='grey', fg='white', justify="center",
                          width=20, height=5, command=lambda: nodes_btn_click(beam_analysis_window))
    nodes_btn.grid(column=0, row=2, padx=5, pady=5)

    loads_label = tk.Label(beam_analysis_window, text="Loads and Moments")
    loads_label.grid(column=1, row=0, padx=5, pady=5)

    loads_btn = tk.Button(beam_analysis_window, text='Loads', bg='grey', fg='white', justify="center",
                          width=20, height=5, command=lambda: load_btn_click(beam_analysis_window))
    loads_btn.grid(column=1, row=1, padx=5, pady=5, rowspan=2)

    beam_analysis_window.columnconfigure(0, weight=1)
    beam_analysis_window.columnconfigure(1, weight=1)


window = tk.Tk()
window.geometry('400x400')
window.title('Structural Analysis')

button1 = tk.Button(window, text='Beam Analysis', width=20, height=5, bg='grey', fg='white',
                    command=start_beam_analysis)
button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()
