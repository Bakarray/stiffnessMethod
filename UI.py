import tkinter as tk
from tkinter import ttk

length = None
node_num = None
node_data = []


def get_load_info(master):
    load_info_window = tk.Toplevel(master)
    load_info_window.geometry('400x400')
    load_info_window.title('Load details')


def get_support_info(master, node_num_entry, length_entry):
    global length, node_num, node_data

    support_info_window = tk.Toplevel(master)
    support_info_window.geometry('1000x1000')
    support_info_window.title('Support details')

    length = float(length_entry.get())
    node_num = int(node_num_entry.get())
    for i in range(node_num):
        # Node label
        node_label = tk.Label(support_info_window, text=f'Details for node {i + 1}:')
        node_label.grid(row=i, column=0, padx=5, pady=5)

        # Position input
        position_label = tk.Label(support_info_window, text='Position (m):')
        position_label.grid(row=i, column=1, padx=5, pady=5)
        position_entry = tk.Entry(support_info_window)
        position_entry.grid(row=i, column=2, padx=5, pady=5)

        # Support input
        support_label = tk.Label(support_info_window, text='Support:')
        support_label.grid(row=i, column=3, padx=5, pady=5)
        support_entry = ttk.Combobox(support_info_window, values=['Fixed', 'Pinned', 'Roller', 'Free'],
                                     state='readonly')
        support_entry.grid(row=i, column=4, padx=5, pady=5)

        # Settlement input
        settlement_label = tk.Label(support_info_window, text='Settlement (m):')
        settlement_label.grid(row=i, column=5, padx=5, pady=5)
        settlement_entry = tk.Entry(support_info_window)
        settlement_entry.grid(row=i, column=6, padx=5, pady=5)

        submit_button = tk.Button(support_info_window, text='Submit',
                                  command=lambda: get_load_info(support_info_window))
        submit_button.grid(row=node_num, column=2, columnspan=6, padx=10, pady=10)

        node_data.append({'position': position_entry.get(), 'support': support_entry.get(),
                          'settlement': settlement_entry.get()})


def get_beam_info():
    print("beam info")
    info_window = tk.Toplevel(window)
    info_window.geometry('400x400')
    info_window.title('Beam info')

    length_label = tk.Label(info_window, text='Total length of the beam:')
    length_label.grid(row=0, column=0, padx=10, pady=10)
    length_entry = tk.Entry(info_window)
    length_entry.grid(row=0, column=1, padx=10, pady=10)

    node_num_label = tk.Label(info_window, text='Number of nodes on the beam:')
    node_num_label.grid(row=1, column=0, padx=10, pady=10)
    node_num_entry = tk.Entry(info_window)
    node_num_entry.grid(row=1, column=1, padx=10, pady=10)

    submit_button = tk.Button(info_window, text='Submit',
                              command=lambda: get_support_info(info_window, node_num_entry, length_entry))
    submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


window = tk.Tk()
window.geometry('400x400')
window.title('Structural Analysis')

button1 = tk.Button(window, text='Beam Analysis', width=20, height=5, bg='grey', fg='white', command=get_beam_info)
button1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()
