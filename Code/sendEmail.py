'''
This function sends an email from growboxcapstone@gmail.com
to the recipients specified.
'''
def sendEmail(who, message):
    #recipients are a list
    #message is a multiline string

    import smtplib, ssl

    #DECIDE WHO TO SEND TO
    if who.lower() == "capstone group":
        recipients  = [
                "levi2@umbc.edu",
                "smitwil1@umbc.edu",
                "ask2@umbc.edu",
                "draico1@umbc.edu"
                ]
        
    elif who.lower() == "just me":
        recipients = [
                "draico1@umbc.edu"
                ]
    else:
        recipients = who
        
    #START SENDING THE EMAIL
    sender_email = "growboxcapstone@gmail.com"  # From 
    password = "testing123!" 

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    sslcontext = ssl.create_default_context()

    #ITERATE THROUGH LIST OF RECIPIENTS AND SEND MESSAGE TO EACH
    for recipient in recipients:
        with smtplib.SMTP_SSL(host=smtp_server, port=port, context=sslcontext) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient, message)


#EXAMPLES OF WHAT THE MESSAGE SHOULD LOOK LIKE 

'''

message = """Subject: Testing Iot Email Prototype

Hey fellas, This is an email sent from the raspberry pi with python.

This is just for a proof of concept
"""

'''











