import random

done = False
startGame = True

while not done:

    while startGame:
        print 'Welcome to HiroChase!\n'
        print 'You did not do your homework and have to make your way to your car.'
        print 'Your teacher wants to confront you and is chasing down, but you\'re wearing new kicks! Survive the school day and outrun your teacher.'

        metersTraveled = 0
        thirst = 0
        footTiredness = 0
        drinksLeft = 3
        teacherMeters = -20

        win = False
        quitted = False
        startGame = False

    print "\nWhat will you do?\n"
    print "A. Drink a Red Bull."
    print "B. Flee at a speed-walk."
    print "C. Flee at a run."
    print "D. Stop and massage your feet."
    print "E. Status check"
    print "Q. Quit."

    dist = 0

    userInput = raw_input("\nType A, B, C, D, E, or Q: ")
    print

    if userInput.upper() == "Q":
        done = True
        quitted = True
    elif userInput.upper() == "E":
        print "Meters traveled:  ", metersTraveled
        print "Red Bulls in Bag:  ", drinksLeft
        print "Your teacher is ", metersTraveled - teacherMeters, " meters away."
    elif userInput.upper() == "D":
        footTiredness = 0
        print "Your feet have been soothed."
        teacherMeters += random.randint(7, 15)
    elif userInput.upper() == "C":
        dist = random.randint(10, 20)
        metersTraveled += dist
        print "You ran ", dist, " meters."
        thirst += 1
        footTiredness += random.randint(1, 3)
        teacherMeters += random.randint(7, 14)
    elif userInput.upper() == "B":
        dist = random.randint(5, 12)
        metersTraveled += dist
        print "You speed-walked ", dist, " meters."
        thirst += 1
        footTiredness += 1
        teacherMeters += random.randint(7, 14)
    elif userInput.upper() == "A":
        if drinksLeft > 0:
            drinksLeft -= 1
            thirst = 0
            print "You quenched your thirst. Good job."
            teacherMeters += random.randint(7, 14)
        else:
            print "Oh shit! You have no Red Bull left!"

    if random.randint(1,20) == 1:
        print "But what luck! You found a lunchbox full of goodies and are renourished."
        thirst = 0
        footTiredness = 0
        drinksLeft += 3

    if thirst > 4 and thirst <= 6:
        print "You\'re getting thirsty."
    elif thirst > 6:
        print "You got dehyrated and cannot continue."
        done = True

    if footTiredness > 5 and footTiredness <= 8 and not done:
        print "Your feet are getting tired."
    elif footTiredness > 8 and not done:
        print "Your feet hurt too much and you cannot continue."
        done = True

    if teacherMeters >= metersTraveled - 15 and teacherMeters < metersTraveled and not done:
        print "Your teacher is getting close!"
    elif teacherMeters >= metersTraveled and not done:
        print "Your teacher has caught you!"
        done = True

    if metersTraveled >= 200 and not done:
        print "You made it to your car and escaped the wrath of you teacher! Great work, kid!"
        done = True
        win = True

    if done and not quitted:
        if win == False:
            print "\nYou ded, brudda."
        if raw_input("Play again? (Type 'yes' or 'no') ").upper() == "YES":
            done = False
            startGame = True
            print "\n"
        else:
            quitted = True


    if quitted:
        print "\nSeeya later, kiddo!"



