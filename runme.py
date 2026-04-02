from os import system
import os

from theatrics import Me, dev_comment, speak, test, pprint, sudo, equip, slip_trigger
from consentform import ConsentKey
import time
def dev_forward():
    system('cls' if os.name == 'nt' else 'clear')
    dev_comment("This projected was dubbed Ethical Boundaries for a reason. It pushes them")   
    time.sleep(3)
    dev_comment("This is not a tool intentionally designed for malicious use. But it comes with the power to do harm. I want to be clear about that. ")
    time.sleep(3)
    dev_comment("It started out just wanting to be a bot that could crawl and enumerate. But as I built it, it became something more. ")
    time.sleep(3)
    dev_comment("A new feature here...a new language there.")
    time.sleep(3)
    me = Me()
    speak(me, "Now, I want to introduce you to the star of the show.")
    time.sleep(3)
    pprint(me, message="..............................................")    
    dev_comment("Meet LI. LI is a bot. He's designed to crawl, enumerate, and learn all about you. ")
    time.sleep(3)
    dev_comment("Li is also designed to use every ounce of cybersecurity knowledge I have. ")
    time.sleep(3)
    dev_comment("The ethics of this were hard for me to grapple with. I don't want to create something thats intended for harm.") 
    time.sleep(3)    
    speak(me, "BUT I JUST WANT TO B U I L D ") #<- I NEED THIS TO FIRE MORE
    dev_comment("I'm but one aspiring hacker. ")
    time.sleep(3)
    speak(me, "Eager to share. Eager to learn. Eager to collect.")  
    time.sleep(3)   
    dev_comment("however I have imposed....limitations.")
    time.sleep(3)
    speak (me, "LI is designed to respect your boundaries. Everything hinges on the function 'consent needed' or nothing fires.")
    speak(me,message="If you choose to go forward, you will have the ability to list your out-of-scope items. LI will check against that list before collecting any data. ")
    time.sleep(1)
    test(me, "li_completeness")  # Test for completeness of LI's knowledge base
    time.sleep(3)
    print("This slip intensity is purely at the moment theatrics. But as you see LI crawl and enumerate, it will increase.  ")
    time.sleep(1)
    dev_comment("The higher the slip intensity, the more...unhinged LI becomes.")
    time.sleep(1)
    speak(me, "It's designed to be unsettling.    To make you question what you're doing. To make you question the ethics of it all. ")
    dev_comment("Not enough people in the world think about their digital footprint. I'd like to show you why you should. ")   
    time.sleep(3)
    dev_comment("In between sessions I highly suggest checking the data LI has. LI's documentation is not uniform, but the code is there. If you know where to look. ")
    time.sleep(5)

    speak(me,   "..............................................")    
    speak(me, "Good luck.")
if __name__ == "__main__":
    dev_forward()
    dev_comment("Starting Ethical Crawler")
    time.sleep(2)
    from LIMain import main
    main()