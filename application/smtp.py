import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .logger import logger

sender_email = "suhailahmadbhat685@gmail.com"
password = 'mpduxrygikkdjpcc'

def sendEmail(to, subject,messag):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(messag, "plain"))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        logger.debug("Logging to the sender account.")
        server.login(sender_email, password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        logger.debug("Mail sent to the customer Successfully.")
        server.close()

        return True
    except Exception as e:
        logger.error("Something went wrong during sending the mail.")
        logger.exception(e)
        return False



