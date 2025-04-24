from tkinter import *
import customtkinter as CTk
import tkinter as tk
from PIL.ImageOps import expand
from click import clear
from libpasteurize.fixes.fix_future_builtins import expression

EQUAL_COLOR='#85b7dc'
EQUAL_COLOR_WHENHOVER='#4a9ede'
BACK_BUTTONS='#adb5bd'
BG_JUST_DIGITS='#f8f9fa'
BG_CALCULATOR='#f4f4f4'
COLOR_AMALGARA='#f8f8f8'
COLOR_AMALGARA_BUTTONS_WHENHOVER='#e0e0e0'
class calculator_APP():
    def __init__(self):
        self.root=CTk.CTk()
        self.root.title('Calculator')
        self.root.geometry('300x520+1100+300')
        self.root.resizable(False,False)
        self.root.iconbitmap('logo_calc.ico')
        # self.root.overrideredirect(True)
        self.root.attributes('-alpha', 1)
        self.display_frame=self.create_display_frame()
        self.buttons_frame=self.create_buttons_frame()
        self.total_experassion=''
        self.current_experassion=''
        self.total_label,self.current_lebel = self.create_display_labels()
        self.digit = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            ".": (4, 1), 0: (4, 2)}
        self.create_digit_button()
        self.operation={"/":"\u00f7","*":"\u00D7","-":"\u2212","+":"+"}
        self.create_operator_button()
        self.create_special_button()
        self.buttons_frame.rowconfigure(0,weight=1)
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x,weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.root.mainloop()


    def create_display_frame(self):
        frame=tk.Frame(self.root,height=200,bg=BG_CALCULATOR)
        frame.pack(fill=BOTH,expand=True)
        return frame
    def create_buttons_frame(self):
        frame = tk.Frame(self.root, height=320, bg=BG_CALCULATOR)
        frame.pack(fill=BOTH, expand=True)
        return frame
    def create_display_labels(self):
        total_label=Label(self.display_frame,text=self.total_experassion,bg=BG_CALCULATOR,anchor=E,fg='black',padx=24,font=('Bodoni',16))
        total_label.pack(fill=BOTH,expand=True)
        current_lebel =Label(self.display_frame, text=self.current_experassion,anchor=E, bg=BG_CALCULATOR, fg='black', padx=24,font=('Bodoni', 40,'bold'))
        current_lebel.pack(fill=BOTH, expand=True)
        return total_label,current_lebel
    def on_hover_digit(self,event):
        event.widget.configure(bg=COLOR_AMALGARA_BUTTONS_WHENHOVER, font=('Bodoni', 24, 'bold'),padx=0,pady=0)

    def on_defualt_digit(self,event):
        event.widget.configure(bg=COLOR_AMALGARA, font=('Bodoni', 24, 'bold'),padx=1,pady=1)
    def create_digit_button(self):
        for digit,gird_value in self.digit.items():
            button = Button(self.buttons_frame, text=str(digit), bg=BG_JUST_DIGITS,cursor='hand2', fg='black', font=('Bodoni', 24, 'bold'),anchor='center',
                               borderwidth=0,command=lambda x=digit:self.add_to_expression(x))
            button.grid(row=gird_value[0],column=gird_value[1],sticky=NSEW,padx=1,pady=1)
            button.bind('<Enter>', self.on_hover_digit)
            button.bind('<Leave>', self.on_defualt_digit)

    def on_hover_digit_operator(self, event):
        event.widget.configure(bg=COLOR_AMALGARA_BUTTONS_WHENHOVER, font=('Bodoni', 24), padx=1, pady=1)

    def on_defualt_digit_operator(self, event):
        event.widget.configure(bg=COLOR_AMALGARA, font=('Bodoni', 24), padx=1, pady=1)
    def create_operator_button(self):
        i=0
        for operator,symbol in self.operation.items():
            button = Button(self.buttons_frame, text=symbol, bg=COLOR_AMALGARA,cursor='hand2',activebackground=COLOR_AMALGARA_BUTTONS_WHENHOVER, fg='black', font=('Bodoni', 24),
                            anchor='center',
                            borderwidth=0,command=lambda x=operator:self.append_operator(x))
            button.grid(row=i,column=4,sticky='nsew',padx=1,pady=1)
            i+=1
            button.bind('<Enter>', self.on_hover_digit_operator)
            button.bind('<Leave>', self.on_defualt_digit_operator)
    def on_hover_digit_clear(self, event):
        event.widget.configure(bg=COLOR_AMALGARA_BUTTONS_WHENHOVER,fg=EQUAL_COLOR_WHENHOVER, font=('Bodoni', 24,'bold'))

    def on_defualt_digit_clear(self, event):
        event.widget.configure(bg=COLOR_AMALGARA,fg='black', font=('Bodoni', 24,'bold'))
    def create_clear_button(self):
        button =Button(self.buttons_frame, text="C",activeforeground=EQUAL_COLOR_WHENHOVER,cursor='hand2', bg=COLOR_AMALGARA, activebackground=COLOR_AMALGARA_BUTTONS_WHENHOVER, fg='black', font=('Bodoni', 24,'bold'),
                        borderwidth=0,command=self.clear)
        button.grid(row=0,column=1 ,columnspan=1, sticky="nsew",padx=1,pady=1)
        button.bind('<Enter>', self.on_hover_digit_clear)
        button.bind('<Leave>', self.on_defualt_digit_clear)

    def on_hover_digit_equals(self, event):
        event.widget.configure(bg=EQUAL_COLOR_WHENHOVER, font=('Bodoni', 24, 'bold'), padx=0, pady=0)

    def on_defualt_digit_equals(self, event):
        event.widget.configure(bg=EQUAL_COLOR, font=('Bodoni', 24, 'bold'), padx=1, pady=1)
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=EQUAL_COLOR,cursor='hand2',activebackground=EQUAL_COLOR_WHENHOVER, fg='black', font=('Bodoni', 24, 'bold'),
                           borderwidth=0,command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky="nsew",padx=1,pady=1)

        button.bind('<Enter>', self.on_hover_digit_equals)
        button.bind('<Leave>', self.on_defualt_digit_equals)
    def square(self):
        self.current_experassion=str(eval(f'{self.current_experassion}**2'))
        self.update_label()
    def on_hover_digit_square(self, event):
        event.widget.configure(bg=COLOR_AMALGARA_BUTTONS_WHENHOVER, font=('Bodoni', 24,'bold'), padx=1, pady=1)
    def on_defualt_digit_square(self, event):
        event.widget.configure(bg=COLOR_AMALGARA, font=('Bodoni', 24,'bold'), padx=1, pady=1)
    def create_square_button(self):
        button =Button(self.buttons_frame, text="x\u00b2",activeforeground='black',cursor='hand2', bg=COLOR_AMALGARA, activebackground=COLOR_AMALGARA_BUTTONS_WHENHOVER, fg='black', font=('Bodoni', 24,'bold'),
                        borderwidth=0,command=self.square)
        button.grid(row=0,column=2, sticky="nsew",padx=1,pady=1)
        button.bind('<Enter>', self.on_hover_digit_square)
        button.bind('<Leave>', self.on_defualt_digit_square)

    def sqrt(self):
        self.current_experassion = str(eval(f'{self.current_experassion}**0.5'))
        self.update_label()
    def create_sqrt_button(self):
        button =Button(self.buttons_frame, text="\u221Ax",activeforeground='black',cursor='hand2', bg=COLOR_AMALGARA, activebackground=COLOR_AMALGARA_BUTTONS_WHENHOVER, fg='black', font=('Bodoni', 24,'bold'),
                        borderwidth=0,command=self.sqrt)
        button.grid(row=0,column=3, sticky="nsew",padx=1,pady=1)
        button.bind('<Enter>', self.on_hover_digit_square)
        button.bind('<Leave>', self.on_defualt_digit_square)
    def update_total_label(self):
        expression=self.total_experassion
        for operator,sumbol in self.operation.items():
            expression=expression.replace(operator,f'{sumbol}')
        self.total_label.config(text=expression)
    def bind_key(self):
        self.root.bind('<Return>',lambda event: self.evaluate())
        for key in self.digit:
            self.root.bind(str(key),lambda event,digit=key:self.add_to_expression(digit))
        for key in self.operation:
            self.root.bind(key,lambda event,operator=key:self.add_to_expression(operator))
    def update_label(self):
        self.current_lebel.config(text=self.current_experassion[:9])
    def add_to_expression(self,value):
        self.current_experassion+=str(value)
        self.update_label()
    def create_special_button(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.bind_key()
    def append_operator(self,operator):
        self.current_experassion+=operator
        self.total_experassion+=self.current_experassion
        self.current_experassion=''
        self.update_total_label()
        self.update_label()
    def clear(self):
        self.current_experassion=''
        self.total_experassion=''
        self.update_label()
        self.update_total_label()
    def evaluate(self):
        self.total_experassion+=self.current_experassion
        self.update_total_label()
        try:
            self.current_experassion=str(eval(self.total_experassion))
            self.total_experassion=''
        except:
            self.current_experassion='Error'
        finally:
            self.update_label()
calculator_APP()