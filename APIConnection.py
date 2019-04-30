from mws import mws
import wget
import zipfile
import os
import json
import base64
import time

FileType = {".jpg" : "jpeg" , ".png" : "PNG" , ".jpeg" : "jpeg" }



def DTG(ordernum, sku, url, place, amount):

    multiorder = ''
    if amount == 1:
        place = ''
        amount = ''
    else:
        multiorder = '_Design(' + str(place) + "OF" + str(amount) + ')'


    print(url)

    while True:

        try:
            wget.download(url, 'C:/Users/kjoos/PycharmProjects/AmazonAPI/' + ordernum + '.zip')
            break
        except:
            time.sleep(2)

    zip_ref = zipfile.ZipFile('C:/Users/kjoos/PycharmProjects/AmazonAPI/' + ordernum + '.zip', 'r')
    zip_ref.extractall('C:/Users/kjoos/PycharmProjects/AmazonAPI/ExtractedDTG')
    zip_ref.close()

    SVGFile = ''
    jsonFile = ''
    ArtFile = ''
    for file in os.listdir("ExtractedDTG/"):
        if file.endswith(".svg"):
            print(os.path.join("ExtractedDTG/", file))
            SVGFile = file

        elif file.endswith(".json"):
            jsonFile = file

        else:

            ArtFile = file


    print(SVGFile)
    print(jsonFile)
    print(ArtFile)

    try:
        FileExten = ArtFile[ArtFile.index("."):]
        print(FileExten)
        FileExtenConvert = FileType[FileExten]
        print(FileExtenConvert)
        base64String = ''
        with open("ExtractedDTG/" + ArtFile, "rb") as imageFile:
            base64String = base64.b64encode(imageFile.read())

        file = open('ConvertedFile/SVG/' + ordernum + '_' + sku.replace(' ', '') +  multiorder + '.svg', 'w')


        with open("ExtractedDTG/" + SVGFile) as imageFile:
                for line in imageFile:
                    print(line)
                    temp = line[0:18]
                    tempsize = line[0:19]
                    print("tempsize = " + tempsize)
                    if tempsize == "<?xml version='1.0'":

                        firstline = '<?xml version = "1.0" encoding = "UTF-8" standalone="no"?> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width ="1008" height="1152" viewBox= "977 594 1227.744 1403.136" xml:space="preserve">'

                        file.write(firstline)
                        continue

                    if temp == "<image xlink:href=":

                        indexspot = line.index(" x=")
                        print(indexspot)
                        newstring = line[0:18] + "'data:image/" + FileExtenConvert  + ";base64, " + str(base64String)[2:-1] + "'" + line[indexspot:]
                        file.write(newstring)
                        continue

                    file.write(line)

        file.close()

    except:
        file = open('ConvertedFile/SVG/' + ordernum + '_' + sku.replace(' ', '') +  multiorder + '.svg', 'w')
        with open("ExtractedDTG/" + SVGFile) as imageFile:
            for line in imageFile:
                print(line)
                temp = line[0:18]
                tempsize = line[0:19]
                print("tempsize = " + tempsize)
                if tempsize == "<?xml version='1.0'":
                    firstline = '<?xml version = "1.0" encoding = "UTF-8" standalone="no"?> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width ="1008" height="1152" viewBox= "977 594 1227.744 1403.136" xml:space="preserve">'

                    file.write(firstline)
                    continue


                file.write(line)

        file.close()


    dir_name = "ExtractedDTG/"
    test = os.listdir(dir_name)

    for item in test:

        os.remove(os.path.join(dir_name, item))

    for file in os.listdir("C:/Users/kjoos/PycharmProjects/AmazonAPI"):
        if file.endswith(".zip"):

            os.remove(os.path.join("C:/Users/kjoos/PycharmProjects/AmazonAPI", file))


    return
'''
import subprocess

script = '"C:\Program Files\Adobe\Adobe Illustrator CC 2019\Presets\en_US\Scripts\PNGsaveDTG.jsx"'
adobePath = r'"C:/Program Files/Adobe/Adobe Illustrator CC 2019/Support Files/Contents/Windows/Illustrator.exe"'
subprocess.Popen("%s %s" % (adobePath, script))
'''


