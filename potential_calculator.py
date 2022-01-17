import random
from functools import reduce
import tkinter as tk
import tkinter.ttk as ttk

## values -----------------------------------------------------------

simulations = 1000
suc_rare_to_epic = 1 / 101

equip = {"Weapon/Emblem":           ("ATT", 3.948, 0.137, 0.004, 100, 100, 100),
         "Force Shield/Soul Ring":  ("ATT", 3.551, 0.136, 0.004, 100, 100, 100),
         "Secondary (Others)":      ("ATT", 2.941, 0.101, 0.002, 100, 100, 100),
         "Helmet/Bottom":           ('Stat', 8.214, 0.832, 0.034, 41.07, 4.16, 0.17),
         "Top/Overall":             ('Stat', 7.424, 0.747, 0.029, 37.12, 3.735, 0.145),
         "Shoes":                   ('Stat', 8.087, 0.718, 0.028, 40.435, 3.59, 0.14),
         "Gloves":                  ('Stat', 6.777, 0.678, 0.026, 33.885, 3.39, 0.13),
         "Belt/Shoulder/Cape":      ('Stat', 8.214, 0.832, 0.034, 41.07, 4.16, 0.17),
         "Accessories":             ('Stat', 12.013, 1.092, 0.05, 60.065, 5.46, 0.25),
         "Heart":                   ('Stat', 12.163, 1.263, 0.06, 60.815, 6.315, 0.3)}

equip_type = ["Equipment Type",
              "Weapon/Emblem",
              "Force Shield/Soul Ring",
              "Secondary (Others)",
              "Helmet/Bottom",
              "Top/Overall",
              "Shoes",
              "Gloves",
              "Belt/Shoulder/Cape",
              "Accessories",
              "Heart"]

current_rarity = ["Current Rarity",
                  "Epic",
                  "Rare"]

## formulae ---------------------------------------------------------



def createEquip(cr_rates):
    cr, rates = cr_rates
    eq = (cr, rates)
    return eq 

def roll(cr, success_rate):
    done, success_rate = 0, success_rate/100
    if cr != "Epic":
        tick1 = random.random()
        if tick1 > suc_rare_to_epic:
            return (cr, done)
        else:
            cr = "Epic"
    tick2 = random.random()
    if tick2 < success_rate:
        done = 1
    return (cr, done)

def wholeProcess(eq):
    cr, rates = eq
    total_cubes = []
    for i in range(1,7):
        done, cubes, success_rate = 0, 0, rates[i]
        while done != 1:
            cubes += 1 
            cr, done = roll(cr, success_rate)
        total_cubes.append(cubes)
    return total_cubes

def getRollCost(level):
    checks = ((30, 0), (70, 0.5), (120, 2.5), (400, 20))
    for check in checks:
        if level <= check[0]:
            constant = check[1]
            return level ** 2 * constant

def getStats(total_cubes, cost_of_cubes, cost_to_roll):
    def mergeList(ls1, ls2):
        if len(ls1) !=  len(ls2):
            return ls1
        else:
            for i in range(len(ls1)):
                ls1[i] += ls2[i]
            return ls1
    
    cubes = reduce(mergeList, total_cubes)
    print(cubes)
    average_cubes = list(map(lambda x: x/simulations, cubes))
    print(average_cubes)

    def costToWords(num):
        if num > 1000000000000:
            word = str(num // 10000000000 / 100) + "T"
        elif num > 1000000000:
            word = str(num // 10000000 / 100) + "B"
        elif num > 1000000:
            word = str(num // 10000 / 100) + "M"
        else:
            word = str(num // 10 / 100) + "k"
        return word
    
    cost_ls = list(map(lambda x: x*(cost_of_cubes + cost_to_roll), average_cubes))
    stats = list(map(costToWords, cost_ls))
    return stats


## tkinter ----------------------------------------------------------

root = tk.Tk()

canvas1 = tk.Canvas(root, width=320, height=450, bg = "dark sea green")
canvas1.pack()

## Label_Group_1
labels1 = ["Level",
           "Cost of Cubes",
           "Equipment Type",
           "Current Rarity"]

x1_value, y1_value = 40, 30
for label in labels1:
    tk.Label(root, text = label,width=13,
             anchor="w").place(x = x1_value, y = y1_value)
    y1_value += 30

## Entry_Group_1 
entry1, entry2 = tk.Entry(root), tk.Entry(root)
entries1 = [entry1, entry2]

x4_value, y4_value = 210, 40
for entry in entries1:
    canvas1.create_window(x4_value, y4_value, window=entry)
    y4_value += 30

entry1.insert(-1, "140")
entry2.insert(-1, "40000") 

## Entry_Group_2
x5_value, y5_value = 148, 90
    
variable1 = tk.StringVar(root)
variable1.set(equip_type[0])
entry3 = ttk.OptionMenu(root, variable1, *equip_type)
entry3.configure(width=15)
entry3.place(x=x5_value, y=y5_value)

variable2 = tk.StringVar(root)
variable2.set(current_rarity[1])
entry4 = ttk.OptionMenu(root, variable2, *current_rarity)
entry4.configure(width=15)
entry4.place(x=x5_value, y=y5_value+30)

def calculate(event=None):
    lvl, cost_of_cubes = int(entry1.get()), int(entry2.get())
    et, cr = variable1.get(),variable2.get()
    rate = equip[et]
    cost_to_roll = getRollCost(lvl)

    sims = [createEquip((cr, rate)) for i in range(simulations)]
    sims = list(map(wholeProcess, sims))
    stats = getStats(sims, cost_of_cubes, cost_to_roll)  


    ## Label_Group_2
    labels2_1 = ["6% ATT",
                 "9% ATT",
                 "12% ATT"]

    labels2_2 = ["6% (Specific)",
                 "9% (Specific)",
                 "12% (Specific)",
                 "6% (Any Stat)",
                 "9% (Any Stat)",
                 "12% (Any Stat)"]

    if rate[0] == "ATT":
        labels2 = labels2_1
    else:
        labels2 = labels2_2

    x2_value, y2_value = 40, 190
    for label in labels2:
        tk.Label(root, text = label,width=13,
                 anchor="w").place(x = x2_value, y = y2_value)
        y2_value += 30

    ## Label_Group_3
    ans1, ans2, ans3, ans4, ans5, ans6 = tk.Label(root), tk.Label(root), tk.Label(root), tk.Label(root), tk.Label(root), tk.Label(root)
    answers = [ans1, ans2, ans3, ans4, ans5, ans6]

    if rate[0] == "ATT":
        answers = answers[:3]

    x3_value, y3_value = 148, 190
    for i in range(len(answers)):
        value = stats[i]
        answers[i] = tk.Label(root, text = value, width=17, anchor="w")
        answers[i].place(x = x3_value, y = y3_value)
        y3_value += 30

    return None 
    
## Button_1
tk.Button(root, text = "Calculate", width = 17,
          command=calculate).place(x = 147,y = 150) 


root.mainloop()

