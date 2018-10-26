# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:12:16 2018

@author: harisbha
"""


import re
import sys

from seqdiag import parser, builder, drawer


re_fileName = re.compile(r'M:(.*) F:')
re_funName = re.compile(r'F:(.*) L:')
re_funName_1 = re.compile(r'F:(.*) L#')

var_Entry_class = []
var_Exit_class = []
var_fun = []
var_flow_tuple = []
sys.stdout=open("output.txt","w")

def update_stack(entry_val,fun_name,exit_val):
    global var_Exit_class,var_Entry_class,var_fun
    var_Entry_class.append(entry_val)
    var_Exit_class.append(exit_val)
    var_fun.append(fun_name)
#    print(entry_val,"=!",fun_name,"=!",exit_val)


def seq_diag_draw():
    print ("***Sequence diagram draw*****")
    global var_Entry_class,var_fun,var_Exit_class
    var_function_flow = ""
    len_class= len(var_Entry_class)-6000
    i = 0
    for i in range (len_class):
#    while i < len_class:
#        print(i,"=",var_Entry_class[i],"=",var_fun[i],"=",var_Exit_class[i])
        if(var_Entry_class[i] != "0" and var_Exit_class[i] =="0"):
            var_in_function = var_Entry_class[i]
            if (var_fun[i] != "0"):
                _tmp_strp_fun = var_fun[i].split("(")
                var_fun_name = _tmp_strp_fun[0]
                if((i+1) < len(var_Entry_class)):
                    if (var_Exit_class[i+1] !="0"):
                        var_out_function = var_Exit_class[i+1]

                    else:
                        var_out_function = var_Entry_class[i+1]

                else:
                    break

    
#    var_fun_name = "Functioncall"
#    var_in_function = "BROWS    "
#    var_out_function = "Websvr"
            var_function_in_flow = u"""%s  -> %s [label = %s];"""%(var_in_function,var_out_function,var_fun_name)
#            var_function_out_flow = u"""%s <- %s;"""%(var_in_function,var_out_function)
            var_function_flow = var_function_flow + var_function_in_flow +"\n"
            
    diagram_definition = u"""
       seqdiag {
default_fontsize = 14;  // default value is 11
       %s
        }
    """%(var_function_flow)
#    diagram_definition = diagram_definition + "\n" +var_function_in_flow + "\n"+ var_function_out_flow
    print (diagram_definition)
    tree = parser.parse_string(diagram_definition)
    print (tree)
    diagram = builder.ScreenNodeBuilder.build(tree)
    draw = drawer.DiagramDraw('PNG', diagram, filename="seg_test_new.png")
    draw.draw()
    draw.save()    
    
with open("player.txt",encoding='cp850') as log:
    for line in log:

        var_entry = line.split("> |->",2) 
        var_exit = line.split("> <-|",2)

            
        if (len(var_entry)>1):
            
            if(re_fileName.search(line)):
                entry_class = (re_fileName.search(line).group(1))
            else:
                entry_class = "Entry_class_missing"
                print (">>>MIssing line",line)
            if (re_funName.search(line)):
                entry_fun = (re_funName.search(line).group(1))
            elif (re_funName_1.search(line)):
                entry_fun = (re_funName_1.search(line).group(1))
            else:
                entry_fun = "Fmissing"
                print (">>>F:missing",line)
#            print ("entry>>filename=", entry_class,"entry>>function name=", entry_fun,)
            update_stack(entry_class,entry_fun,"0")
        elif (len(var_exit)>1):
            if (re_fileName.search(line)):
                exit_val = (re_fileName.search(line).group(1))
            else:
                exit_val = "Exit_ClassName_missing"
                print (">>>Exit class:missing",line)
            if (re_funName.search(line)):
                entry_fun = (re_funName.search(line).group(1))
            elif (re_funName_1.search(line)):
                entry_fun = (re_funName_1.search(line).group(1))
#            print ("exit<< filename=", exit_val)
            update_stack("0",entry_fun,exit_val)

        else:
            print ("===skip===")
            
print("===final Table=====")
print ("Entry class","=","Function","=","Exit" , len(var_Entry_class) )
var_class_list = list(set(var_Entry_class))
for i in range (len(var_Entry_class)):
    print(i,"=",var_Entry_class[i],"=",var_fun[i],"=",var_Exit_class[i])

seq_diag_draw()
var_class_list.remove("0")
    
#
#for i in range(len(var_class_list)):
#    print (i,"=",var_class_list[i])
    
