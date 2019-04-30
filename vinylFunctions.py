import PyPDF2
import os
import shutil



SymbolConvert ={'&' : 'Ampersand',
                '*' : 'Asterisk',
                '@' : 'At_Sign',
                '\\' : 'Backslash',
                '^' : 'Caret',
                ':' : 'Colon',
                ',' : 'Comma',
                '$' : 'Dollar_Sign',
                '"' : 'Double_Quote',
                '=' : 'Equals',
                '!' : 'Exclamation',
                '.' : 'Full_Stop',
                '`' : 'Grave_Accent',
                '>' : 'Greater_Than',
                '#' : 'Hash',
                '{' : 'Left_Brace',
                '[' : 'Left_Bracket',
                '(' : 'Left_Parenthesis',
                '<' : 'Less_Than',
                '-' : 'Minus',
                '%' : 'Percent',
                '+' : 'Plus',
                '?' : 'Question_Mark',
                ')' : 'Right_Parenthesis',
                '}' : 'Right_Brace',
                ']' : 'Right_Bracket',
                ';' : 'Semicolon',
                '\'' : 'Single_Quote',
                '/' : 'Slash',
                '~' : 'Tilde',
                '_' : 'Underscore',
                '|' : 'Vertical_Bar'


                }



ColorHexDic = { "#000000" : "#black",
                "#FF0000" : "#red",
                "#FFFF00" : "#yellow",
                "#000080" : "#blue",
                "#008000": "#green",
                "#FFFFFF" : "#white",
                "#800080" : "#purple",
                "#808080" : "#grey",
                "#FFA500" : "#orange",
                "#FF69B4" : "#pink",
                "#131391" : "#blue",
                "#FD2525" : "#red",
                "#622525" : "#brown",
                "#403E3E" : "#black",
                "#DC1414" : "red",
                "#FFAA00" : "#orange"

                }


def widthFinder(tempHoldFiles, Space, Font):
    count = 0
    widthArray = []
    widthArray.append(0)
    sumOfWids = 0
    for x in tempHoldFiles:
        if x == " ":
            widthArray.append(Space * 4)
            sumOfWids += Space * 4
        else:
            pdf = PyPDF2.PdfFileReader("bin/CharLibrary/"+Font+"/"+x[:-4] + ".pdf", "rb")
            p = pdf.getPage(0)
            temp = p.mediaBox.getWidth()
            widthArray.append(float(temp))  #* (Scale)
            sumOfWids += float(temp)  + Space #* (Scale)
            print(p.mediaBox.getHeight())
        count += 1
    return sumOfWids - Space





def largestLineFinder(file1, file2, file3, Space, Line1Font, Line2Font, Line3Font):
    file1width = widthFinder(file1,  Space, Line1Font)
    file2width = widthFinder(file2,  Space, Line2Font)
    file3width = widthFinder(file3, Space, Line3Font)
    largestwidth = max(file1width, file2width, file3width)

    return largestwidth



def FindArtboardHeight(Space, Size, numOfLines):





    return (Space * (numOfLines)- (Space -(576*Size)))



def maxHeightFinder(tempHoldFiles, Font):
    count = 0
    height = 0
    for x in tempHoldFiles:
        if x == " ":
            continue
        else:
            pdf = PyPDF2.PdfFileReader("bin/CharLibrary/"+Font+"/" + x[:-4] + ".pdf", "rb")
            p = pdf.getPage(0)
            temp = p.mediaBox.getHeight()
            if temp > height:
                height = temp
        count += 1
    return height


def FileFinder(CurrentLineString, Font):

    FileLocations = []
    CharArray = []
    for x in range(0, len(CurrentLineString)):
        check = False
        for k, v in SymbolConvert.items():
            if CurrentLineString[x] == k:
                CharArray.append(v)
                check = True
                break
        if check == True:
            continue
        if CurrentLineString[x].islower() == True:
            CharArray.append('_'+CurrentLineString[x].lower())
        else:
            CharArray.append(CurrentLineString[x])
        print(CharArray[x])

    for x in range(0, len(CurrentLineString)):
        if CharArray[x] == " ":
            FileLocations.append(" ")
            continue
        check = False
        for root, dirs, files in os.walk("bin/CharLibrary/"+Font+"/"):

            for filename in files:

                if filename == CharArray[x] + ".svg":
                    FileLocations.append(filename)
                    check = True
                    break
        if check == False:
            FileLocations = []
            Error = "ERROR"
            FileLocations.append(Error)
            return FileLocations
    return FileLocations

def numberOfLinesCheck(lineOneCount, lineTwoCount, lineThreeCount):
    numOfLines = 0
    if lineOneCount > 0:
        numOfLines += 1
    if lineTwoCount > 0:
        numOfLines += 1
    if lineThreeCount > 0:
        numOfLines += 1
    return numOfLines

def ColorConverter(HexColor):
    for k, v in ColorHexDic.items():
        if HexColor.upper()  == k:
            return v

    return "Error"


def addFill(FileLoc, FileName, HexColor1, HexColor2, HexColor3, LineOne, LineTwo, LineThree):
    file = open('bin/ConvertedFiles/svgtemp/' + FileName, 'w')
    LineOneCount = len(LineOne.replace(" ", ""))
    LineTwoCount = len(LineTwo.replace(" ", ""))
    LineThreeCount = len(LineThree.replace(" ", ""))

    print("lineonecount: " +str(LineOneCount))

    StylePos = 1
    count = 1
    with open(FileLoc) as f:
        for line in f:
            print(count)
            HexColor = HexColor1
            if count > LineOneCount :
                HexColor = HexColor2
            if count > LineOneCount + LineTwoCount :
                HexColor = HexColor3

            if line[:14] == "      .cls-1 {":
                StylePos += 1
                newLine = "      .cls-"+str(StylePos)+" {"
                file.write(newLine)
                continue

            if line[:22] == '  <path class="cls-1" ':
                newLine = '  <path class="cls-'+str(StylePos)+'" ' + line[22:]
                file.write(newLine)
                continue

            if line[:23] == '    <rect class="cls-1"':
                newLine ='    <rect class="cls-'+str(StylePos)+'"' + line[23:]
                file.write(newLine)
                continue

            if line[:24] == '  <polygon class="cls-1"':
                newLine = '  <polygon class="cls-'+str(StylePos)+'"' + line[24:]
                file.write(newLine)
                continue


            if line[:19] == "        fill: none;":
                # print("found")
                newLine = "        fill: "+HexColor
                file.write(newLine)
                count += 1
                continue
            if line[:24] == "        stroke: #ec008c;":
                continue
            if line[:30] == "        stroke-miterlimit: 10;":
                continue
            if line[:29] == "        stroke-width: 0.25px;":
                continue

            file.write(line)

    file.close()

    SOURCE_DIR = 'bin/ConvertedFiles/svgtemp'
    DEST_DIR = 'bin/ConvertedFiles/SVG'

    for fname in os.listdir(SOURCE_DIR):
        if fname.lower().endswith('.svg'):
            shutil.move(os.path.join(SOURCE_DIR, fname), os.path.join(DEST_DIR, fname))

    for fname in os.listdir(SOURCE_DIR):
        if fname.lower().endswith('.svg'):
            os.remove(os.path.join(SOURCE_DIR, fname))

    return