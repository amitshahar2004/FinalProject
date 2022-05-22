import getpass, smtplib

try: #Try to execute the code between try: and except:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('amitshproject@gmail.com','hronen100') #<-- SMTPAuthenicationError is raised here.
    #Now Python will look for an Except clause that handles that specific error, skipping over the rest of the Try clause.
    #Which is printing that we are logged in, which we aren't!

    print ("Logged in as ")

except smtplib.SMTPAuthenticationError:        #Found it!
    print ("Error! Wrong password or username.")