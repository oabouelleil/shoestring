import csv
import random
from fuzzywuzzy import process

data = []

sorry_messages = ["So its related to {}, any more information?",
                  "Ah yes, {}, whats wrong with it?",
                  "{}... whats the problem?",
                  "Okay so {}, what about it",
                  "So its the {}, tell me more"]


with open('.\solutions.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        # print(f'\t{row["Index"]}, {row["solution"]}, {row["priorityValue"]}, {row["trouble"]}, {row["subTrouble"]}')
        data.append([int(row["Index"]), row["solution"], int(row["priorityValue"]), row["trouble"], row["subTrouble"]])
        line_count += 1
    # print(f'Processed {line_count} lines.')


def takePriority(elem):
    return elem[2]


def sortSolutions(arr):
    arr.sort(key=takePriority, reverse=True)
    # print("sortedData", arr)


def incrementPriority(index, arr):
    for row in arr:
        if index == row[0]:
            row[2] += 1
            arr[index - 1] = row


def separateTroubles(arr):
    sepDict = {}
    for row in arr:
        if row[3] not in sepDict:  # if trouble not in dictionary
            sepDict[f"{row[3]}"] = {}  # then create a new dictionary for trouble
        if row[4] not in sepDict[f"{row[3]}"]:  # if subTrouble not in dictionary
            sepDict[f"{row[3]}"][f"{row[4]}"] = []  # then create a new array for subtrouble
        sepDict[f"{row[3]}"][f"{row[4]}"].append(row[1])  # append to that subtrouble if subtrouble already exists
    return sepDict


incrementPriority(1, data)
sortSolutions(data)
finalDict = separateTroubles(data)

with open("solutions1.csv", mode="w", newline="") as solutionsFile:
    solutionsWriter = csv.writer(solutionsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    solutionsWriter.writerow(["Index", "solution", "priorityValue", "trouble", "subTrouble"])
    for row in data:
        solutionsWriter.writerow(row)


##############################
class ChatBot:
    # best match minimum threshold
    MATCH_CONFIDENCE_THRESHOLD = 50
    RETRY_LIMIT = 2

    # problems and solutions
    base_layer = {
        'EDM': {'thing go brr': {'F': ["If F, then undie"]},
                'no powa': ["Also F"]
                },
        "CNC": {}
    }

    layer = base_layer  # which layer of the nested dict we are atm
    topic = ""
    troubleshooting = False
    retry_counter = 0  # Count attempts to provide automatic help
    current_advice_index = -1  # Index within deepest layer list

    # def __init__(self):

    #   this two to be substituted by discord bot
    async def stub_input(self, msg):
        if not self.troubleshooting:
            print("Not troubleshooting")
            match = process.extractOne(msg, self.layer.keys())
            subcat = match[0]
            confidence = match[1]

            if confidence < self.MATCH_CONFIDENCE_THRESHOLD:
                print("Low confidence")
                await self.stub_output("Sorry, didnt get that.")
                self.retry_counter += 1

                if self.retry_counter > self.RETRY_LIMIT:
                    print("Too many tries")
                    await self.print_help(self.layer)

                return
            print("Reset retries")

            self.retry_counter = 0
            self.layer = self.layer[subcat]

            if not isinstance(self.layer, dict):
                self.troubleshooting = True
                await self.stub_output("Hmm.. lets try a few things")
            else:
                await self.stub_output(random.choice(sorry_messages).format(subcat))

        else:  # provide troubleshooting help
            print("Troubleshooting")
            if msg == "yes":
                await self.stub_output("Bye!")
                await self.reset()
                return
            # print("i=")
            self.current_advice_index += 1
            if self.current_advice_index <= len(self.layer):  # Double check whether it should be < or <=
                await self.stub_output(self.layer[self.current_advice_index])
                await self.stub_output("Did that work?")

    # discord bot should implement exit functionality and input validations
    async def stub_output(self, msg):
        print(msg)

    async def print_help(self, layer):
        problems = ', '.join(list(layer.keys()))
        await self.stub_output("Is it related to this? {}...".format(problems))

    async def reset(self):
        return
