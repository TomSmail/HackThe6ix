from microbit import pin0, sleep, display
import radio #Allows microbits to communicate

RATE = 20
pin0.set_analog_period(RATE)
display.scroll('Hello, World!')  

def setAngle(angle,pin):
    """Set the servo to a particular angle from -90 to +90 degrees"""
    if (angle > 90 or angle < -90):
        return False
        
    duty_time = angle/180 + 1.5 #1 ms = -90 degrees; 2ms = +90 degrees
    pin.write_analog(duty_time*1000/RATE) # convert using the set rate
    
    return True

def spoofLocation():
    lat = 56.1304
    lon = -106.3468
    STEP_Lat = 0.01
    STEP_Lon = -0.01
    
    while True:
        yield(lat,lon)
        lat += STEP_Lat
        lon += STEP_Lon


# send 



# radio.config(group=2,queue=1) #group = channel; queue=1 ensures that the microbits only store a backlog of 1 message rather than storing loads, meaning they can't get clogged up. The microbits are always listening even when doing something else and messages are added to a queue. Here we cap the queue at size 1 message
# radio.on() #radio communication is off by default to save power so we need to activate it.

# while True: 
    
#     thisPlayer = random.choice(["top","btm"]) # Randomly decide whether to be the top player or the bottom player. We use btm so that the two are the same length so that when we display on screen "you are the btm player" it doesn't take any longer than to say "you are the top player". If it did the microbits would get out of sync and the game would break.
#     radio.send("play"+thisPlayer)#Tell all microbits on this channel you want to play and you want to be top/bottom
#     message = radio.receive()#Receive a message from the queue - this will be from the other microbit telling you which player it wants to be
#     radio.receive() #consume any extra messages that might be clogging up the queue.
#     if message and (message[:4] == "play" and message[4:] != thisPlayer): #If the message we got was a message saying to start playing and the other microbit wants to be a different player to us then this will work. Otherwise we have to keep trying until both microbits have a different choice of player (by continuing to iterate)
#         otherPlayer = message[4:] #Save what player the other player wanted to be
#         display.scroll("You are " + thisPlayer + " player. 5 pts to win") #tell the user which player they are
 
#         frameCount = 0 #This will count how many frames of the game have elapsed so that we can only move the ball every n frames otherwise the ball moves too fast.
#         ballVelocity = [-1,-1]#Always 1 or -1 in each of y then x (sorry), starting from top left (again sorry)
#         while not(topScore == 5 or bottomScore == 5): #While neither player has won
#             if thisPlayer == "top": #If you are the top player
#                 if button_b.is_pressed(): #if you pressed the b button
#                     topPos += 1 #the top player moves one space to the right
#                     radio.send("moveRight") #tell the other microbit you moved right (mbs can't pick up their own messages so if we use the same message name moveRight for top and bottom that will be fine)
#                 elif button_a.is_pressed(): #if you are the pressed the a button
#                     topPos -= 1 #the top player moves one space to the left
#                     radio.send("moveLeft") #tell the other microbit you moved left
#                 msg = radio.receive()#Now we need to check if the other player has moved
#                 if msg == "moveRight": #If they moved right
#                     bottomPos += 1 #The bottom player moved right since we are the top player
#                 elif msg == "moveLeft": #if they moved left
#                     bottomPos -= 1 # the mbottom player moved left since we are the top player
                        
#             elif thisPlayer == "btm": #if we are the bottom player
#                 if button_b.is_pressed(): #if the b button was pressed we move right and tell the other player we did so
#                     bottomPos += 1
#                     radio.send("moveRight")
#                 elif button_a.is_pressed(): #If the a button was pressed we move left and tell the other player
#                     bottomPos -= 1
#                     radio.send("moveLeft")
#                 msg = radio.receive() #Receive any messages that might have been sent to tell us the other player has also moved. Pro note: Unlike in functional programming the radio.receive() function has a side effect of consuming the front message in the queue (i.e. removing it from the queue) and so we need to receive the message before we can then compare its contents against different things as if we received it every time, the second thing we compared the message to would have a different message to check 
#                 if msg == "moveRight":#and adjust their position accordingly
#                     topPos += 1
#                 elif msg == "moveLeft": 
#                     topPos -= 1
            
#             if topPos >= 4: #The paddles should only go as far as the 4th led out of 5 since they are 2 in length and if they went to the last one then half of them would be cut off
#                 topPos = 3
#             elif topPos < 0: #The paddles can't be below 0 as they'd be off the screen.
#                 topPos = 0
#             if bottomPos < 0:
#                 bottomPos = 0
#             elif bottomPos >= 4:
#                 bottomPos = 3
                
#             frameCount += 1 #Increment the frame count for this frame.
#             if frameCount % DIFFICULTY == 0: #Every DIFFICULTY frames we are due to move the ball.
#                 if ballPos[0] == 1: #If the ball is on the second to top line
#                     if ballPos[1] == topPos or ballPos[1] == topPos+1: #If it lines up horizontally with the top paddle it needs to bounce off the paddle
#                         ballVelocity[0] = -ballVelocity[0] #so flip the vertical component of the velocity
#                     else:
#                         bottomScore += 1 #if the ball is about to go onto the top row but it doesn't line up with a paddle then the top player has missed it so the bottom player scores one point.
#                         ballPos = [2,2] #So reset the ball position to the centre of the screen. you could extend this by making the ball go into a random position at the beginning of each game but make sure both microbits get the same random place (hint: use random.seed or even better send the randomly chosen space by radio)
#                         ballVelocity = [-1,-1] #Reset the ball's velocity so it travels upwards and to the left ready for the next point
#                         display.scroll("Top: " + str(topScore) + " Bottom: " + str(bottomScore)) #tell the user the score
#                 elif ballPos[0] == 3: #if the ball is on the second to bottom line 
#                     if ballPos[1] == bottomPos or ballPos[1] == bottomPos+1: #if it lines up horizontally with the bottom paddle then it must bounce
#                         ballVelocity[0] = -ballVelocity[0]
#                     else: #Otherwise the top player scores and we reset the game.
#                         topScore += 1
#                         ballPos = [2,2] #Again you could make this a random start position
#                         ballVelocity = [-1,-1]
#                         display.scroll("Top: " + str(topScore) + " Bottom: " + str(bottomScore))
    
                
#                 ballPos[0] += ballVelocity[0] #On every frame where we move the ball we add its velocity to its position in both x and y directions
#                 ballPos[1] += ballVelocity[1]
                
#                 if ballPos[1] < 0: #if the ball is off the screen laterally then put it back on
#                     ballPos[1] = 0
#                 elif ballPos[1] > 4:
#                     ballPos[1] = 4
                    
#                 if ballPos[1] == 4 or ballPos[1] == 0: #If the ball is touching the edge laterally then it should bounce in the x direction
#                     ballVelocity[1] = -ballVelocity[1]


#             display.show(generateImage(topPos,bottomPos,ballPos))#Show the current state of the game

#         if topScore == 5:
#             display.scroll("The winner is the top player.")#At the end of the game say who won and then start a new game by looping
#         else:
#             display.scroll("The winner is the bottom player.")
        