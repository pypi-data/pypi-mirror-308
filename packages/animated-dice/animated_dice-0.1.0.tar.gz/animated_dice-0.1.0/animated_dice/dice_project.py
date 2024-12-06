
#dice roller logan maguire

print ("testing can you read this?")
import random #this is the recommended library for any and all random related stuff and it is recommended that you don't recode work
amount_of_dice =0 #the amount of dice requested to be rolled
i=0 #so that the while loops can do the required amounts of loops
dice_applier =[]
while amount_of_dice<10:
    number = random.randint(1, 10)
    dice_applier.append(number)
print(f"{dice_applier}")