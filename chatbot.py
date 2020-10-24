import csv

data = []

with open('.\solutions.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        #print(f'\t{row["Index"]}, {row["solution"]}, {row["priorityValue"]}, {row["trouble"]}, {row["subTrouble"]}')
        data.append([int(row["Index"]), row["solution"], int(row["priorityValue"]), row["trouble"], row["subTrouble"]])
        line_count += 1
    #print(f'Processed {line_count} lines.')



def takePriority(elem):
    return elem[2]

def sortSolutions(arr):
    arr.sort(key=takePriority, reverse = True)
    #print("sortedData", arr)

def incrementPriority(index, arr):
    for row in arr:
        if index == row[0]:
            row[2] += 1
            arr[index - 1] = row

def separateTroubles(arr):
    sepDict = {}
    for row in arr:
        if row[3] not in sepDict: #if trouble not in dictionary
            sepDict[f"{row[3]}"] = {} #then create a new dictionary for trouble
        if row[4] not in sepDict[f"{row[3]}"]: #if subTrouble not in dictionary
            sepDict[f"{row[3]}"][f"{row[4]}"] = [] #then create a new array for subtrouble
        sepDict[f"{row[3]}"][f"{row[4]}"].append(row[1]) #append to that subtrouble if subtrouble already exists
    return sepDict

incrementPriority(1, data)
sortSolutions(data)
finalDict = separateTroubles(data)

with open("solutions1.csv", mode = "w", newline = "") as solutionsFile:
    solutionsWriter = csv.writer(solutionsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    solutionsWriter.writerow(["Index", "solution", "priorityValue", "trouble", "subTrouble"])
    for row in data:
        solutionsWriter.writerow(row)



from fuzzywuzzy import process

# best match minimum threshold
MATCH_CONFIDENCE_THRESHOLD = 50
RETRY_LIMIT = 2

# problems and solutions
base_layer = {


    'CNC': finalDict,
    'EDM': {'thing go brr': ["F"],
            'no powa': ["Also F"]
            }
}


layer = base_layer  # which layer of the nested dict we are atm
topic = ""
troubleshooting = False
retry_counter = 0 # Count attempts to provide automatic help

# this two to be substituted by discord bot
def stub_input(msg):
    return input(msg)

# discord bot should implement exit functionality and input validations
def stub_output(msg):
    print(msg)

def print_help(layer):
    problems = ', '.join(list(layer.keys()))
    stub_output("Is it related to this? {}...".format(problems))

while True:
    if not troubleshooting: # pin down the cause
        match = ( process.extractOne(stub_input("Whats the problem {}: ".format(topic)), layer.keys()) )

        subcat = match[0]
        confidence = match[1]

        if confidence < MATCH_CONFIDENCE_THRESHOLD:
            stub_output("Sorry, didnt get that.")
            retry_counter += 1
            if retry_counter > RETRY_LIMIT:
                print_help(layer)
            continue

        retry_counter=0
        layer = layer[subcat]
        topic = topic+">"+subcat

        if not isinstance(layer, dict):
            troubleshooting = True

    else: #provide troubleshooting help
        stub_output("Hmm.. lets try a few things")
        for t in layer:
            stub_output(t)
            res = stub_input("did that work?")
            if res == "yes":
                stub_output("Bye!")
                break
        break
