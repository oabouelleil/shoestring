import csv
import json
import os


def parse_db(filename):
    data = []

    with open(filename) as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            data.append(
                [int(row["Index"]),
                 row["solution"],
                 int(row["priorityValue"]),
                 row["trouble"],
                 row["subTrouble"]])

            line_count += 1

    return data


def take_priority(elem):
    return elem[2]


def sort_solutions(arr):
    arr.sort(key=take_priority, reverse=True)


def increment_priority(index, arr):
    for row in arr:
        if index == row[0]:
            row[2] += 1
            arr[index - 1] = row


def separate_troubles(arr):
    sep_dict = {}

    for row in arr:
        if row[3] not in sep_dict:  # if trouble not in dictionary
            sep_dict[f"{row[3]}"] = {}  # then create a new dictionary for trouble

        if row[4] not in sep_dict[f"{row[3]}"]:  # if subTrouble not in dictionary
            sep_dict[f"{row[3]}"][f"{row[4]}"] = []  # then create a new array for subtrouble

        sep_dict[f"{row[3]}"][f"{row[4]}"].append(row[1])  # append to that subtrouble if subtrouble already exists

    return sep_dict


def update_db(data):  # updates priority values
    with open("solutions1.csv", mode="w", newline="") as solutionsFile:
        solutions_writer = csv.writer(solutionsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        solutions_writer.writerow(["Index", "solution", "priorityValue", "trouble", "subTrouble"])

        for row in data:
            solutions_writer.writerow(row)


# import me! base_layer = gen_dict('./db/)
def gen_dict(directory):
    base_layer = {}
    for filename in os.listdir(directory):
        data = parse_db(directory + filename)

        increment_priority(1, data)
        sort_solutions(data)
        final_dict = separate_troubles(data)

        base_layer['.'.join(filename.split('.')[:-1])] = final_dict

    return base_layer


if __name__ == "__main__":
    out_dict = gen_dict('./db/')
    print(json.dumps(out_dict, sort_keys=True, indent=4))
