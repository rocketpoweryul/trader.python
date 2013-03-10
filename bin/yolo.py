#!/usr/bin/env python
# Created by genBTC 3/9/2013
# Checks market conditions
# Order X amount of BTC between price A and B
# optional Wait time (default to instant gratification)


import args	#lib/args.py modified to use product 1 & bitfloor.json file
import cmd
import time
import functions

#this variable goes into args.py and will pass any API calls defined in the bitfloor.py RAPI
bitfloor = args.get_rapi()

#get the entire Lvl 2 order book    entirebook() was not needed, for the entire book just call book(2)
#whereas book (1) is the last bid/ask
#entirebook = bitfloor.entirebook()    
entirebook = functions.floatify(bitfloor.book(2))

	# old trade function including Chunk Trade spread logic & Confirmation
	# def trade(side, amount, price_lower, price_upper, chunks):
    # loop_price = float(price_lower)
    # for x in range (0, int(chunks)):
        # price_range = float(price_upper) - float(price_lower)
        # price_chunk = float(price_range)/ float(chunks)
        # chunk_amount = float(amount) / float(chunks)
        # print "Chunk # ",x+1," = ",chunk_amount," BTC @ $", loop_price
        # print bitfloor.order_new(side=side, amount=chunk_amount, price=loop_price)
        # loop_price += price_chunk
    # totalprice=0
    # bidcounter=0
    # weightedavgprice=0
    # counter=0
def tradeasks(side,amount,lower,upper,waittime=0):
    totalBTC, totalprice, bidcounter, weightedavgprice, counter = 0
    for askprice in reversed(entirebook['asks'][:10]):
        totalBTC+=askprice[1]
        totalprice+=askprice[0]*askprice[1]
        if totalBTC >= amount:
            totalprice-=askprice[0]*(totalBTC-amount)
            print 'Your ask amount of %r BTC can be serviced by the first %r of orders' % (amount,totalBTC)
            totalBTC=amount
            break
        counter+=1
    weightedavgprice=totalprice/totalBTC
    time.sleep(waittime)
    print '%r BTC @ $%.2f per each BTC is $%.2f' % (totalBTC, weightedavgprice,totalprice)
    
def tradebids(side,amount,lower,upper,waittime=0):
    totalBTC, totalprice, bidcounter, weightedavgprice, counter = 0
    for bidprice in entirebook['bids'][:10]:
        totalBTC+=askprice[1]
        totalprice+=askprice[0]*askprice[1]
        if totalBTC >= amount:
            totalprice-=askprice[0]*(totalBTC-amount)
            print 'Your bid amount of %r BTC can be serviced by the first %r of orders' % (amount,totalBTC)
            totalBTC=amount
            break
        counter+=1
    weightedavgprice=totalprice/totalBTC
    time.sleep(waittime)
    print '%r BTC @ $%.2f per each BTC is $%.2f' % (totalBTC, weightedavgprice,totalprice)

#some ideas
# if trying to buy start from lowerprice, check ask order book, buy if an order on order book is lower than lowerprice
#mtgox is @ 47.5 , you want to buy @ 47-46, you say "Buy 47" 
# NOT COMPLETE> SOMETHING IS TOTALLY WRONG WITH THIS FILE YOU CAUGHT ME IN THE MIDDLE OF IT
#if trying to sell start from higherprice, put higherprice on orderbook regardless, 

def addupasks(side,amount,lower,upper,waittime=0):
    totalBTC=0
    totalprice=0
    bidcounter=0
    weightedavgprice=0
    counter=0
    for askprice in reversed(entirebook['asks'][:10]):
        totalprice+=float(askprice[0])*float(askprice[1])
        totalBTC+=float(askprice[1])
        weightedavgprice=totalprice/totalBTC
        counter+=1
    time.sleep(float(waittime))
    print '$', totalprice, totalBTC, ' BTC', weightedavgprice, ' for ASKS'


class Shell(cmd.Cmd):
    def emptyline(self):
        pass

	#start printing first 10 asks and 10 bids of the order book
    for askprice in reversed(entirebook['asks'][:10]):
        print ' '*30,'$%.2f, %.5f --ASK-->' % (askprice[0],askprice[1])
    print ' '*20,'|'*11
    for bidprice in entirebook['bids'][:10]:
        print '<--BID--$%.2f, %.5f' % (bidprice[0],bidprice[1])
    
#give a little user interface
    print 'Press Ctrl+Z to exit gracefully or  Ctrl+C to force quit'
    print ' '
    prompt = '(buy|sell, amount, lower, upper, wait) '

	#pass arguments back up to trade() function
    def do_sell(self, arg):
        try:
            amount, lower, upper, wait = arg.split()
            amount = float(amount)
            lower = float(lower)
            upper = float(upper)
            wait = float(wait)
        except:
            print "Invalid arg {1}, expected amount price".format(side, arg)        
        #trade(1, amount, lower, upper, wait)
        tradeasks(1,amount,lower,upper,wait)
    def do_buy(self, arg):
        try:
            amount, lower, upper, wait = arg.split()
        except:
            print "Invalid arg {1}, expected amount price".format(side, arg)        
        #trade(0, amount, lower, upper, wait)
        tradebids(0,amount,lower,upper,wait)

#exit out if Ctrl+Z is pressed
    def do_EOF(self, arg):
        print "Any Trades have been Executed, Session Terminating......."
        return True

Shell().cmdloop()
