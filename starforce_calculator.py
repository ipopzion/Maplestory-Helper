import tkinter as tk
import random

## values -----------------------------------------------------------

simulations = 10000

rateup = {0: (95, 100, 0),
          1: (90, 100, 0),
          2: (85, 100, 0),
          3: (85, 100, 0),
          4: (80, 100, 0),
          5: (75, 100, 0),
          6: (70, 100, 0),
          7: (60, 100, 0),
          8: (60, 100, 0),
          9: (55, 100, 0),
          10: (50, 100, 0),
          11: (45, 0, 100),
          12: (40, 0, 99),
          13: (35, 0, 98),
          14: (30, 0, 98),
          15: (30, 97, 0),
          16: (30, 0, 97),
          17: (30, 0, 97),
          18: (30, 0, 96),
          19: (30, 0, 96),
          20: (30, 90, 0),
          21: (30, 0, 90),
          22: (3, 0, 80),
          23: (2, 0, 70),
          24: (1, 0, 60)}         

## formulae ---------------------------------------------------------

def createequip(lvl_cs_ds):
    lvl, cs, ds = lvl_cs_ds
    rlvl = lvl // 10 * 10
    sf, fail, cost, boom = cs, 0, 0, 0
    eq = (rlvl, sf, fail, cost, boom, ds)
    return eq 

def sfUp(eq):
    rlvl, sf, fail, cost, boom, ds = eq
    newcost = getCost(eq)
    if boom:
        pass
    elif fail == 2:
        sf += 1
        fail = 0
        cost += newcost
    else:
        tick1 = random.random()
        if tick1 < rateup[sf][0] / 100:
            sf += 1
            fail = 0
            cost += newcost
        else:
            tick2 = random.random()
            if tick2 < rateup[sf][1] / 100:
                fail += 1
                cost += newcost
            elif tick2 < (rateup[sf][1] + rateup[sf][2]) / 100:
                fail += 1
                cost += newcost
                sf -= 1
            else:
                boom = 1
    eq = (rlvl, sf, fail, cost, boom, ds)
    return eq

def getCost(eq):
    rlvl, sf, fail, cost, boom, ds = eq
    base, nextsf = rlvl ** 3, sf + 1 
    if sf < 11:
        cost = base * nextsf / 25
    elif sf < 16:
        cost = base * (nextsf ** 2.7) / 400
    else:
        cost = base * (nextsf ** 2.7) / 200
    return cost + 1000

def powerup(eq):
    rlvl, sf, fail, cost, boom, ds = eq
    while (sf < ds) and (boom == 0):
        eq = sfUp(eq)
        rlvl, sf, fail, cost, boom, ds = eq
    return eq

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

def getStats(ls, simulations):
    boom_record, boom_count = {}, 0
    for entry in ls:
        if entry[4] == 1:
            if entry[1] not in boom_record:
                boom_record[entry[1]] = 0
            boom_record[entry[1]] += 1
            boom_count += 1
    boom_lvl_list = list(boom_record.items())
    boom_lvl_list.sort(key=lambda x: x[1], reverse=True)
    top_booms = ""
    if len(boom_lvl_list):
        for entry in boom_lvl_list[:5]:
            top_booms += "SF{}: {} times\n".format(entry[0],entry[1])
        top_booms = top_booms[:-2]
    
    norm_cost_ls = list(map(lambda x: x[3],(filter(lambda x: x[4] == 0, ls))))
    boom_cost_ls = list(map(lambda x: x[3],(filter(lambda x: x[4] == 1, ls))))

    
    norm_cost_ls.sort()
    min_cost = costToWords(min(norm_cost_ls))
    median_cost = costToWords(norm_cost_ls[(simulations - boom_count)//2])
    average_cost = costToWords(sum(norm_cost_ls)/ len(norm_cost_ls))
    max_cost = costToWords(max(norm_cost_ls))
    

    booms = "{}/{}  :  {:.2%}".format(
        boom_count,
        simulations,
        boom_count/simulations)
    avg_boom_cost = 0
    if boom_count > 0:
        avg_boom_cost = costToWords(sum(boom_cost_ls)/ boom_count)
    
    stats = (min_cost, median_cost, average_cost, max_cost,
             booms, avg_boom_cost, top_booms)
    return stats



## tkinter ----------------------------------------------------------

root = tk.Tk()

canvas1 = tk.Canvas(root, width=320, height=450, bg = "turquoise3")
canvas1.pack()

# the label for user_name 
tk.Label(root, text = "Equipment Level",width=13, anchor="w").place(x = 40, y = 30)
entry1 = tk.Entry(root) 
canvas1.create_window(210, 40, window=entry1)

tk.Label(root, text = "Current Star", width=13, anchor="w").place(x = 40, y = 60) 
entry2 = tk.Entry(root) 
canvas1.create_window(210, 70, window=entry2)

tk.Label(root, text = "Desired Star", width=13, anchor="w").place(x = 40, y = 90)
entry3 = tk.Entry(root) 
canvas1.create_window(210, 100, window=entry3)

tk.Label(root, text = "Lowest Cost", width=13, anchor="w").place(x = 40, y = 160)
tk.Label(root, text = "Median Cost", width=13, anchor="w").place(x = 40, y = 190)
tk.Label(root, text = "Average Cost", width=13, anchor="w").place(x = 40, y = 220)
tk.Label(root, text = "Highest Cost", width=13, anchor="w").place(x = 40, y = 250)
tk.Label(root, text = "Boom Counts", width=13, anchor="w").place(x = 40, y = 300)
tk.Label(root, text = "Avg Boom Cost", width=13, anchor="w").place(x = 40, y = 330)
tk.Label(root, text = "Most Booms At", width=13, anchor="w").place(x = 40, y = 360)

lb1 = tk.Label(root, text = "", width=17, anchor="w")
lb1.place(x = 150, y = 160)

lb2 = tk.Label(root, text = "", width=17, anchor="w")
lb2.place(x = 150, y = 190)

lb3 = tk.Label(root, text = "", width=17, anchor="w")
lb3.place(x = 150, y = 220)

lb4 = tk.Label(root, text = "", width=17, anchor="w")
lb4.place(x = 150, y = 250)

lb5 = tk.Label(root, text = "", width=17, anchor="w")
lb5.place(x = 150, y = 300)

lb6 = tk.Label(root, text = "", width=17, anchor="w")
lb6.place(x = 150, y = 330)

lb7 = tk.Label(root, text = "", width=17, anchor="w")
lb7.place(x = 150, y = 360)

def generate(event=None):
    lvl, cs, ds = int(entry1.get()), int(entry2.get()), int(entry3.get())
    list_eq = [(lvl,cs,ds) for i in range(simulations)]
    list_eq = list(map(createequip, list_eq))
    list_eq = list(map(powerup, list_eq))
    stats = getStats(list_eq, simulations)
    lb1.configure(text = stats[0])
    lb2.configure(text = stats[1])
    lb3.configure(text = stats[2])
    lb4.configure(text = stats[3])
    lb5.configure(text = stats[4])
    lb6.configure(text = stats[5])
    lb7.configure(text = stats[6])
    return None 
    
generate_button = tk.Button(root, text = "Generate", width = 17,
          command = generate).place(x = 145,y = 120) #refresh button
root.bind('g',generate)


root.mainloop()
