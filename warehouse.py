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
        newDemandPercentage = 1 + (random.randrange(1,100)/100)
        
        # We want the demand of pricy items to be lower
        if price > 25:
            newDemandPercentage /= 2
        # Increase the demand
        newFloat = gameData[demand] * newDemandPercentage
        newInt = round(newFloat)
        gameData[demand] += newInt
        
        


        


# Check if stock is equal to demand
def checkWarehouse(gameData):
    stock_keys = [key for key in gameData.keys() if 'stock' in key]
    demand_keys = [key for key in gameData.keys() if 'demand' in key]
    
    # Iterate through the demand and stock and evaluate
    for i in stock_keys:    # Get the item name
        item = i.split(" ")[0]

                            # If the demand is equal to or less than the stock
        if gameData[item + " stock"] >= gameData[item + " demand"]:
            # Sell merchandise
            gameData['cash'] += (gameData[item + " stock"]*gameData[item + " price"])
            gameData[item + ' demand'] -= gameData[item + ' demand']
            gameData[item + " stock"] -= gameData[item + ' demand']




