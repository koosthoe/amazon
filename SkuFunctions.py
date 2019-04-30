import csv



def GetSkuVariables():


    row_counter = getrowcount()



    for currentRowSku in range(1, row_counter):
        with open("bin/SkuVariables.csv") as f:
            reader = csv.reader(f)
            # next(reader)  # skip header
            reader = list(reader)


    print(reader)
    return reader

def getrowcount():
    row_counter = 0
    with open("bin/SkuVariables.csv") as f:
        reader = csv.reader(f)

        row_counter = sum(1 for row in reader)
        print(row_counter)

    return row_counter