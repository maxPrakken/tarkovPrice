#https://tarkov-market.com/dev/api
import os
import sys
import subprocess
import time

apikey = open("apikey.txt", "r").read()

while True:
    try:
        item = input('Search for: \n')
        
        #gets item description from tarkov-market by argument
        command = 'curl -H x-api-key:' + apikey + ' https://tarkov-market.com/api/v1/item?q=' + item#sys.argv[1]
        print(command)
        #captures output into res and converts to str due to text=true
        res = subprocess.run(command, capture_output=True, text=True)

        if(res is not None):
            #base indexes
            basefirst = res.stdout.index("basePrice")
            basesecond = res.stdout.find(',', basefirst)

            pricefirst = res.stdout.index("price")
            pricesecond = res.stdout.find(',', pricefirst)

            traderfirst = res.stdout.index("traderPrice")
            tradersecond = res.stdout.find(',', traderfirst)

            namefirst = res.stdout.index("name")
            namesecond = res.stdout.find(',', namefirst)

            print('\n' + res.stdout[namefirst:namesecond])
            print(res.stdout[basefirst:basesecond])
            print(res.stdout[pricefirst:pricesecond])
            print(res.stdout[traderfirst:tradersecond])
            print('\n========================================\n')

        else:
            print('===BAD REQUEST===')
    except:
        print('===BAD INPUT===')
    
    

