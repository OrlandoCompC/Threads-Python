"""
Name: Orlando
date: 04/15/2023

This program is an animal zoo where each time an anime gets hungry, it will eat the food that is available.
If the food is not available, it will wait until the food is available.
It will use threads to simulate the animals eating the food.
It will also use threads to increase the amount of food available until an animal can eat it.
It will also use classes to create the animals.

There is a function called slowPrint which prints the text slowly.
I use ansi escape sequences to color the text, this way its easier to read the output.

Imports are: threading, random, time

threading is used to create the threads
random is used to generate random numbers
time is used to make the program sleep for a certain amount of time
"""

import threading
import random
import time

lock_food=threading.Lock() #This will be used to lock the food stock
food_stock=0 # This is the global food stock 
total_food_eaten=0 #This is the amount of food eaten by all animals

#this function will be used to get the number of animals to feed
while (True):
    try:
        animals_to_feed= lambda num=int(input("Enter number of animals to be fed: ")): num 
        if (animals_to_feed()<=0):
            raise Exception("Please enter a positive integer")
        #The following is to document the lambda function
        animals_to_feed.__doc__= """
        Name:
        -----
            animals_to_feed

        Description:
        ------------
            This is a lambda function that will be used to get the number of animals to feed.
            This function gets the number of animals to feed from the user then stores it in a variable called num and returns it.
            This number must be a positive integer.

        Returns
        -------
        num : int 
            The number of animals to feed.

        Raises
        ------
            Exception: An error occurs when the user enters a negative number or a non-integer.
            It also when a user enters a number that is not a positive integer.
        """
        num_to_feed=animals_to_feed()
        break
    except Exception as e:
        print("Please enter a positive integer")
        continue



class Animal(): #this is the animal class
    """
    Description:
    ------------
        This class will be used to create the animals. It will have the following

    Attributes:
    -----------
        name : str
            The name of the animal.
        food_amount : int
            The amount of food needed by the animal.
        times_hungry : int
            The number of times the animal is hungry.
        times_fed : int
            The number of times the animal is fed.
        total_food_consumed : int
            The total amount of food consumed by the animal.

    Methods:
    --------
        times_animal_hungry()
            This will increase with the number of times the animal is hungry.
        times_animal_fed()
            This will increase with the number of times the animal is fed.
        increase_food_consumed()
            This will increase with the amount of food consumed by the animal.
        getName()
            This will return the name of the animal.
        getFoodAmount()
            This will return the amount of food needed by the animal.
        getTimesHungry()
            This will return the number of times the animal is hungry.
        getTimesFed()
            This will return the number of times the animal is fed.
        getTotalFoodConsumed()
            This will return the total amount of food consumed by the animal.
    """

    def __init__(self,name:str,food_amount:int)->None:
        """
        Description:
        ------------
            This is the constructor for the Animal class.
            Initializes an Animal object with the specified name and food amount.

        Parameters:
        ----------
        name : str
            The name of the animal.
        food_amount : int
            The amount of food needed by the animal
        """

        self.name=name
        self.food_amount=food_amount
        self.times_hungry=0
        self.times_fed=0
        self.total_food_consumed=0


    def times_animal_hungry(self)->None: #this will increase the number of times the animal is hungry
        """
        Name:
        -----
            times_animal_hungry

        Description:
        ------------
            This method will increase the number  each time the animal is hungry.
        """
        self.times_hungry+=1

    def times_animal_fed(self)->None: #this will increase the number of times the animal is fed
        """
        Name:
        -----
            times_animal_fed

        Description:
        ------------
            This method will increase the number of times the animal is fed.
        """
        self.times_fed+=1

    def increase_food_consumed(self)->None: #this will increase the amount of food consumed by the animal
        """
        Name:
        -----
            increase_food_consumed

        Description:
        ------------
            This method will increase the amount of food consumed by the animal.
        """
        self.total_food_consumed+=self.food_amount

    #getters
    def getName(self)->str: #this will return the name of the animal
        """
        Name:
        -----
            getName

        Description:
        ------------
            This method will return the name of the animal.

        Returns:
        -------
            str: The name of the animal.
        """
        return self.name
    
    def getFoodAmount(self)->int: #this will return the amount of food needed by the animal
        """
        Name:
        -----
            getFoodAmount

        Description:
        ------------
            This method will return the amount of food needed by the animal.

        Returns:
        -------
            int: The amount of food needed by the animal.
        """
        return self.food_amount
    
    def getTimesHungry(self)->int: #this will return the number of times the animal is hungry
        """
        Name:
        -----
            getTimesHungry 

        Description:
        ------------
            This method will return the number of times the animal is hungry.

        Returns:
        -------
            int: Number of times the animal is hungry.
        """
        return self.times_hungry
    
    def getTimesFed(self)->int: #this will return the number of times the animal is fed
        """
        Name:
        -----
            getTimesFed

        Description:
        ------------
            This method will return the number of times the animal is fed.

        Returns:
        -------
            int: A counter with the number of times the animal is fed. 
        """
        return self.times_fed
    
    def getFoodConsumed(self)->int: #this will return the total amount of food consumed by the animal
        """
        Name:
        -----
            getFoodConsumed

        Description:
        ------------
            This method will return the total amount of food consumed by the animal.

        Returns:
        -------
            int: A counter with the total amount of food consumed by the animal.
        """
        return self.total_food_consumed
    

def animal_list_Orlando()->list:#instantiating the animals
    """
    Name:
    -----
        animal_list_Orlando

    Description:
    ------------
        This method instatiates the animals and returns a list with the animals.

    Returns:
    -------
        list: A list with the animals objects to be able to use by other functions.
    """
    
    elephant=Animal("Elephant",15)
    giraffe=Animal("Giraffe",9)
    horse=Animal("Horse",5)
    zebra=Animal("Zebra",5)
    deer=Animal("Deer",3)
    return [elephant,giraffe,horse,zebra,deer]

def feed_animals(zoo_cond:threading.Condition)->None: #Feeding task
    """
    Name:
    -----
        feed_animals

    Description:
    ------------
        This method feeds the animals and prints the information of the animal that is being fed.
        If the animal doesnt have enough food it will wait until the food is available.

    Parameters:
    ----------
        zoo_cond : threading.Condition
        The condition variable that will be used to synchronize the threads.    

    Returns:
    -------
        None: This method does not return anything.
    """
    global food_stock
    global total_food_eaten
    global num_to_feed
    global animals
    animals=animal_list_Orlando()
    while(num_to_feed>0):
        random_animal=random.choice(animals) # will choose one of the animals randomly
        # print(f'\033[1;34m{random_animal.getName()} is hungry\033[0;0m')
        time.sleep(0.3)
        with zoo_cond:
            while(food_stock<random_animal.getFoodAmount()):
                    print(f'\033[1;34mWAIT FOR FOOD: {random_animal.getName()} Is Hungry and Patiently Waiting For Food To Be Available\033[0;0m')
                    random_animal.times_animal_hungry() #increases the number of times the animal is hungry
                    zoo_cond.wait() #waits until the food is available
            lock_food.acquire()        
            food_stock-=random_animal.getFoodAmount()
            lock_food.release()
            total_food_eaten+=random_animal.getFoodAmount()
            random_animal.times_animal_fed() #increases the number of times the animal is fed
            random_animal.increase_food_consumed()
            print(f'\033[33m{random_animal.getName()} got fed {random_animal.getFoodAmount()} kg----> Food Stock: {food_stock} kg\033[0m')
            print(f'\033[1;32m{random_animal.getName()} feed Count: {random_animal.getTimesFed()}\033[0;0m')
            random_animal.times_animal_hungry() #increases the number of times the animal is hungry
            num_to_feed-=1

        

def food_deposited(zoo_cond:threading.Condition)->None: # Depositing Task
    """
    Name:
    -----
        food_deposited

    Description:
    ------------
        If the food stock is less than needed then this function adds food to the food stock.
        This function adds food to the food stock and prints the information of the food that is being added.

    Parameters:
    ----------
        zoo_cond : threading.Condition
        The condition variable that will be used to synchronize the threads.       

    Returns:
    -------
        None: This method does not return anything.
    """
    global food_stock
    global num_to_feed
    while(num_to_feed>0):
        time.sleep(0.4)
        with zoo_cond:
            #There is 0 food amount at the start
            amount=random.randint(1,10) #food amount is random
            lock_food.acquire()
            food_stock+=amount
            lock_food.release()
            print(f'\t\tAdd food: {amount}----> Food Stock: {food_stock}')
            zoo_cond.notify_all() #sends the signal to all waiting threads


def hungriest_Orlando()->None: #this function prints the hungriest of all the animals
    """
    Name:
    -----
        hungriest_Orlando

    Description:
    ------------
        This function prints the animal that is the hungriest.
        This function also prints the number of times the animal is hungry and the number of times the animal is fed.
    """

    animalDict={}
    for animal in animals:
        print(f'\033[1;34m{animal.getName()}\033[0m got hungry {animal.getTimesHungry()} time(s), fed {animal.getTimesFed()} time(s) and consumed {animal.total_food_consumed} kg of food')
        print("==================================================================")
        animalDict[animal.getName()]=animal.getTimesHungry()
    for k,v in animalDict.items():
        if v==max(animalDict.values()):
            print(f'\033[1;34m{k}\033[0m Is The Hungriest Animal\n==================================================================')


def consumed_most_food_Orlando()->None: #this function prints the animal that consumed the most amount of food
    """
    Name:
    -----
        consumed_most_food_Orlando

    Description:
    ------------
        This function prints the animal that consumed the most amount of food.
        This function also prints the total amount of food consumed by all the animals.
    """
    animalDict={}
    for animal in animals:
        animalDict[animal.getName()]=animal.getFoodConsumed()
        
    for k,v in animalDict.items():
        if v==max(animalDict.values()):
            print(f'\033[1;34m{k}\033[0m Consumed The Most Amount Of Food\n==================================================================')

    print("The Total Amount Of Food Consumed By All Animals Is: ",total_food_eaten,"kg")

def slowPrint(string_word:str)->None:
    """
    Name:
    -----
        slowPrint

    Description:
    ------------
        This function prints the string character by character with a delay of 0.01 seconds.
        The string that will be printed character by character.
        
    Parameters:
    ----------
        string_word : str 
    """
    for letter in string_word :
        print(letter, end='', flush=True)
        time.sleep(0.01)


if __name__=="__main__":# This is the main function/ main thread of the program
    condition=threading.Condition() #this is the condition that will be used to wait and notify
    fanimals=threading.Thread(name='feed-animals',target=feed_animals,args=(condition,))
    fDeposit=threading.Thread(name='food-deposit',target=food_deposited,args=(condition,))
    slowPrint("\033[1;44m%%%%%%%%%%%%%%%%%%%%% FEEDING BEGINS %%%%%%%%%%%%%%%%%%%%%\033[0;0m\n")
    slowPrint("ZOO ANIMAL FEEDING SYSTEM\n")
    slowPrint("DEVELOPED BY: ORLANDO COMPANIONI\n")
    slowPrint('STUDENT#: 991437087\n')
    slowPrint("===========================================================\n")

    #starting the threads
    fanimals.start()
    fDeposit.start()

    #joining the threads
    fanimals.join()
    fDeposit.join()
    slowPrint("\033[1;44m%%%%%%%%%%%%%%%%%%%%% ANIMAL FEEDING SUMMARY %%%%%%%%%%%%%%%%%%%%%\033[0;0m\n")
    hungriest_Orlando()
    consumed_most_food_Orlando()


#All the documentation for the functions and classes printed
    slowPrint(f'\033[33m%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% DOCUMENTATION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(f"\nAnimal Class: {Animal.__doc__}")
    print(Animal.getName.__doc__)
    print(Animal.getFoodAmount.__doc__)
    print(Animal.getTimesHungry.__doc__)
    print(Animal.getTimesFed.__doc__)
    print(Animal.getFoodConsumed.__doc__)
    print(Animal.times_animal_hungry.__doc__)
    print(Animal.times_animal_fed.__doc__)
    print(Animal.increase_food_consumed.__doc__)
    print(feed_animals.__doc__)
    print(food_deposited.__doc__)
    print(hungriest_Orlando.__doc__)
    print(consumed_most_food_Orlando.__doc__)
    print(slowPrint.__doc__)
    print('-----------------------------------------------------------------------------')
    print(animals_to_feed.__doc__)
