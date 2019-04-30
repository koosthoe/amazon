import svgutils.transform as sg
import csv
import os
import PyPDF2
import pyautogui
import time
import shutil
from datetime import date
import vinylFunctions
import SkuFunctions
import re




ErrorFiles = []


def mainCode(ordernum, sku, Line1Text, Line1Font, Line1Color, Line2Text, Line2Font, Line2Color, Line3Text, Line3Font, Line3Color, place, amount):



    Sku = sku.replace(" ", "")
    orderNum = ordernum

    LineOne = Line1Text
    LineTwo = Line2Text
    LineThree = Line3Text
    ColorLine1 = Line1Color
    ColorLine2 = Line2Color
    ColorLine3 = Line3Color
    FontLine1 = Line1Font
    FontLine2 = Line2Font
    FontLine3 = Line3Font




    row_counter = 0
    with open("bin/SkuVariables.csv") as d:
        reader = csv.reader(d)

        row_counter = sum(1 for row in reader)
        print(row_counter)


    recogSku = False
    for currentRowSku in range(1, row_counter):
        with open("bin/SkuVariables.csv") as d:
            reader = csv.reader(d)
            # next(reader)  # skip header
            reader = list(reader)

            if reader[currentRowSku][0] in Sku:
                recogSku = True




    print(orderNum)



    if os.path.isdir("bin/CharLibrary/"+ FontLine1) == False:
        FontLine1 = "default"

    if os.path.isdir("bin/CharLibrary/"+ FontLine2) == False:
        FontLine2 = "default"

    if os.path.isdir("bin/CharLibrary/"+ FontLine3) == False:
        FontLine3 = "default"

    HexColor1 = ColorLine1
    HexColor2 = ColorLine2
    HexColor3 = ColorLine3


    NameNum = "NameNum"



    FoundError = False
    LineChecker = False
    while LineChecker == False:

        if (LineOne == "--EMPTY--" or LineOne == "") and NameNum.lower() in Sku.lower() and (LineTwo != "--EMPTY--" and LineTwo != ""):
            lineOneCount = len(LineOne)
            LineChecker = True

        elif LineOne != "--EMPTY--" and LineOne != "":
            lineOneCount = len(LineOne)
            LineChecker = True
        elif (LineOne == "--EMPTY--" or LineOne == "") and ((LineTwo != "--EMPTY--" and LineTwo != "") or (LineThree != "--EMPTY--" and LineThree != "")):
            LineOne = LineTwo
            LineTwo = LineThree
            LineThree = "--EMPTY--"
            #lineOneCount = 0
        else:
            FoundError = True
            break


    if FoundError == True:
        ErrorFiles.append(orderNum)
        return ErrorFiles



    if LineTwo != "--EMPTY--" and LineTwo != "":
        lineTwoCount = len(LineTwo)
    elif (LineTwo == "--EMPTY--" or LineTwo == "") and (LineThree != "--EMPTY--" and LineThree != ""):
        LineTwo = LineThree
        lineTwoCount = len(LineTwo)
        LineThree = "--EMPTY--"
    else:
        lineTwoCount = 0
    if LineThree != "--EMPTY--" and LineThree != "":
        lineThreeCount = len(LineThree)
    else:
        lineThreeCount = 0
    print("1: " + str(lineOneCount))
    print(lineTwoCount)
    print(lineThreeCount)


    MaxLineCount = max(lineOneCount, lineTwoCount, lineThreeCount)
    print("MaxlineCount "+str(MaxLineCount))






    numberOfLines =  vinylFunctions.numberOfLinesCheck(lineOneCount, lineTwoCount, lineThreeCount)

    print("number of line: "+str(numberOfLines))

    LineOneFiles = []
    LineTwoFiles =[]
    LineThreeFiles = []
    FoundError = False
    for x in range(1,numberOfLines+1):
        if x == 1:
            print(FontLine1)
            LineOneFiles = vinylFunctions.FileFinder(LineOne, FontLine1)
            if LineOneFiles[0] == "ERROR":
                FoundError = True
        if x == 2:
            LineTwoFiles = vinylFunctions.FileFinder(LineTwo, FontLine2)
            if LineTwoFiles[0] == "ERROR":
                FoundError = True
        if x == 3:
            LineThreeFiles = vinylFunctions.FileFinder(LineThree, FontLine3)
            if LineThreeFiles[0] == "ERROR":
                FoundError = True

    if FoundError is True:
        print("ERROR")
        ErrorFiles.append(orderNum)
        return ErrorFiles


    row_counter = 0
    with open("bin/SkuVariables.csv") as f:
        reader = csv.reader(f)

        row_counter = sum(1 for row in reader)
        print(row_counter)

    ABWidth = ''
    ABHeight = ''
    MaxLineHeight = ''
    SpacingData = ''
    LineSpacingData = ''

    print("hi")
    print("Sku: " + Sku)

    for currentRowSku in range(1, row_counter):
        with open("bin/SkuVariables.csv") as f:
            reader = csv.reader(f)
            # next(reader)  # skip header
            reader = list(reader)

            if reader[currentRowSku][0].lower() in Sku.lower():

                for item in reader[currentRowSku][1].splitlines():
                    #temp = item.split(':')
                    ABWidth=  item.rstrip().lstrip()
                for item in reader[currentRowSku][2].splitlines():
                    #temp = item.split(':')
                    ABHeight= item.rstrip().lstrip()
                for item in reader[currentRowSku][3].splitlines():
                    #temp = item.split(':')
                    MaxLineHeight= item.rstrip().lstrip()
                for item in reader[currentRowSku][4].splitlines():
                    #temp = item.split(':')
                    SpacingData= item.rstrip().lstrip()
                for item in reader[currentRowSku][5].splitlines():
                    #temp = item.split(':')
                    LineSpacingData = item.rstrip().lstrip()
    print("hello")
    print(LineSpacingData)

    LineSpacing = int(LineSpacingData)
    Spacing = int(SpacingData)



    NameNum = "NameNum"
    print("Sku: "+Sku)
    print("hi")

    if NameNum.lower() in Sku.lower():

        print("NameNum found")
        if LineOne == "--EMPTY--":
            NumOnlyProcess(Sku, orderNum, LineTwoFiles, lineTwoCount, ABWidth, ABHeight, MaxLineHeight, Spacing, LineSpacing, FontLine1, FontLine2, HexColor1, HexColor2, HexColor3, LineOne, LineTwo, LineThree,  place, amount)
        else:
            NameNumProcess(Sku, orderNum, LineOneFiles, LineTwoFiles, lineOneCount, lineTwoCount, numberOfLines, ABWidth, ABHeight, MaxLineHeight, Spacing, LineSpacing, FontLine1, FontLine2, HexColor1, HexColor2, HexColor3, LineOne, LineTwo, LineThree,  place, amount)
        print("bye")
        #currentRow += 1
        return ErrorFiles

    print(FontLine1)
    LargestLine= vinylFunctions.largestLineFinder(LineOneFiles, LineTwoFiles, LineThreeFiles, Spacing, FontLine1, FontLine2, FontLine3)
    print("largest line: " + str(LargestLine))
    SizeScale = float((float(int(ABWidth)-20.0))/float(LargestLine))

    print("scale: " + str(SizeScale))

    HeightLine1 = 0
    HeightLine2 = 0
    HeightLine3 = 0
    LastLineHeight = 0

    if numberOfLines >= 1:
        HeightLine1 = int(vinylFunctions.maxHeightFinder(LineOneFiles, FontLine1))
        LastLineHeight = HeightLine1
    if numberOfLines >= 2:
        HeightLine2 = int(vinylFunctions.maxHeightFinder(LineTwoFiles, FontLine2))
        LastLineHeight = HeightLine2
    if numberOfLines == 3:
        HeightLine3 = int(vinylFunctions.maxHeightFinder(LineThreeFiles, FontLine3))
        LastLineHeight = HeightLine3


    HighestHeight = max(HeightLine1, HeightLine2, HeightLine3)

    if HighestHeight*SizeScale > int(MaxLineHeight):
        SizeScale = int(MaxLineHeight)/HighestHeight




    #totalHeight =  (HeightLine1 * SizeScale) + (HeightLine2 * SizeScale) + (HeightLine3 * SizeScale) + (LineSpacing * SizeScale * (numberOfLines-1))
    totalHeight = ((HighestHeight*numberOfLines) * SizeScale)+ (LineSpacing * (numberOfLines - 1)) - ((HighestHeight* SizeScale) - (LastLineHeight * SizeScale))

    if totalHeight  > int(ABHeight) -20:
        SizeScale = (int(ABHeight)-20)/((HighestHeight*numberOfLines)+(LineSpacing* (numberOfLines - 1)) - (HighestHeight - LastLineHeight))

    ArtboardWidth = float((float(LargestLine)* float(SizeScale)))+20.0
    #ArtboardHeight = Functions.FindArtboardHeight(LineSpacing, SizeScale, numberOfLines)+70
    ArtboardHeight = ((HighestHeight*numberOfLines) * SizeScale)+ (LineSpacing  * (numberOfLines - 1))+20 - ((HighestHeight* SizeScale) - (LastLineHeight * SizeScale))


    fig = sg.SVGFigure(ArtboardWidth, ArtboardHeight)


    if lineOneCount > 0:
        count = 0
        widthArray = []
        widthArray.append(0)
        sumOfWids = 0
        for x in LineOneFiles:
            if x == " ":
                widthArray.append(Spacing*SizeScale*4)
                sumOfWids += Spacing*SizeScale*4
            else:
                pdf = PyPDF2.PdfFileReader("bin/CharLibrary/"+FontLine1+"/"+x[:-4] + ".pdf", "rb")
                p = pdf.getPage(0)
                temp = p.mediaBox.getWidth()
                widthArray.append(int(temp) * SizeScale)
                sumOfWids += (int(temp)+Spacing) * SizeScale
                print(p.mediaBox.getHeight())
            count += 1
        #print("art:" +str(ArtboardWidth) + " sum:" + str(sumOfWids-(Spacing*SizeScale)))
        startingPos = (ArtboardWidth/2) - (sumOfWids-(Spacing*SizeScale))/2
        print(startingPos)

        count = 0
        prevWids = 0
        for x in LineOneFiles:
            print(x)
            if x != " ":
                fig1 = sg.fromfile("bin/CharLibrary/"+FontLine1+"/"+x)
                plot1 = fig1.getroot()


                plot1.moveto(startingPos + prevWids + widthArray[count], 10, scale=SizeScale)
                fig.append(plot1)
                prevWids += widthArray[count] + (Spacing*SizeScale)
            else:
                prevWids += widthArray[count]

            count += 1

    if lineTwoCount > 0:
        count = 0
        widthArray = []
        widthArray.append(0)
        sumOfWids = 0
        for x in LineTwoFiles:
            if x == " ":
                widthArray.append(Spacing*SizeScale*4)
                sumOfWids += Spacing*SizeScale*4
            else:
                pdf = PyPDF2.PdfFileReader("bin/CharLibrary/"+FontLine2+"/"+x[:-4] + ".pdf", "rb")
                p = pdf.getPage(0)
                temp = p.mediaBox.getWidth()
                widthArray.append(int(temp) * SizeScale)
                sumOfWids += (int(temp) + Spacing) * SizeScale
                print(p.mediaBox.getHeight())
            count += 1

        startingPos = (ArtboardWidth / 2) - (sumOfWids - (Spacing * SizeScale)) / 2

        count = 0
        prevWids = 0
        for x in LineTwoFiles:
            if x != " ":
                fig1 = sg.fromfile("bin/CharLibrary/"+FontLine2+"/"+x)
                plot1 = fig1.getroot()


                plot1.moveto(startingPos + prevWids + widthArray[count], 10+(HighestHeight* SizeScale)+(LineSpacing), scale=SizeScale)
                fig.append(plot1)
                prevWids += widthArray[count] + (Spacing*SizeScale)
            else:
                prevWids += widthArray[count]
            count += 1


    if lineThreeCount > 0:
        count = 0
        widthArray= []
        widthArray.append(0)
        sumOfWids= 0
        for x in LineThreeFiles:
            if x == " ":
                widthArray.append(Spacing*SizeScale*4)
                sumOfWids += Spacing*SizeScale*4
            else:
                pdf = PyPDF2.PdfFileReader("bin/CharLibrary/"+FontLine3+"/"+x[:-4] + ".pdf", "rb")
                p = pdf.getPage(0)
                temp = p.mediaBox.getWidth()
                widthArray.append(int(temp) * SizeScale)
                sumOfWids += (int(temp) + Spacing) * SizeScale
                print(p.mediaBox.getHeight())
            count += 1

        startingPos = (ArtboardWidth / 2) - (sumOfWids - (Spacing * SizeScale)) / 2

        count = 0
        prevWids=0
        for x in LineThreeFiles:

            if x != " ":
                fig1 = sg.fromfile("bin/CharLibrary/"+FontLine3+"/"+x)
                plot1 = fig1.getroot()

                plot1.moveto(startingPos + prevWids + widthArray[count], 10+(HighestHeight* SizeScale)+(HighestHeight* SizeScale)+(LineSpacing)+(LineSpacing), scale=SizeScale)
                fig.append(plot1)
                prevWids += widthArray[count] + (Spacing*SizeScale)
            else:
                prevWids += widthArray[count]
            count += 1


    TextFile = ""
    print("hello")


    if amount >= 2:

        FileLoc = "bin/ConvertedFiles/SVG/" + Sku + "_"   + orderNum + "(" + str(place) + "OF" + str(amount) + ").svg"
        FileName = Sku + "_"  + orderNum + "(" + str(place) + "OF" + str(amount) + ").svg"
        fig.save(FileLoc)

        TextFile = FileLoc
    else:
        FileLoc = "bin/ConvertedFiles/SVG/"+Sku+"_"+orderNum + ".svg"
        FileName = Sku+"_"+orderNum+".svg"
        fig.save(FileLoc)

        TextFile = FileLoc





    return ErrorFiles


def OpenIllustrator():
    '''
    pyautogui.hotkey('Win', 'r')
    pyautogui.typewrite('illustrator')
    pyautogui.press('enter')
    return
    '''

    import subprocess

    script = '"C:\Program Files\Adobe\Adobe Illustrator CC 2019\Presets\en_US\Scripts\Onesie.jsx"'
    adobePath = r'"C:/Program Files/Adobe/Adobe Illustrator CC 2019/Support Files/Contents/Windows/Illustrator.exe"'
    subprocess.Popen("%s %s" % (adobePath, script))
    return



def FileChecker():

    check = False

    numfiles = len([f for f in os.listdir('bin/ConvertedFiles/SVG') if os.path.isfile(os.path.join('bin/ConvertedFiles/SVG', f))])
    numfiles2 = len([f for f in os.listdir('bin/ConvertedFiles/PDF') if os.path.isfile(os.path.join('bin/ConvertedFiles/PDF', f))])

    if(numfiles2 == (numfiles)+1):
            check = True

    return check



def Reset():
    dir_name = "bin/ConvertedFiles/PDF"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".svg"):
            os.remove(os.path.join(dir_name, item))
        if item.endswith(".pdf"):
            os.remove(os.path.join(dir_name, item))

    dir_name = "bin/ConvertedFiles/svg"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".svg"):
            os.remove(os.path.join(dir_name, item))



def Organize():
    time.sleep(2)
    dir_name = "bin/ConvertedFiles/PDF"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".svg"):
            os.remove(os.path.join(dir_name, item))


    dir_name = "bin/ConvertedFiles/svg"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".svg"):
            os.remove(os.path.join(dir_name, item))

    today = str(date.today())
    print(today)

    SOURCE_DIR = 'bin/ConvertedFiles/PDF'
    DEST_DIR = 'ReadyFiles/'+today

    if os.path.isdir(DEST_DIR) == False:
        os.makedirs(DEST_DIR)

    for fname in os.listdir(SOURCE_DIR):
        if fname.lower().endswith('.pdf'):
            shutil.move(os.path.join(SOURCE_DIR, fname), os.path.join(DEST_DIR, fname))

    return



def NameNumProcess(Sku, orderNum, LineOneFiles, LineTwoFiles,  lineOneCount, lineTwoCount, numberOfLines,  ABWidth, ABHeight, MaxLineHeight,Spacing, LineSpacing, Line1Font, Line2Font, HexColor1, HexColor2, HexColor3, LineOne, LineTwo, LineThree, place, amount):
    print("hellooooooo")
    row_counter = 0
    with open("bin/SkuVariables.csv") as f:
        reader = csv.reader(f)

        row_counter = sum(1 for row in reader)
        print(row_counter)
    numSize = ''
    for currentRow in range(1, row_counter):
        with open("bin/SkuVariables.csv") as f:
            reader = csv.reader(f)
            # next(reader)  # skip header
            reader = list(reader)
            if reader[currentRow][0].lower() in Sku.lower():


                for item in reader[currentRow][6].splitlines():
                    #temp = item.split(':')
                    numSize = item.rstrip().lstrip()
                    print(numSize)




    Line1Width = vinylFunctions.widthFinder(LineOneFiles, Spacing, Line1Font)
    Line2Width = vinylFunctions.widthFinder(LineTwoFiles, Spacing, Line2Font)
    print("largest line: " + str(Line1Width))

    Line1SizeScale = float((float(float(ABWidth) - 20.0)) / float(Line1Width))

    print(Line1SizeScale)


    HeightLine1 = 0
    HeightLine2 = 0

    LastLineHeight = 0
    Line2SizeScale = 0
    print(numberOfLines)

    if numberOfLines >= 1:
        HeightLine1 = float(vinylFunctions.maxHeightFinder(LineOneFiles, Line1Font))
        LastLineHeight = HeightLine1
    if numberOfLines >= 2:
        HeightLine2 = float(vinylFunctions.maxHeightFinder(LineTwoFiles, Line2Font))
        LastLineHeight = HeightLine2

        Line2SizeScale = float(numSize) / float(HeightLine2)



    #HighestHeight = max(HeightLine1, HeightLine2)

    if float(HeightLine1) * float(Line1SizeScale) > float(MaxLineHeight):
        Line1SizeScale = float(MaxLineHeight) / float(HeightLine1)

    Line1StartingVertical = ((LineSpacing)/2)-((float(HeightLine1) * float(Line1SizeScale))/2)


    LargestWidth = max(float((float(Line1Width) * float(Line1SizeScale))),  float(Line2Width)*float(Line2SizeScale))
    ArtboardWidth = float(LargestWidth) + 20.0
    # ArtboardHeight = Functions.FindArtboardHeight(LineSpacing, SizeScale, numberOfLines)+70
    ArtboardHeight = (float(HeightLine2) * float(Line2SizeScale)) + (float(HeightLine1) * float(Line1SizeScale)) + 20.0 + LineSpacing

    fig = sg.SVGFigure(ArtboardWidth, ArtboardHeight)
    print(lineOneCount)
    if lineOneCount > 0:
        count = 0
        widthArray = []
        widthArray.append(0)
        sumOfWids = 0
        for x in LineOneFiles:
            if x == " ":
                widthArray.append(Spacing * Line1SizeScale * 4)
                sumOfWids += Spacing * Line1SizeScale * 4
            else:
                pdf = PyPDF2.PdfFileReader("bin/CharLibrary/"+Line1Font+"/" + x[:-4] + ".pdf", "rb")
                p = pdf.getPage(0)
                temp = p.mediaBox.getWidth()
                widthArray.append(int(temp) * Line1SizeScale)
                sumOfWids += (int(temp) + Spacing) * Line1SizeScale
                print(p.mediaBox.getHeight())
            count += 1
        # print("art:" +str(ArtboardWidth) + " sum:" + str(sumOfWids-(Spacing*SizeScale)))
        startingPos = (ArtboardWidth / 2) - (sumOfWids - (Spacing * Line1SizeScale)) / 2
        print(startingPos)

        count = 0
        prevWids = 0
        for x in LineOneFiles:
            print(x)
            if x != " ":
                fig1 = sg.fromfile("bin/CharLibrary/"+Line1Font+"/" + x)
                plot1 = fig1.getroot()

                plot1.moveto(startingPos + prevWids + widthArray[count], 10 , scale=Line1SizeScale)
                fig.append(plot1)
                prevWids += widthArray[count] + (Spacing * Line1SizeScale)
            else:
                prevWids += widthArray[count]

            count += 1

    if lineTwoCount > 0:
        count = 0
        widthArray = []
        widthArray.append(0)
        sumOfWids = 0
        for x in LineTwoFiles:
            if x == " ":
                widthArray.append(Spacing * Line2SizeScale * 4)
                sumOfWids += Spacing * Line2SizeScale * 4
            else:
                pdf = PyPDF2.PdfFileReader("bin/CharLibrary/"+Line2Font+"/" + x[:-4] + ".pdf", "rb")
                p = pdf.getPage(0)
                temp = p.mediaBox.getWidth()
                widthArray.append(int(temp) * Line2SizeScale)
                sumOfWids += (int(temp) + Spacing) * Line2SizeScale
                print(p.mediaBox.getHeight())
            count += 1

        startingPos = (ArtboardWidth / 2) - (sumOfWids - (Spacing * Line2SizeScale)) / 2

        count = 0
        prevWids = 0
        for x in LineTwoFiles:
            if x != " ":
                fig1 = sg.fromfile("bin/CharLibrary/"+Line2Font+"/" + x)
                plot1 = fig1.getroot()

                plot1.moveto(startingPos + prevWids + widthArray[count], 10 + (float(HeightLine1) * float(Line1SizeScale))+int(LineSpacing), scale=Line2SizeScale)
                fig.append(plot1)
                prevWids += widthArray[count] + (Spacing * Line2SizeScale)
            else:
                prevWids += widthArray[count]
            count += 1

    print("hello")
    if amount >= 2:

        FileLoc = "bin/ConvertedFiles/SVG/" + Sku + "_"   + orderNum + "(" + str(place) + "OF" + str(amount) + ").svg"
        FileName = Sku + "_"  + orderNum + "(" + str(place) + "OF" + str(amount) + ").svg"
        fig.save(FileLoc)

        TextFile = FileLoc
    else:
        FileLoc = "bin/ConvertedFiles/SVG/"+Sku+"_"+orderNum + ".svg"
        FileName = Sku+"_"+orderNum+".svg"
        fig.save(FileLoc)

        TextFile = FileLoc
    return

def NumOnlyProcess(Sku, orderNum, LineTwoFiles, lineTwoCount, ABWidth, ABHeight, MaxLineHeight, Spacing, LineSpacing, numberOfOrders, orderplace, quantity, Line1Font, Line2Font, HexColor1, HexColor2, HexColor3, LineOne, LineTwo, LineThree,  place, amount):
    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    row_counter = 0
    with open("bin/SkuVariables.csv") as f:
        reader = csv.reader(f)

        row_counter = sum(1 for row in reader)
        print(row_counter)
    numSize = ''
    for currentRow in range(1, row_counter):
        with open("bin/SkuVariables.csv") as f:
            reader = csv.reader(f)
            # next(reader)  # skip header
            reader = list(reader)
            if reader[currentRow][0].lower() in Sku.lower():

                for item in reader[currentRow][6].splitlines():
                    # temp = item.split(':')
                    numSize = item.rstrip().lstrip()


    Line2Width = vinylFunctions.widthFinder(LineTwoFiles, Spacing, Line2Font)


    HeightLine1 = 0
    HeightLine2 = 0

    LastLineHeight = 0


    HeightLine2 = float(vinylFunctions.maxHeightFinder(LineTwoFiles, Line2Font))
    LastLineHeight = HeightLine2

    Line2SizeScale = float(numSize) / float(HeightLine2)

    # HighestHeight = max(HeightLine1, HeightLine2)





    ArtboardWidth = float( float(Line2Width) * float(Line2SizeScale)) + 20.0
    # ArtboardHeight = Functions.FindArtboardHeight(LineSpacing, SizeScale, numberOfLines)+70
    ArtboardHeight = (float(HeightLine2) * float(Line2SizeScale)) + 20.0

    fig = sg.SVGFigure(ArtboardWidth, ArtboardHeight)



    if lineTwoCount > 0:
        count = 0
        widthArray = []
        widthArray.append(0)
        sumOfWids = 0
        for x in LineTwoFiles:
            if x == " ":
                widthArray.append(Spacing * Line2SizeScale * 4)
                sumOfWids += Spacing * Line2SizeScale * 4
            else:
                pdf = PyPDF2.PdfFileReader("bin/CharLibrary/" + Line2Font + "/" + x[:-4] + ".pdf", "rb")
                p = pdf.getPage(0)
                temp = p.mediaBox.getWidth()
                widthArray.append(int(temp) * Line2SizeScale)
                sumOfWids += (int(temp) + Spacing) * Line2SizeScale
                print(p.mediaBox.getHeight())
            count += 1

        startingPos = (ArtboardWidth / 2) - (sumOfWids - (Spacing * Line2SizeScale)) / 2

        count = 0
        prevWids = 0
        for x in LineTwoFiles:
            if x != " ":
                fig1 = sg.fromfile("bin/CharLibrary/" + Line2Font + "/" + x)
                plot1 = fig1.getroot()

                plot1.moveto(startingPos + prevWids + widthArray[count], 10, scale=Line2SizeScale)
                fig.append(plot1)
                prevWids += widthArray[count] + (Spacing * Line2SizeScale)
            else:
                prevWids += widthArray[count]
            count += 1

    print("hello")
    if amount >= 2:

        FileLoc = "bin/ConvertedFiles/SVG/" + Sku + "_"   + orderNum + "(" + str(place) + "OF" + str(amount) + ").svg"
        FileName = Sku + "_"  + orderNum + "(" + str(place) + "OF" + str(amount) + ").svg"
        fig.save(FileLoc)

        TextFile = FileLoc
    else:
        FileLoc = "bin/ConvertedFiles/SVG/"+Sku+"_"+orderNum + ".svg"
        FileName = Sku+"_"+orderNum+".svg"
        fig.save(FileLoc)

        TextFile = FileLoc

    return