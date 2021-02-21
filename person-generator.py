import tkinter as tk
import csv
from random import randint
import sys
import pandas

# Configure pandas to handle state csv data files
pandas.set_option('display.max_columns', None)


# Variables to make things work
states = ["AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NM", "NV", "OR", "UT", "WA", "WY"]     # Defines valid states

# Update user input variables
def accept_inputs():
    """
    Place the data input by the user into input variables
    """
    global city
    city = cityEntry.get()
    global state
    state = stateList.get()
    global zipCode
    zipCode = zipEntry.get()
    global age
    age = ageEntry.get()
    global dob
    dob = dobEntry.get()
    global amount
    amount = amountEntry.get()
    if amount == "":        # If no amount defined, generate 1
        amount = 1
    global export
    export = csvVar.get()
    if export == 1:
        export = True

    # Move to generate addresses
    generate(amount)
    return

# Generate peron(s)
def generate(count):
    """
    Takes the input and generates the person information
    based on the input information.
    """

    # Open correct state raw data
    with open(state.lower()+".csv", mode='r', newline="\n", errors='ignore') as stateData:
        data_types = {'NUMBER': 'string', 'STREET': 'str', 'CITY': 'str', 'POSTCODE': 'str'}
        use_columns = ['NUMBER', 'STREET', 'CITY', 'POSTCODE']
        reader = pandas.read_csv(stateData, dtype=data_types, usecols=use_columns, encoding='utf-8')
        address_data = [list(row) for row in reader.values]
        data = list()
        for i in range(0, int(count)):
            data.append(address_data[randint(0, len(address_data))])
    if export:
        export_data(data)
    show_output(data)
    return

# Export data
def export_data(output_data):
    """
    Exports the generated data to a csv file
    """
    with open("output.csv", mode='w', newline="\n") as output:
        writer = csv.writer(output, delimiter=',')
        # Write the output header
        writer.writerow(["input_state", "input_number_to_generate", "output_content_type", "output_content_value"])

        # Write data to output file
        for i in output_data:
            writer.writerow([state, amount, "street address", i])
    return

# Display the generated output
def show_output(output_data):
    # Show number of generated addresses
    outputAmountLabel = tk.Label(text="Number of addresses generated: "+str(amount))
    outputAmountLabel.grid(row=9, column=0, columnspan=3, sticky=tk.W)

    # Create text box to display output and the header
    output_text = tk.Text()
    output_text.insert("1.0", "input_state,input_number_to_generate,output_content_type,output_content_value\n")

    # Add the generated data to the text box
    for i in output_data:
        # build output string
        out_string = str(state)+","+str(amount)+",street address,"+str(i)+"\n"
        # Insert output string to textbox
        output_text.insert("2.0", out_string)
    # Display the output text
    output_text.grid(row=10, column=0, columnspan=4, sticky='nsew')
    return


# Import CSV
try:
    csv_input = pandas.read_csv(sys.argv[1], names=["input_state", "input_number_to_generate"])
    state = csv_input.input_state.to_list()[1]
    amount = csv_input.input_number_to_generate.to_list()[1]
    export = True
    generate(amount)
except IndexError:
    pass


# Create GUI window
window = tk.Tk()
window.title("Person Generator")

titleFrame = tk.Label(text="Build-a-Person")
titleFrame.grid(row=0, column=0, columnspan=4)

addressLabel = tk.Label(text="Address")
addressLabel.grid(row=1, column=0, sticky=tk.W)

cityLabel = tk.Label(text="City")
cityLabel.grid(row=1, column=2, sticky=tk.W)
cityEntry = tk.Entry(width=10)
cityEntry.grid(row=1, column=3)

stateLabel = tk.Label(text="State")
stateLabel.grid(row=2, column=0, sticky=tk.W)
stateList = tk.StringVar(window)
stateList.set("-")
stateEntry = tk.OptionMenu(window, stateList, *states)
stateEntry.grid(row=2, column=1)

zipLabel = tk.Label(text="Zip")
zipLabel.grid(row=2, column=2, sticky=tk.W)
zipEntry = tk.Entry(width=10)
zipEntry.grid(row=2, column=3)

idLabel = tk.Label(text="ID Number")
idLabel.grid(row=3, column=0, sticky=tk.W)

ageLabel = tk.Label(text="Age")
ageLabel.grid(row=4, column=0, sticky=tk.W)
ageEntry = tk.Entry(width=10)
ageEntry.grid(row=4, column=1)

heightLabel = tk.Label(text="Height")
heightLabel.grid(row=4, column=2, sticky=tk.W)

dobLabel = tk.Label(text="Date of Birth")
dobLabel.grid(row=5, column=0, sticky=tk.W)
dobEntry = tk.Entry(width=10)
dobEntry.grid(row=5, column=1)
dobFormat = tk.Label(text="(YYYY-MM-DD)")
dobFormat.grid(row=6, column=0, sticky=tk.W)

weightLabel = tk.Label(text="Weight")
weightLabel.grid(row=5, column=2, sticky=tk.W)

amountLabel = tk.Label(text="Amount to Generate")
amountLabel.grid(row=7, column=0, sticky=tk.W)
amountEntry = tk.Entry(width=10)
amountEntry.grid(row=7, column=1)

csvLabel = tk.Label(text="Export CSV")
csvLabel.grid(row=7, column=2, sticky=tk.W)
csvVar = tk.IntVar()
csvToggle = tk.Checkbutton(window, variable=csvVar)
csvToggle.grid(row=7, column=3)

generateButton = tk.Button(text="Generate", width=6, height=1, command=lambda: accept_inputs())
generateButton.grid(row=8, column=3)

# Start GUI
window.mainloop()