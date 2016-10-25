# main code for the bike market

# model = ["women","men","kids","road","mountain","hybrid"]
# weight = [50,50,30,30,50,60]
# cost = [100,100,70,300,250,150]

import bike_market

bike1 = bike_market.Bicycle("women", 50, 100)
bike2 = bike_market.Bicycle("men", 50, 100)
Shop1 = bike_market.Bike_shop("OntheRoad",[bike1,bike2],20)
Costumer1 = bike_market.Costumer("Bob",125)

print(Costumer1.canBuy(Shop1,bike1))