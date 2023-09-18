import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.dal import get_recipient_email

def sendEmail(recipient_email : str, file_path : str):
    sender_email = "podcastpulse9@gmail.com"
    sender_password = "mqdzplzhayjedpug"
    subject = "Your podcast summary 🚀"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL or 587 for TLS
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    file_path = os.path.normpath(file_path)
    # print(file_path)
    with open(file_path, "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="txt")
    attachment.add_header("Content-Disposition", f"attachment; filename=summary.txt")
    message.attach(attachment)

    message_text = message.as_string()

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Use for TLS
        server.login(sender_email, sender_password)  # Uncomment for SMTP server requiring authentication
        server.sendmail(sender_email, recipient_email, message_text)
        server.quit()
        print("Email sent successfully.")
        return "Email sent successfully."
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return f"Error sending email: {str(e)}"

def send_worker_email(uuid, file_path):
    recipient_email = get_recipient_email(uuid)
    print("#123 ################# email === {}".format(recipient_email))
    sender_email = "podcastpulse9@gmail.com"
    sender_password = "mqdzplzhayjedpug"
    subject = "Your podcast summary 🚀"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL or 587 for TLS
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    file_path = os.path.normpath(file_path)
    # print(file_path)
    with open(file_path, "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="txt")
    attachment.add_header("Content-Disposition", f"attachment; filename=summary.txt")
    message.attach(attachment)

    message_text = message.as_string()

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Use for TLS
        server.login(sender_email, sender_password)  # Uncomment for SMTP server requiring authentication
        server.sendmail(sender_email, recipient_email, message_text)
        server.quit()
        print("Email sent successfully.")
        return "Email sent successfully."
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return f"Error sending email: {str(e)}"
