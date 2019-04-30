from mws import mws
import wget
import zipfile
import os
import json
import base64
import time
import APIConnection
import JsonReader
import csv

def getrowcount():
    row_count = 0
    with open("bin/skuProduction.csv") as f:
        reader = csv.reader(f)

        row_count = sum(1 for row in reader)
        print(row_count)

    return row_count

access_key = 'AKIAI35PBHODQEJBL5RQ' #replace with your access key
seller_id = 'AWTVN3BNE3NEZ' #replace with your seller id
secret_key = 'YYGrr7RZGmQ+ALpbNp80IHRajYmmXF1TL/E051No' #replace with your secret key
marketplace_usa = 'ATVPDKIKX0DER'

orders_api = mws.Orders(access_key, secret_key, seller_id, region='US')
service_status = orders_api.list_orders(marketplaceids=[marketplace_usa], created_after='2017-07-07', orderstatus=('Unshipped', 'PartiallyShipped') )


ordersParsed = service_status.parsed


OrderArray = []
print(ordersParsed)

x = 0




while True:

    try:
        token = ordersParsed['NextToken']['value']
        print(token)
    except:
        token = ''
        print("end")
    while True:

        try:
            if ordersParsed["Orders"]["Order"][x]['AmazonOrderId']["value"]:

                try:
                    temp = ordersParsed["Orders"]["Order"][x]["TFMShipmentStatus"]["value"]


                except:
                    tempOrder = ordersParsed["Orders"]["Order"][x]['AmazonOrderId']["value"]
                    OrderArray.append(tempOrder)


            else:
                break
        except:
            break

        x += 1

    OrderDic ={}

    for i in OrderArray:
        print(i)
        while True:
            try:
                orders = orders_api.list_order_items(i)

                break
            except:
                time.sleep(2)

        ordersParsed = orders.parsed
        print(ordersParsed)

        #print(ordersParsed)
        try:
            url = ordersParsed['OrderItems']['OrderItem']['BuyerCustomizedInfo']['CustomizedURL']['value']
            Sku = ordersParsed['OrderItems']['OrderItem']['SellerSKU']['value']
            print(url)
            print(Sku)
            OrderDic[i] = Sku + " : " + url
        except:
            p=0
            while True:
                try:
                    url = ordersParsed['OrderItems']['OrderItem'][p]['BuyerCustomizedInfo']['CustomizedURL']['value']
                    Sku = ordersParsed['OrderItems']['OrderItem'][p]['SellerSKU']['value']
                    print(Sku)
                    print(url)
                    if p > 0:
                        OrderDic[i] = OrderDic[i] + ", " + Sku + " : " + url
                    else:
                        OrderDic[i] = Sku + " : " + url

                    p += 1
                except:
                    break


    row_counter = getrowcount()
    for k, v in OrderDic.items():
        print(k, v)
        place = 1
        sku = v.split(", ")
        amount = len(sku)
        for skuSplit in range(0, amount):
            SkuName = sku[skuSplit].split(":")
            print("SkuName: " + SkuName[0])
            print("URL: " + SkuName[1])

            for currentRowSku in range(1, row_counter):
                with open("bin/skuProduction.csv") as f:
                    reader = csv.reader(f)
                    # next(reader)  # skip header
                    reader = list(reader)

                    if reader[currentRowSku][0] in SkuName[0]:
                        print(reader[currentRowSku][1])

                        if reader[currentRowSku][1] == "CustomShirt-DTG":
                            APIConnection.DTG(k, SkuName[0], str(SkuName[1].replace(' ', '') + ':' + SkuName[2]), place, amount)
                            place += 1

                        if reader[currentRowSku][1] == "Custom-Vinyl/Cut":
                            JsonReader.JsonRead(k, SkuName[0], str(SkuName[1].replace(' ', '') + ':' + SkuName[2]), place, amount)
                            place += 1



    try:

        service_status = orders_api.list_orders(next_token=token)

        ordersParsed = service_status.parsed
        print(ordersParsed)
        continue
    except:
        break

