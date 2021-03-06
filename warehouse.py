"""Module for displaying warehouse stock and demand"""

import pygame
import random

# Increase the demand
def increaseDemand(gameData):
    demand_keys = [key for key in gameData.keys() if 'demand' in key]

    for i in demand_keys:
        demand = i
        item = i.split(" ")[0]
        price = gameData[item + ' price']
        #newDemandPercentage = 1 + (random.randrange(1,100)/100)
        newDemandPercentage = random.randrange(20, 200)

        # We want the demand of pricy items to be lower
        if price > 25:
            newDemandPercentage /= 2
        if price > 250:
            newDemandPercentage /= 4
        # Increase the demand
        if gameData[demand] < 1:
            gameData[demand] += 1
        #newFloat = gameData[demand] * newDemandPercentage
        #print(i, newDemandPercentage)
        newFloat = gameData[demand] + newDemandPercentage
    
        newInt = round(newFloat)
        gameData[demand] = newInt
      
        

# Check if stock is equal to demand
def checkWarehouse(gameData):
    stock_keys = [key for key in gameData.keys() if 'stock' in key]
    demand_keys = [key for key in gameData.keys() if 'demand' in key]

    # Iterate through the demand and stock and evaluate
    for i in stock_keys:    # Get the item name
        item = i.split(" ")[0]

        # If there is a demand and item is in stock
        if gameData[item + " demand"] > 0 and gameData[item + " stock"] > 0:

            # Increase income, subtract items sold from demand and stock
            demand = gameData[item + ' demand'] 
            stock = gameData[item + ' stock']
            stock = int(stock * (gameData["renown"] / 100))
            quantitySold = 0

            if demand >= stock:
                quantitySold = stock
            elif demand < stock:
                quantitySold = demand

            quantitySold = int(quantitySold * (gameData["renown"] / 200))

            gameData['cash'] += quantitySold * gameData[item + " price"]
            gameData[item + ' demand'] -= quantitySold
            gameData[item + " stock"] -= quantitySold




