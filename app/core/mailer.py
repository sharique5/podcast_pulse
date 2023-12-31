import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

def sendEmail(recipient_email, file_path):
    subject = "Your podcast summary 🚀"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use 465 for SSL or 587 for TLS
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    file_path = os.path.normpath(file_path)
    # print(file_path)
    summary_text = ""
    with open(file_path, "rb") as file:
        summary_text = file.read()
        attachment = MIMEApplication(summary_text, _subtype="txt")
    attachment.add_header("Content-Disposition", f"attachment; filename=summary.txt")
    message.attach(attachment)

    email_template = ""
    curr_dir = os.path.dirname(os.path.abspath(__file__)) 
    template_file = os.path.normpath(os.path.join(curr_dir, "../", "../", "templates/email.html"))
    with open(template_file, "rb") as file:
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

# recipient_email = "priyam.poddar2@gmail.com" #insert recipient_email
# file_path = "summary.txt"  # Replace with the actual file path

# sendEmail(recipient_email, file_path)