import wget
import zipfile
import os
import json
import VinylCut
import time




def JsonRead(ordernum, sku, url, place, amount):

    Size = "--EMPTY--"
    Pattern = "--EMPTY--"
    Line1Font = "--EMPTY--"
    Line1Color = "--EMPTY--"
    Line1Text = "--EMPTY--"
    Line2Font = "--EMPTY--"
    Line2Color = "--EMPTY--"
    Line2Text = "--EMPTY--"
    Line3Font = "--EMPTY--"
    Line3Color = "--EMPTY--"
    Line3Text = "--EMPTY--"
    LineFont = "--EMPTY--"
    LineColor = "--EMPTY--"
    LineText = "--EMPTY--"

    while True:

        try:
            wget.download(url, 'C:/Users/kjoos/PycharmProjects/AmazonAPI/' + ordernum + '.zip')
            break

        except:
            time.sleep(2)






    zip_ref = zipfile.ZipFile('C:/Users/kjoos/PycharmProjects/AmazonAPI/'+ ordernum + '.zip', 'r')
    zip_ref.extractall('C:/Users/kjoos/PycharmProjects/AmazonAPI/ExtractedVinylCut')
    zip_ref.close()



    path = 'C:/Users/kjoos/PycharmProjects/AmazonAPI/ExtractedVinylCut/'

    for filename in os.listdir(path):

        with open(path+filename) as json_file:
            data = json.load(json_file)
            print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            print(data['customizationInfo'])


            try:
                Line1Font = data['customizationInfo']['aspects'][0]['font']['value']
                Line1Color = data['customizationInfo']['aspects'][0]['color']['value']
                Line1Text = data['customizationInfo']['aspects'][0]['text']['value']

            except:
                Line1Font = "--EMPTY--"
                Line1Color = "--EMPTY--"
                Line1Text = "--EMPTY--"


            try:
                Line2Font = data['customizationInfo']['aspects'][1]['font']['value']
                Line2Color = data['customizationInfo']['aspects'][1]['color']['value']
                Line2Text = data['customizationInfo']['aspects'][1]['text']['value']
            except:
                Line2Font = "--EMPTY--"
                Line2Color = "--EMPTY--"
                Line2Text = "--EMPTY--"

            try:
                Line3Font = data['customizationInfo']['aspects'][2]['font']['value']
                Line3Color = data['customizationInfo']['aspects'][2]['color']['value']
                Line3Text = data['customizationInfo']['aspects'][2]['text']['value']

            except:
                Line3Font = "--EMPTY--"
                Line3Color = "--EMPTY--"
                Line3Text = "--EMPTY--"






            print(Line1Font)
            print(Line2Font)
            print(Line3Font)
            print(Line1Color)
            print(Line2Color)
            print(Line3Color)
            print(Line1Text)
            print(Line2Text)
            print(Line3Text)
            VinylCut.mainCode(ordernum, sku, Line1Text, Line1Font, Line1Color, Line2Text, Line2Font, Line2Color, Line3Text, Line3Font, Line3Color, place, amount)


            LineFont = data['customizationInfo']
            LineColor = data['customizationInfo']
            LineText = data['customizationInfo']

    dir_name = "ExtractedVinylCut/"
    test = os.listdir(dir_name)

    for item in test:
        os.remove(os.path.join(dir_name, item))
    for file in os.listdir("C:/Users/kjoos/PycharmProjects/AmazonAPI"):
        if file.endswith(".zip"):
            os.remove(os.path.join("C:/Users/kjoos/PycharmProjects/AmazonAPI", file))

    return
