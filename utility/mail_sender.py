# Imports
import email.message as msg
import smtplib

# Constants
SYSTEM_NAME = "Safe Route Manager"                                                   # NAME
SYSTEM_EMAIL = "saferoute.manager@yahoo.com"                                         # EMAIL
SYSTEM_PASSWORD = "CANLQb=tKjgU@NNu^b9kU_xK*DAeWSkJ8Lv#@!+_JjY?cq-Wt&qUhRTbcTh8D7Dw" # EMAIL PASSWORD
SYSTEM_APP = "mail"                                                                  # APP NAME (YAHOO)
SYSTEM_APP_PASSWORD = "cczttrfuxupixqii"                                             # APP PASSWORD (FOR YAHOO)
SYSTEM_EMAIL_SUBJECT = "Abnormal Behavior Detected for User {user_name}"
SYSTEM_EMAIL_BODY = "Something might happen to {user_name}, please try to contact the person.\nIf the related user is unable to response, it might be a good idea to contact your local authority."
SYSTEM_EMAIL_NOTE = "\n\nMore information:\n{info}"

def create_email(recipient_email:str, username:str,
        sender:str=SYSTEM_EMAIL, subject:str=SYSTEM_EMAIL_SUBJECT,
        body:str=SYSTEM_EMAIL_BODY, note:dict[str,str]={}) -> msg.EmailMessage:
    """Create an email with the given receiver and username.
    kwargs is used to add note such as last_known_location
    Note:
    - recipient_email can be in the form of list of string (for multiple recipients)"""
    message = msg.EmailMessage()
    message["From"] = sender
    message["To"] = recipient_email
    message["Subject"] = subject.format(user_name=username)
    message_body = body.format(user_name=username)
    if note:
        message_body += convert_note(note)
    message.set_content(message_body)
    return message

def convert_note(args:dict[str,str], note_format:str=SYSTEM_EMAIL_NOTE) -> str:
    """Convert args (dictionary) to a note list (string)"""
    note_list = ""
    for note_title in args:
        note_list += f"- {str.title(note_title.replace('_', ' '))} : {args[note_title]}\n"
    return note_format.format(info=note_list)

def send_email(recipient_email:str, message:msg.EmailMessage,
        sender_email:str=SYSTEM_EMAIL, sender_password:str=SYSTEM_APP_PASSWORD,
        log:bool=False):
    """Send email to the recipient from sender"""
    mail_server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    # Trigger security
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(sender_email, sender_password)
    # Send mail
    mail_server.send_message(message)
    # Close connection
    mail_server.quit()
    if log:
        print(f"Email successfully sent to {recipient_email}")


def create_send_email(recipient_email:str, username:str,
        sender_email:str=SYSTEM_EMAIL, subject:str=SYSTEM_EMAIL_SUBJECT,
        body:str=SYSTEM_EMAIL_BODY, sender_password:str=SYSTEM_APP_PASSWORD,
        log:bool=False, **kwargs):
    """Create and send email function wrapper"""
    mail = create_email(recipient_email=recipient_email, username=username,
        sender=sender_email, subject=subject, body=body, note=kwargs)
    send_email(recipient_email=recipient_email, message=mail,
        sender_email=sender_email, sender_password=sender_password, log=log)