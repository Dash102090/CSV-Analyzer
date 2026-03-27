from customtkinter import *
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def main_page():

    Empty_Error = CTkLabel(frame, font=('Arial',10, 'normal'), text_color="#A70000", height=5)
    Empty_Error.place(x=90, y=143)

    if File_name.get() != '':
        Empty_Error.configure(text='                                                            ')

        if '.csv' in File_name.get():
            
            try:
                Found = False
                start_path = os.getcwd()

                for root, dir, files in os.walk(start_path,topdown=True):
                    for name in files:
                        if  name.lower() == File_name.get().lower():
                            
                            try:
                                df = pd.read_csv(os.path.join(root, name), encoding='utf-8')
                            except UnicodeDecodeError: 
                                df = pd.read_csv(os.path.join(root, name), encoding='latin1')

                            Confirm_Button.configure(state=DISABLED)

                            main_window = CTkToplevel()

                            main_window.geometry('900x700')
                            main_window.resizable(False, False)

                            Avg_frame = CTkScrollableFrame(main_window, height=250, width=250,
                                                           fg_color="#412381", border_width=3, border_color="#110235")
                            Avg_frame.place(x=10, y=10)

                            Avg = df.mean(numeric_only=True)

                            Average_label = CTkLabel(Avg_frame, text='AVERAGE', font=('Arial', 30, 'bold'), text_color='#110235')
                            Average_label.pack()

                            Average = CTkLabel(Avg_frame, text=Avg.to_string(), font=('Arial', 15))
                            Average.pack()

                            Median_frame = CTkScrollableFrame(main_window, height=250, width=250,
                                                           fg_color="#412381", border_width=3, border_color="#110235")
                            Median_frame.place(x=300, y=10)

                            First_val = df.median(numeric_only=True)

                            Median_label = CTkLabel(Median_frame, text='MIDDLE VALUE', font=('Arial', 30, 'bold'), text_color='#110235')
                            Median_label.pack()

                            Median = CTkLabel(Median_frame, text=First_val.to_string(), font=('Arial', 15))
                            Median.pack()

                            No_val_frame = CTkScrollableFrame(main_window, height=250, width=250,
                                                           fg_color="#412381", border_width=3, border_color="#110235")
                            No_val_frame.place(x=600, y=10)

                            No_val = df.isnull().sum()

                            No_val_label = CTkLabel(No_val_frame, text='MISSING VALUE', font=('Arial', 30, 'bold'), text_color='#110235')
                            No_val_label.pack()

                            Missing = CTkLabel(No_val_frame, text=No_val.to_string(), font=('Arial', 15))
                            Missing.pack()

                            pie_chart_frame = CTkFrame(main_window)
                            pie_chart_frame.place(x=150, y=300)

                            numeric_df = df.select_dtypes(include='number')

                            numeric_df = numeric_df.loc[:, numeric_df.nunique()<len(df)]

                            categories = numeric_df.columns
                            values = numeric_df.sum().values

                            fig = Figure(figsize=(6, 3.5), dpi=100)
                            ax = fig.add_subplot(111)
                            ax.pie(values, labels=categories, autopct='%1.1f%%')

                            canvas = FigureCanvasTkAgg(fig, pie_chart_frame)
                            canvas.draw()
                            canvas.get_tk_widget().pack()

                            Found = True
                            break

                    if Found:
                        break

            except FileNotFoundError:
                Empty_Error.configure(text='File Not Found.')
        
        else:

            Empty_Error.configure(text='This is not a csv file')

    else:

        Empty_Error.configure(text='Enter a cvs file.')


window = CTk()

window.geometry('500x450')
window.configure(fg_color="#878ACE")
window.resizable(False, False)

band = CTkFrame(window, height=50, fg_color="#0D0127", corner_radius=0)
band.pack(fill='x', side=TOP)

band_text = CTkLabel(window, text='CTk Company', font=('Arial', 30, 'bold'), fg_color='#0D0127', 
                     text_color="#EAE0FF")
band_text.place(x=10, y=10)

frame = CTkFrame(window, height=200, width=300, fg_color="#6F4EB9", border_width=3, border_color="#1A034E")
frame.place(x=100, y=100)

WELCOME_text = CTkLabel(frame, text='WELCOME!!!', font=('Helvetica', 45, 'bold'), text_color="#370268",)
WELCOME_text.place(x=15, y=20)

text = CTkLabel(frame, text='Enter the file you want Analyzed!', font=('Arial', 15, 'bold'), text_color="#1F013B")
text.place(x=35, y=80)

File_name = CTkEntry(frame, placeholder_text='Enter csv file...', corner_radius=20)
File_name.place(x=80, y=115)

Confirm_Button = CTkButton(frame, text='Confirm', corner_radius=20, 
                           fg_color="#4417AD", hover_color="#350C92",
                           command=main_page)
Confirm_Button.place(x=80, y=160)

window.mainloop()