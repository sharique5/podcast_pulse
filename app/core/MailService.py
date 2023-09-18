import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.dal.get_podcast_details import get_recipient_email
import os

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

def sendEmail(recipient_email : str, file_path : str):
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
    subject = "Your podcast summary 🚀"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL or 587 for TLS
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    file_path = os.path.normpath(os.path.join('./summary', file_path))
    file_path += ".txt"
    summary_text = ""
    with open(file_path, "rb") as file:
        summary_text = file.read()
        attachment = MIMEApplication(summary_text, _subtype="txt")
    attachment.add_header("Content-Disposition", f"attachment; filename=summary.txt")
    message.attach(attachment)


    email_template = ""
    with open("./templates/email.html", "rb") as file:
        email_template = file.read().decode()
    
    email_template = email_template.replace("{{SUMMARY}}", summary_text.decode())
    
    html_email = MIMEText(email_template, 'html')
    message.attach(html_email)
    
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
