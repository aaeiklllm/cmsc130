import tkinter
import customtkinter
from tkinter import ttk
from tkinter import messagebox

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

window = customtkinter.CTk()
window.geometry("950x500")
window.title("Quine McCluskey Algorithm")
checked_minterms = set()
prime_implicants = set()

def change_appearance_mode(self, new_appearance_mode):
    customtkinter.set_appearance_mode(new_appearance_mode)

def on_closing(self, event=0):
    window.destroy()

def read_input():
    global minterms
    minterms=[]
    minterms=[int(i) for i in entry.get().strip().split()]
    minterms.sort

def clear_entry():
    entry.delete(0, "end")

def view_groupings():
    tk_textbox.configure(state="normal")  # configure textbox to be read-only 
    #make sure that the display textbox is clear
    tk_textbox.delete("1.0", customtkinter.END)
    group_minterms(minterms)
    tk_textbox.configure(state="disabled")  # configure textbox to be read-only 

def view_implicants():
    global chart
    tk_textbox.configure(state="normal")  # configure textbox to be read-only 
    #make sure that the display textbox is clear
    tk_textbox.delete("1.0", customtkinter.END)
    chart = print_prime_implicants(minterms)
    tk_textbox.configure(state="disabled")  # configure textbox to be read-only 

def view_results():
    tk_textbox.configure(state="normal")  # configure textbox to be read-only 
    #make sure that the display textbox is clear
    tk_textbox.delete("1.0", customtkinter.END)
    remove_EPI(chart)
    tk_textbox.configure(state="disabled")  # configure textbox to be read-only 

#=====================definitions=================================
def convert_to_variables(x): ##findvariables(x) in ref
   variables = []
   for i in range(len(x)):
       if x[i] == '1':
           variables.append(chr(i+65))
       elif x[i] == '0':
           variables.append(chr(i+65) + "'")
   return variables
 
def multiply_expressions(x, y):
   result = []
   for i in x:
       for j in y:
           tmp = multiply_minterms(i,j)
           result.append(tmp) if len(tmp) != 0 else None
   return result
 
def multiply_minterms(x, y):
   result = []
   for i in x:
       if i+"'" in y or (len(i)==2 and i[0] in y):
           return []
       else:
           result.append(i)
   for i in y:
       if i not in result:
           result.append(i)
   return result
 
def flatten_list(l):
   flat_list = []
   for sublist in l:
       flat_list.extend(l[sublist])
   return flat_list
 
def compare_binary(num1,num2): #compares minterms and check if difference is 1 or more, if 1 tells what index it is
   num_of_ones = 0
   for i in range(len(num1)):
       if num1[i] != num2[i]:
           diff_index = i
           num_of_ones += 1
           if num_of_ones > 1:
               return (False, None)
   return (True, diff_index)
 
def group_minterms(minterms): #
   size = len(bin(minterms[-1]))-2
   group = {}
 
   for i in minterms:
       try:
           group[bin(i).count('1')].append(bin(i)[2:].zfill(size))
       except KeyError:
           group[bin(i).count('1')] = [bin(i)[2:].zfill(size)]
 
   print_first_groups(group)
   compare_groups(group)
 
def print_first_groups(group):
    tk_textbox.insert(customtkinter.END, "\nGroup\t\tMinterms\t\tBinary of Minterms\n%s\n"%('.'*50))
    text = tk_textbox.get("0.0", "end")  # get text from line 0 character 0 till the end
    for i in sorted(group.keys()):
        tk_textbox.insert(customtkinter.END, "%5d:\n"%i)
        for j in group[i]:
            tk_textbox.insert(customtkinter.END, "\t\t    %-20d%s\n"%(int(j,2),j))
    tk_textbox.insert(customtkinter.END, "\n%s"%('-'*50))

def print_groups(group):
    tk_textbox.insert(customtkinter.END, "\nGroup\t\tMinterms\t\tBinary of Minterms\n%s\n"%('.'*50))
    for i in sorted(group.keys()):
        tk_textbox.insert(customtkinter.END, "%5d:\n"%i)
        for j in group[i]:
            tk_textbox.insert(customtkinter.END, "\t\t%-24s%s\n"%(','.join(find_merged_minterms(j)),j))
        tk_textbox.insert(customtkinter.END, "\n%s\n"%('-'*50))
 
def find_merged_minterms(binary):
   temp = []
   dash = binary.count('-')
   if dash == 0:
       return [str(int(binary, 2))]
 
   x = [bin(i)[2:].zfill(dash) for i in range(pow(2,dash))]
 
   for i in range(pow(2, dash)):
       binary_copy = binary[:]
       index = -1
       for j in x[0]:
           if index != -1:
               index = index+binary_copy[index+1:].find('-')+1
           else:
               index = binary_copy[index+1:].find('-')
           binary_copy = binary_copy[:index]+j+binary_copy[index+1:]
       temp.append(str(int(binary_copy,2)))
       x.pop(0)
   return temp
 
def compare_groups(group):
   while True:
       temp = group.copy()
       group = {}
       k = 0
      
       break_loop = True
 
 
       group_num = sorted(list(temp.keys())) #group numbers sorted in list
       for x in range(len(group_num)-1): #binary of minterms of current group
           for i in temp[group_num[x]]: #iterates to all elements of the binary of minterms of current group
               for j in temp[group_num[x+1]]: #iterates to all elements of the binary of minterms of next group
                   result = compare_binary(i, j)
                   if result[0]:
                       checked_minterms.add(i)
                       checked_minterms.add(j)
                       try:
                           common_binary = i[:result[1]]+'-'+i[result[1]+1:]
                           group[k].append(common_binary) if common_binary not in group[k] else None
 
                       except KeyError:
                           common_binary = [j[:result[1]]+'-'+j[result[1]+1:]]
                           group[k] = common_binary
 
                       break_loop = False  
           k += 1 
       prime_implicants = get_prime_implicants(temp)
       if break_loop:
           tk_textbox.insert(customtkinter.END, ("\nPrime Implicants: ", None if len(prime_implicants) == 0 else ', '.join(prime_implicants)))
           break
      
       print_groups(group)
 
def get_prime_implicants(temp):
   global prime_implicants
   unchecked_minterms = set(flatten_list(temp)).difference(checked_minterms)
   prime_implicants = prime_implicants.union(unchecked_minterms)
   return prime_implicants
 
def print_prime_implicants(minterms): #print prime implicants
   size = len(str(minterms[-1]))
   chart = {}
   tk_textbox.insert(customtkinter.END, '\nPrime Implicants chart:\n\n    Minterms    |%s\n%s'%(' '.join((' ' * (size - len(str(i)))) + str(i) for i in minterms),'.' * (len(minterms) * (size + 1) + 16)))
   for i in prime_implicants:
       merged_minterms = find_merged_minterms(i)
       y = 0
       tk_textbox.insert(customtkinter.END, ("\n%-16s|"%','.join(merged_minterms)))
      
       for j in merged_minterms:
           x = minterms.index(int(j)) * (size + 1)
           tk_textbox.insert(customtkinter.END, (' ' * abs(x - y) + ' ' * (size - 1) + 'X'))
           y = x + size
           try:
               chart[j].append(i) if i not in chart[j] else None
           except KeyError:
               chart[j] = [i]
       tk_textbox.insert(customtkinter.END, '\n' + '-' * (len(minterms) * (size + 1) + 16))
   return chart
 
def remove_EPI(chart):
   result = []
   for i in chart:
       if len(chart[i]) == 1:
           result.append(chart[i][0]) if chart[i][0] not in result else None
  
   for i in result:
       for j in find_merged_minterms(i):
           try:
               del chart[j]
           except KeyError:
               pass
   get_answer(chart, result)
 
def get_answer(chart, EPI): 
   answer=[]
   if(len(chart) == 0):
       answer = [convert_to_variables(i) for i in EPI]
   else:
       P = [[convert_to_variables(j) for j in chart[i]] for i in chart]
       while len(P) > 1:
           P[1] = multiply_expressions(P[0], P[1])
           P.pop(0)
       answer = [min(P[0], key = len)]
       answer.extend(convert_to_variables(i) for i in EPI)
   tk_textbox.insert(customtkinter.END, '\nAnswer: F = '+' + '.join(''.join(i) for i in answer))

#======================end==========================================

window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

left_frame = customtkinter.CTkFrame(master=window,
                                                 width=180,
                                                 corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nswe", rowspan=1)

display_frame = customtkinter.CTkFrame(master=window)
display_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

#left_frame widgets
left_frame.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
left_frame.grid_rowconfigure(5, weight=1)  # empty row as spacing
left_frame.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
left_frame.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

button_groupings = customtkinter.CTkButton(master=left_frame,
                                                text="View Groupings",
                                                command=view_groupings)
button_groupings.grid(row=2, column=0, pady=10, padx=20)

button_implicants = customtkinter.CTkButton(master=left_frame,
                                                text="View Implicants",
                                                command=view_implicants)
button_implicants.grid(row=3, column=0, pady=10, padx=20)

button_result = customtkinter.CTkButton(master=left_frame,
                                                text="View Results",
                                                command=view_results)
button_result.grid(row=4, column=0, pady=10, padx=20)

button_exit = customtkinter.CTkButton(master=left_frame,
                                                text="Exit",
                                                command=lambda: on_closing(window))
button_exit.grid(row=9, column=0, pady=10, padx=20)

#display_frame widgets
entry = customtkinter.CTkEntry(master=display_frame,
                                            width=400,
                                            placeholder_text="Enter minterms (separated by space): e.g. 1 2 3 4")
entry.grid(row=0, column=0, columnspan=1, pady=10, padx=20, sticky="nw")

tk_textbox = tkinter.Text(display_frame, highlightthickness=0, fg="green", bg="black")
tk_textbox.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

# create CTk scrollbar
ctk_textbox_scrollbar = customtkinter.CTkScrollbar(display_frame, command=tk_textbox.yview)
ctk_textbox_scrollbar.grid(row=1, column=1, sticky="ns")

# connect textbox scroll event to CTk scrollbar
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

btn_go = customtkinter.CTkButton(master=display_frame, text="Enter", command=read_input)
btn_go.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

window.mainloop()


