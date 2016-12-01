import random

print 'Welcome to HiroChase!'
print 'You did not do your homework and have to make your way to your car.'
print 'Your teacher wants to confront you and is chasing down, but you\'re wearing new kicks! Survive the school day and outrun your teacher.'

done = False

while not done:
    print "A. Drink a Red Bull."
    print "B. Flee at a speed-walk."
    print "C. Flee at a run."
    print "D. Stop and massage your feet."
    print "E. Status check"
    print "Q. Quit."

    metersTraveled = 0
    thirst = 0
    footTiredness = 0
    drinksLeft = 3
    teacherMeters = -20
    dist = 0

    userInput = raw_input("What will you do?: ")

    if userInput.upper() == "Q":
        done = True
    elif userInput.upper() == "E":
        print "Meters traveled:  " + metersTraveled
        print "Red Bulls in Bag:  " + drinksLeft
        print "Your teacher is " + (metersTraveled - teacherMeters) + " meters away."
    elif userInput.upper() == "D":
        footTiredness = 0
        print "Your feet have been soothed."
        teacherMeters += random.randint(7, 15)
    elif userInput.upper() == "C":
        dist = random.randint(10, 21)
        metersTraveled += dist
        print "You ran " + dist + " meters."
        thirst += 1
        footTiredness += random.randint(1, 4)
        teacherMeters += random.randint(7, 15)
    elif userInput.upper() == "B":
        dist = random.randint(5, 13)
        metersTraveled += dist
        print "You speed-walked " + dist + " meters."
        thirst += 1
        footTiredness += 1
        teacherMeters += random.randint(7, 15)
    elif userInput.upper() == "A":
        if drinksLeft > 0:
            drinksLeft -= 1
            thirst = 0
            print "You quenched your thirst. Good job."
            teacherMeters += random.randint(7, 15)
        else:
            print "Oh shit! You have no Red Bull left!"

    if thirst > 4 and thirst <= 6:
        "You\'re getting thirsty."
    elif thirst > 6:
        "You got dehyrated and cannot continue."
        done = True

    if footTiredness > 5 and footTiredness <= 8:
        "Your feet are getting tired."
    elif footTiredness > 8:
        "Your feet broke off and you cannot continue."
        done = True
