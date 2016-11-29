#Pandas the introduction working with data. 

Solutions 

import csv

world_alcohol = []
with open('world_alcohol.csv', 'r') as file: 
    data = csv.reader(file, delimiter=',')
    for row in data: 
        world_alcohol.append(row)
        
years = []
total = 0    
for row in world_alcohol: 
    year = row[0]
    try: 
        total += float(year)
        years.append(year)
    except (ValueError): 
        pass

avg_year = total/len(years)

# Numpy 
# basically does import the data and stores it in array 
import numpy as np 
world_alcohol = n.genfromtxt("world_alcohol.csv", delimiter=",")

creating arrays 
vector = numpy.array([10, 20, 30])
matrix = numpy.array([[5, 10, 15], [20, 25, 30], [35, 40, 45]])

numpy.array can convert list and lists of lists into either vectors or matrices. 
matrix is a n dimentional array 
vector is one dimentional array 

