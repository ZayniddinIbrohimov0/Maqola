import tkinter as tk
from utils import Price, real_or_int, price_real_or_int


class CustomInput:
    def __init__(self,window: tk.Tk, width: int, height: int, position_x: int, position_y: int, *args, **kwargs):
        self.input = tk.Entry(window, font=('Arial 15'), *args, **kwargs)
        self.input.place(height=height, width=width, x=position_x, y=position_y)
    
    def get_text(self):
        return self.input.get()
    
    def set_text(self, text: str):
        self.input.delete(0, tk.END)
        self.input.insert(0, text)
    
    def change_place(self, x: int, y: int):
        self.input.place(x=x,y=y)
    
    def delete(self):
        self.input.destroy()

class CustomButton:
    def __init__(self, window: tk.Tk, text: str, width: int, height: int, position_x: int, position_y: int, *args, **kwargs):
        self.button = tk.Button(window, text=text, *args, **kwargs)
        self.button.place(height=height, width=width, x=position_x, y=position_y)
    
    def change_state(self, state):
        self.button["state"] = state
    
    def delete(self):
        self.button.destroy()
    def full_width(self, window: tk.Tk, margin = 0):
        self.button.place(width=window.winfo_width() - margin * 2, x=margin)

        

class TransportationSolveGUI:
    """ Transport muammosi uchun GUI dasturi """
    def __init__(self, solution_class:dict, demand_name: str, offer_name: str, *args, **kwargs) -> None:
        self.solution_class = solution_class
        self.demand_name = demand_name
        self.offer_name = offer_name
        self.class_list = []
        for i, j in solution_class.items():
            self.class_list.append(i)

        self.demand_size = 3
        self.offer_size = 3
        self.inputs = []
        self.demands = []
        self.offers = []

        self.label_demand = []
        self.label_offer = []

        self.window = tk.Tk()
        self.window.title("Transport muammosini yechish uchun GUI")
        self.window.geometry("600x300+100+100")
        self.window.protocol("WM_DELETE_WINDOW",  self.event_close)
        self.window.configure(bg='#e6e6ff')

        self.new_window = None
        # Buttonlarni chizish
        self.buttons_draw()

        # Matritsa inputlarni chizish
        self.inputs_draw()

        # labellarni chizish
        self.offer_label_draw()
        self.demand_label_draw()

        # demand va offer inputlarini chizish
        self.demand_and_offer_draw()
        self.window.mainloop()

    def demand_label_draw(self):
        for i in range(self.demand_size):
            self.label_demand.append(CustomButton(
                self.window, text='%s-%s'%(self.demand_name, str(i + 1)),
                height=40, width=70, position_x=120 + i * 70,
                position_y=50, state=tk.DISABLED, font=('Arial 11')
            ))

    def offer_label_draw(self):
        for i in range(self.offer_size):
            self.label_offer.append(CustomButton(
                self.window, text='%s-%s'%(self.offer_name, str(i + 1)),
                height=40, width=70, position_x=50, position_y=90 + i * 40,
                state=tk.DISABLED, font=('Arial 11')
            ))

    def buttons_draw(self):
        self.button_demand_plus = CustomButton(self.window, text=' + ', font=('Arial 20'), width=70, height=40, position_x=40, position_y=0, command=self.add_demand)
        self.button_demand_minus = CustomButton(self.window, text=' - ', font=('Arial 20'), width=70, height=40, position_x=120, position_y=0, command=self.subtraction_demand)
        
        self.button_offer_plus = CustomButton(self.window, text=' + ', font=('Arial 20'), width=40, height=70, position_x=0, position_y=40, command=self.add_offer)
        self.button_offer_minus = CustomButton(self.window, text=' - ', font=('Arial 20'), width=40, height=70, position_x=0, position_y=120, command=self.subtraction_offer)


        self.solve_button = CustomButton(self.window, text=' Hisoblash ', font=('Arial 13'), width=150, height=40, position_x=200, position_y=0, command=self.solve)
        
        self.menu = tk.StringVar()
        self.menu.set(self.class_list[0])
        
        self.dropdown = tk.OptionMenu(self.window, self.menu, *self.class_list)
        self.dropdown.place(width=120, height=40, x=360, y=0)

    def inputs_draw(self):
        for i in range(self.offer_size):
            self.inputs.append([])
            for j in range(self.demand_size):
                self.inputs[i].append(
                    CustomInput(self.window, width=70, height=40, position_x = 120 + j * 70, position_y = 90 + i * 40 )
                )
    def demand_and_offer_draw(self):
        self.demand_draw()
        self.offer_draw()

    def demand_draw(self):
        for i in range(self.demand_size):
            self.demands.append(
                CustomInput(self.window, width=70, height=40, position_x = 120 + i * 70, position_y = 100 + self.offer_size * 40)
            )
        
    def offer_draw(self):
        for i in range(self.offer_size):
            self.offers.append(
                CustomInput(self.window, width=70, height=40, position_x = 130 + self.demand_size * 70, position_y=90 + i * 40)
            )
    
    def add_demand(self):
        self.demands.append(
            CustomInput(self.window, width=70, height=40, position_x=self.demand_size * 70 + 120, position_y=100 + self.offer_size * 40)
        )
        for i in range(self.offer_size):
            self.inputs[i].append(
                CustomInput(self.window, width=70, height=40, position_x=self.demand_size * 70 + 120, position_y=90 + i * 40)
            )
            self.offers[i].change_place(x=(self.demand_size + 1) * 70 + 130, y= 90 + i * 40)
        self.label_demand.append(CustomButton(
                self.window, text='%s-%s'%(self.demand_name, str(self.demand_size + 1)),
                height=40, width=70, position_x=50 + (self.demand_size + 1) * 70, position_y=50,
                state=tk.DISABLED, font=('Arial 11')
            ))
        self.demand_size += 1

        if self.demand_size > 3:
            self.window.geometry("%sx%s"%( str(self.window.winfo_width() + 70), str(self.window.winfo_height())  ))

        if self.demand_size >= 2:
            self.button_demand_minus.change_state(tk.ACTIVE)

    def add_offer(self):
        self.offers.append(
            CustomInput(self.window, width=70, height=40, position_x=130 + self.demand_size * 70, position_y=90 + self.offer_size * 40)
        )
        self.inputs.append([])
        for i in range(self.demand_size):
            self.inputs[-1].append(
                CustomInput(self.window, width=70, height=40, position_x=120 + i * 70, position_y=self.offer_size * 40 + 90)
            )
            self.demands[i].change_place(x=120 + i * 70, y=(self.offer_size+1)*40 + 100)
        self.label_offer.append(CustomButton(
                self.window, text='%s-%s'%(self.offer_name, str(self.offer_size + 1)),
                height=40, width=70, position_x=50, position_y=90 + (self.offer_size) * 40,
                state=tk.DISABLED, font=('Arial 11')
            ))
        self.offer_size += 1

        self.window.geometry("%sx%s"%( str(self.window.winfo_width()), str(self.window.winfo_height() + 40)))

        if self.offer_size >= 2:
            self.button_offer_minus.change_state(tk.ACTIVE)

    def subtraction_demand(self):
        self.demands[len(self.demands) - 1].delete()
        del self.demands[len(self.demands) - 1]

        for i in range(self.offer_size):
            self.inputs[i][len(self.inputs[i])-1].delete()
            del self.inputs[i][len(self.inputs[i])-1]

            self.offers[i].change_place(x=(self.demand_size - 1) * 70 + 130, y = 90 + i * 40)
        
        self.label_demand[len(self.label_demand)-1].delete()
        del self.label_demand[len(self.label_demand)-1]

        self.demand_size -= 1

        self.window.geometry("%sx%s"%( str(self.window.winfo_width() - 70), str(self.window.winfo_height())))
        if self.window.winfo_width() <= 500:
            self.window.geometry("500x%s"%(str(self.window.winfo_height())))

        if self.demand_size == 1:
            self.button_demand_minus.change_state(tk.DISABLED)

    def subtraction_offer(self):
        self.offers[len(self.offers) - 1].delete()
        del self.offers[len(self.offers) - 1]

        for i in range(self.demand_size):
            self.inputs[-1][i].delete()
            self.demands[i].change_place(x=120 + i * 70, y=(self.offer_size - 1) * 40 + 100)
        del self.inputs[-1]
        self.offer_size -= 1
        self.label_offer[len(self.label_offer)-1].delete()
        del self.label_offer[len(self.label_offer)-1]
        
        
        self.window.geometry("%sx%s"%( str(self.window.winfo_width()), str(self.window.winfo_height() - 40)))
        if self.window.winfo_width() < 500:
            self.window.geometry("500x%s"%(str(self.window.winfo_height())))

        if self.offer_size == 1:
            self.button_offer_minus.change_state(tk.DISABLED)

    def solve(self):
        price_matrix = []
        talab = []
        taklif = []
        for i in range(len(self.inputs)):
            price_matrix.append([])
            for j in range(len(self.inputs[i])):
                text = self.inputs[i][j].get_text()
                if text == '':
                    return self.error_view(error=''' %s-ustun %s-satr bo'sh. \n Ma'lumotlar To'liq emas ! '  '''%(str(j+1), str(i+1)))
                if float(text) < 0:
                    return self.error_view(error=''' Manfiy sonlar kiritilishi mumkin emas ! ''')
                try:
                    price_matrix[i].append(real_or_int(float(text)))
                except:
                    return self.error_view(error=''' %s-ustun %s-satrda xatolik mavjud '''%(str(j+1), str(i+1)))
                
        for i in range(len(self.demands)):
            text = self.demands[i].get_text()
            if text == '':
                return self.error_view(error=''' %s-talab miqdorini kiriting. \n Ma'lumotlar To'liq emas ! '''%(str(i + 1)))
            if float(text) < 0:
                return self.error_view(error=''' Manfiy sonlar kiritilishi mumkin emas ! ''')
            try:
                talab.append(real_or_int(float(text)))
            except:
                return self.error_view(error=''' %s-talab miqdorini kiritishda xatolik mavjud '''%(str(i+1)))
            
        for i in range(len(self.offers)):
            text = self.offers[i].get_text()
            if text == '':
                return self.error_view(error=''' %s-taklif miqdorini kiriting. \n Ma'lumotlar To'liq emas ! '''%(str(i + 1)))
            if float(text) < 0:
                return self.error_view(error=''' Manfiy sonlar kiritilishi mumkin emas ! ''')
            try:
                taklif.append(real_or_int(float(text)))
            except:
                return self.error_view(error=''' %s-taklif miqdorini kiritishda xatolik mavjud '''%(str(i+1)))
        if not (sum(taklif) == sum(talab)):
            return self.error_view(error=''' Talab va taklif miqdori bir xil bo'lishi kerak ! ''')
        
        try:            
            method = self.solution_class[self.menu.get()]
            _solve = method(price_matrix, talab, taklif).get_rezault()
            _solve = list(map(price_real_or_int, _solve))
            return self.solve_view(_solve, price_matrix)
        except Exception as e:
            print(e)
            return self.error_view(''' Nomalum xatolik yuz berdi ! ''')
        
    def solve_view(self, point_list: list[Price], price_matrix: list[list[int]]):
        if not (self.new_window == None):
            return
        
        text = ''
        sum = 0
        for i in point_list:
            text += '%s*%s + '%(
                str(i.arg), str(price_matrix[i.i][i.j])
            )
            sum += i.arg * price_matrix[i.i][i.j]
        text = text[:-3]
        text += ' = %s'%(str(sum))

        self.new_window = tk.Tk()
        self.new_window.protocol("WM_DELETE_WINDOW",  self.event_close_new_window)
        self.new_window.title(" Muammo yechimi ")
        width = self.demand_size * 100 + 100
        height = self.offer_size * 50 + 200
        if (width < len(text) * 10 + 60): 
            width = len(text) * 10 + 60

        self.new_window.geometry(f"{width}x{height}+150+150")
        CustomButton(self.new_window, width=width - 40, height=80, position_x=20, position_y=20, state=tk.DISABLED, text=text, font=('Arial 14'))

        input_list: list[list[CustomInput]] = []

        for i in range(self.offer_size):
            inputs: list[CustomInput] = []
            for j in range(self.demand_size):
                ci = CustomInput(self.new_window, width=100, height=50, position_x=40+j*100, position_y=140+i*50)
                ci.set_text(str(self.inputs[i][j].get_text()))
                inputs.append(ci)
            input_list.append(inputs)
        
        for i in point_list:
            input_list[i.i][i.j].set_text(
                text='%s (%s)'%(str(input_list[i.i][i.j].get_text()), str(i.arg))
            )
        self.new_window.mainloop()

    
    def error_view(self, error: str):
        if not (self.new_window == None):
            return
        self.new_window = tk.Tk()
        self.new_window.protocol("WM_DELETE_WINDOW",  self.event_close_new_window)
        self.new_window.title(" Xatolik !")
        self.new_window.geometry("400x150+500+300")
        def close_new_window():
            self.new_window.destroy()
            self.new_window = None
        CustomButton(self.new_window, text=error, width=400, height=150, position_x=0, position_y=0, font=('Arial 14'), fg='red', command=close_new_window)
        self.new_window.mainloop()

    def event_close(self):
        try:
            if self.new_window == None:
                pass
            else:
                self.new_window.destroy()
            self.window.destroy()
        except:
            self.window.destroy()

    def event_close_new_window(self):
        if self.new_window is not None:
            self.new_window.destroy()
            self.new_window = None
