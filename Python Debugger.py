import importlib.util #library used to import modules by their file path
import sys
import timeit
import os
from PIL import Image, ImageDraw, ImageFont
import imageio
import inspect
import yaml

file = importlib.util.spec_from_file_location("", "hello")
if (len(sys.argv) != 4) and (len(sys.argv) != 5):
    print("Error: Ensure that 4 arguments are providedthe third should be the program you want to debug")
    print("The first one is 'Python Debugger.py', which is the debugger")
    print("The second should be the function name")
    print("The third should be the name of the program you want to debug, if it's in the same directory as the debugger, or if it's not, the full file path of program")
    print("The fourth parameter should be the name you want to give the GIF that this debugger creates of the debugging process. Make sure to include the file extension '.gif'")
    print("The fifth parameter is optional, and is the name of the yaml file if one is used")
    sys.exit()


global func_name
func_name = sys.argv[1]
file_path = sys.argv[2]
gif_name = sys.argv[3]
if (gif_name[len(gif_name) - 4] + gif_name[len(gif_name) - 3] + gif_name[len(gif_name) - 2] + gif_name[len(gif_name) - 1]) != (".gif"):
    print("Error: Ensure the fourth parameter ends with the file extension '.gif'")
    sys.exit()
if (file_path[len(file_path) - 3] + file_path[len(file_path) - 2] + file_path[len(file_path) - 1]) != (".py"):
    print("Error: Ensure that the file is a python program. Remember: the second argument is the function name and the third is the file name")
    sys.exit()
try:
    spec = importlib.util.spec_from_file_location("", file_path)
except FileNotFoundError:
    print("Error: Ensure the program exists in the same directory as this debugger or input the full file path of the program you want to debug")
    sys.exit()
mod = importlib.util.module_from_spec(spec) 
spec.loader.exec_module(mod)


if len(sys.argv) == 5:
    yaml_file_name = sys.argv[4]
    if (yaml_file_name[len(yaml_file_name) - 4] + yaml_file_name[len(yaml_file_name) - 3] + yaml_file_name[len(yaml_file_name) - 2] + yaml_file_name[len(yaml_file_name) - 1]) == (".yml"):
        try:
            yaml_file = open(yaml_file_name)
        except FileNotFoundError:
            print("Error: Make sure the yaml file either exists in the same directory as the debugger or input the full file path to the yaml file")
            sys.exit()
        file_config_details = list(yaml.load(yaml_file, Loader = yaml.FullLoader).values())
        config_details = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(file_config_details)):
            if (type(file_config_details[i]) is int) or (type(file_config_details[i]) is float):
                if file_config_details[i] >= 100:
                    config_details[5] = file_config_details[i]
                    config_details[6] = file_config_details[i]
                elif file_config_details[i] >= 10:
                    config_details[2] = file_config_details[i]
                elif file_config_details[i] >= 0:
                    config_details[0] = file_config_details[i]

            if type(file_config_details[i]) is str:
                if file_config_details[i][len(file_config_details[i]) - 4 : len(file_config_details[i])] == ".ttf":
                    config_details[1] = file_config_details[i]
                else:
                    config_details[3] = file_config_details[i]

            if type(file_config_details[i]) is bool:
                config_details[4] = file_config_details[i]

            if type(file_config_details[i]) is list:
                config_details[i] = file_config_details[i]
    else:
        print("Error: Make sure you include the file extension '.yml'")
        sys.exit()
else:
    config_details = []
    config_details.append(1.5)
    config_details.append("Antaro.ttf")
    config_details.append(15)
    config_details.append("")
    config_details.append(False)
    config_details.append(1280)
    config_details.append(720)
    config_details.append([])
    config_details.append([])
print(config_details)

    
source_lines = []
text_file = open("Debugger Output.txt", "w")
try:
    text_file.write(inspect.getsource(eval("mod." + func_name)))
except AttributeError:
    print("Error: Ensure the function exists in the program you want to debug")
    sys.exit()
text_file.close()
text_file = open("Debugger Output.txt", "r")
one_line = "####"
while one_line != "":
    one_line = text_file.readline()
    source_lines.append(one_line)
text_file.close()
text_file = open("Debugger Output.txt", "w")
text_file.close()

images = []
img = Image.new("RGBA", (config_details[5], config_details[6]), "white")
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype(config_details[1], size = config_details[2])
except OSError:
    print("Error: Sorry, that font is not supported")
    sys.exit()
draw.text((0, 0), config_details[3], fill = "rgb(0, 0, 0)", font = font)
images.append(img)
img = Image.new("RGBA", (config_details[5], config_details[6]), "white")
draw = ImageDraw.Draw(img)
image_line_counter = 0
for line in source_lines:
    draw.text((0, image_line_counter), line, fill = "rgb(0, 0, 0)", font = font)
    image_line_counter += (config_details[2] + 5)
image_line_counter = 0
if config_details[4] == True:
    draw.text((1000, 700), "Generated by " + sys.argv[2], fill = "rgb(0, 0, 0)", font = font)
images.append(img)
img.save("Image.png")

text_file = open("Debugger Output.txt", "w") #opens the text file for which the output is written to

def trace_calls(frame, event, arg): #traces the call of the function to be tested
    if frame.f_code.co_name == func_name:
        global starting_line_number
        starting_line_number = frame.f_lineno + 1
        return trace_lines #calls upon function 'trace_lines' for each frame

var_values = [] #list that stores the values of the current variables
var_names = [] #list that stores the names of the current variables 
var_data_types = [] #list that stores the data type of each variable, for it to be output at the end
var_line_numbers = [] #list that stores the line number on which each variable was instantiated on
record_of_values = [] #a list in which each element will be list, and each of these elements will record the values thaat each value was assigned throughout the debugging process, for it to be output at the end
line_counters = [] #each element keeps track of a particular line number and counts how many times it has run e.g. for a for loop
times = [] #a list in which each element is a list that tracks the time for each particular line to execute e.g. if line 3 was executed twice the element for line 3 will store the time for each of the 2 instances where the line was executed
overall_total = 0.0 #a running total to calculate how long the program took to execute
step_number = 1 #global variable that is a step number output to the text file
output_line_number = (len(source_lines) + 5) * config_details[2] #a global variable to track the line number of the video frame on which the function output should be written
def trace_lines(frame, event, arg):
    global var_values
    global var_names
    global var_data_types
    global var_line_numbers
    global record_of_values
    global times
    global overall_total
    global previous_line_number
    global step_number
    global images
    global image_line_counter
    global font
    global draw
    global img
    global output_line_number

    if frame.f_lineno > starting_line_number: #checks that the appropriate line number is reached at the start so any new variables can be added to the dictionary
        #this statement solves a minor bug where the same line number is output twice towards the end
        number_subtracted = starting_line_number    
        if len(line_counters) - 1 < frame.f_lineno - number_subtracted - 1:
            line_counters.append(1) #adds a new element to line_counters if a new line has been reached i.e. not in a loop
            times.append([]) #adds a new list element to times so that the times of execution of this new line can be tracked
        else:
            line_counters[frame.f_lineno - number_subtracted - 1] += 1 #if an already existing line is being executed, then increment the appropriate element of line_counters           

        img = Image.open("Image.png")
        draw = ImageDraw.Draw(img)
        if len(frame.f_locals) != len(var_values): #checks whether a new variable has been created
            #unpacks the names of the variables and the values of the variables from the dictionary 'frame.f_locals' into 2 separate global lists
            var_names = list(frame.f_locals.keys()) 
            var_values = list(frame.f_locals.values())
            var_name_changed = var_names[len(var_names) - 1]
            var_value_changed = var_values[len(var_values) - 1]
            #checks the data type of the new variable and adds the data type of the new variable to var_data_types
            if type(var_value_changed) is int:
                var_data_types.append("Integer")
            elif type(var_value_changed) is float:
                var_data_types.append("Floating point")
            elif type(var_value_changed) is str:
                var_data_types.append("String")
            elif type(var_value_changed) is bool:
                var_data_types.append("Boolean")
            elif type(var_value_changed) is list:
                var_data_types.append("List")
            var_line_numbers.append(frame.f_lineno - number_subtracted) #a new variable has been created and therefore var_line_numbers needs to be appended with the line number this new variable was instantiated on
            record_of_values.append([]) #record_of_values also needs to be appended with a new list element to track the values this variable is assigned throughout the debugging of the program
            record_of_values[len(record_of_values) - 1].append(var_value_changed) #appends the appropriate list element of record_of_values with the value with which this new variable has been instantiated with
            #outputs the name and value of the new variable/list to both the console window and the text file
            try:
                text_file.write("Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of " + var_name_changed + " is assigned " + str(var_value_changed) + "\n")
            except IndexError:
                for i in range((frame._lineno - number_subtracted - 1) - (len(line_counters) - 1)):
                    line_counters.append(1)
                text_file.write("Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of " + var_names_changed + " is assigned " + str(var_value_changed) + "\n")
            message = "Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of " + var_name_changed + " is assigned " + str(var_value_changed)
            print(message)
            display_name = True
            for variable in config_details[7]:
                if variable == var_name_changed:
                    display_name = False
                    break        
            if display_name == True:
                for variable in config_details[8]:
                    print(variable)
                    if variable == var_name_changed:
                        message = "Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of pointer variable is pointing to element " + str(var_value_changed)
                draw.text((450, image_line_counter), message, fill = "rgb(0, 255, 0)", font = font)  
        else:
            #checks whether any previous variabls/lists have been changed
            temp_var_values = list(frame.f_locals.values()) 
            for i in range(len(temp_var_values)):
                if temp_var_values[i] != var_values[i]:
                    record_of_values[i].append(temp_var_values[i]) #updates the appropriate list element of record_of_values with the new value of the variable
                    #outputs the new and old values of the variable to both the console window and the text file
                    try:
                        text_file.write("Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of " + var_names[i] + " is changed from " + str(var_values[i]) + " to " + str(temp_var_values[i]) + "  " + str(overall_total) + " seconds   " + str(step_number) + "\n")
                    except IndexError:
                        for i in range((frame._lineno - number_subtracted - 1) - (len(line_counters) - 1)):
                            line_counters.append(1)
                        text_file.write("Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of " + var_names[i] + " is changed from " + str(var_values[i]) + " to " + str(temp_var_values[i]) + "  " + str(overall_total) + " seconds   " + str(step_number) + "\n")
                    message = "Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of " + var_names[i] + " is changed from " + str(var_values[i]) + " to " + str(temp_var_values[i])
                    print(message)
                    display_name = True
                    for variable in config_details[7]:
                        if variable == var_names[i]:
                            display_name = False
                            break
                    if display_name == True:
                        for variable in config_details[8]:
                            print(variable)
                            if variable == var_names[i]:
                                message = "Line " + str(frame.f_lineno - number_subtracted) + ", running " + str(line_counters[frame.f_lineno - number_subtracted - 1]) + " times: Value of pointer variable is pointing to " + str(temp_var_values[i])
                        draw.text((450, image_line_counter), message, fill = "rgb(0, 255, 0)", font = font)
                    break
                
            var_values = temp_var_values
        image_line_counter += (config_details[2] + 5)  
        try:
            times[frame.f_lineno - number_subtracted - 1].append(timeit.default_timer()) #times how long it took to execute the line
        except IndexError:
            times.append([])
            times.append([])
            times[frame.f_lineno - number_subtracted - 1].append(timeit.default_timer())
        overall_total += times[frame.f_lineno - number_subtracted - 1][len(times[frame.f_lineno - number_subtracted - 1]) - 1] #increments the overall total for the execution of the whole program
        step_number += 1
        #the following lines average the time spent on the current line, if the line has been executed multiple times in a loop and outputs the results
        total = 0.0
        for i in range(len(times[frame.f_lineno - number_subtracted - 1])):
            total += times[frame.f_lineno - number_subtracted - 1][i]
        average = total / len(times[frame.f_lineno - number_subtracted - 1])
        text_file.write("Total time spent on line: " + str(total) + " seconds     Average time spent on line: " + str(average) + " seconds\n")
        print("Total time spent on line: " + str(total) + " seconds     Average time spent on line: " + str(average) + " seconds")
        draw.text((1000, image_line_counter - (config_details[2] + 5)), "Time spent: " + str(total)[:5] + " seconds", fill = "rgb(255, 0, 0)", font = font)
        if source_lines[frame.f_lineno - number_subtracted].strip()[:5] == "print":
            output = source_lines[frame.f_lineno - number_subtracted].strip()[:-2]
            output = output[7 : len(output)]
            draw.text((0, output_line_number), output, fill = "rgb(1, 150, 32)", font = font)
            output_line_number += (config_details[2] + 5)
        img.save("Image.png")
        draw.text((0, (config_details[2] + 5) * (frame.f_lineno - number_subtracted)), source_lines[frame.f_lineno - number_subtracted], fill = "rgb(255, 255, 255)", font = font)
        draw.text((0, (config_details[2] + 5) * (frame.f_lineno - number_subtracted)), source_lines[frame.f_lineno - number_subtracted], fill = "rgb(0, 0, 255)", font = font)
        images.append(img)      
        


sys.settrace(trace_calls)
try:
    eval("mod." + func_name)() #function to be tested is called. Note: if there are any parameters for the function to be debugged they NEED to be passed in this statement
except SyntaxError:
    print("Error: Ensure that 4 arguments are providedthe third should be the program you want to debug")
    print("The first one is 'Python Debugger.py', which is the debugger")
    print("The second should be the function name")
    print("The third should be the name of the program you want to debug, if it's in the same directory as the debugger, or if it's not, the full file path of program")
    print("The fourth parameter should be the name you want to give the GIF that this debugger creates of the debugging process. Make sure to include the file extension '.gif'")
    print("The fifth parameter is optional, and is the name of the yaml file if one is used")
    sys.exit()
except AttributeError:
    print("Error: Ensure the function exists in the program you want to debug")
    sys.exit()
except TypeError:
    parameters = input("Enter the parameters you would like to pass to this function: ").split(',')
    eval("mod." + func_name)(float(parameters[0]))
    
    
#this outputs the results of the debugging i.e. all the variables, their data types, the lines they were instantiated on and the total time for execution
print()
for i in range(len(var_names)):
    text_file.write(var_data_types[i] + " variable of name " + var_names[i] + " instantiated on line " + str(var_line_numbers[i]) + " function '" + func_name + "'\n")
    print(var_data_types[i] + " variable of name " + var_names[i] + " instantiated on line " + str(var_line_numbers[i]) + " function '" + func_name + "'")
    text_file.write("List of values that " + var_names[i] + " had been assigned: " + str(record_of_values[i]) + "\n")
    print("List of values that " + var_names[i] + " had been assigned: " + str(record_of_values[i]))
    text_file.write("\n")
    print()

text_file.write("\n")
print()
for i in range(len(line_counters)):
    text_file.write("Line " + str(i + 1) + " was executed " + str(line_counters[i]) + " times\n")
    print("Line " + str(i + 1) + " was executed " + str(line_counters[i]) + " times")

text_file.write("\n")
print()
text_file.write("Total time for execution: " + str(overall_total) + " seconds\n")
print("Total time for execution: " + str(overall_total) + " seconds")
text_file.close()
imageio.mimsave(gif_name, images, duration = config_details[0])
