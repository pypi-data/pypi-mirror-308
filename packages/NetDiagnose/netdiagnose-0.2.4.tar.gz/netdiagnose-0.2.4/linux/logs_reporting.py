import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr

class ReportManager:
    def __init__(self, filename="network_diagnostic_report.txt"):
        self.filename = filename
        self.content = []

    def append_to_report(self,text):
        """Appends given text to the report content list."""
        self.content.append(text)

    def save_report(self):
      if not self.content:
        print("Error: Report content is empty.")
        return
    # Convert all items in content to strings and join them with newline for better formatting
      with open(self.filename, "w") as file:
        file.writelines(str(line) + "\n" for line in self.content)

    def email_report(self, recipient_email):
        """Emails the report file to the specified email."""
        sender_email = "MS_Pvh4Gm@trial-zr6ke4nn7v34on12.mlsender.net"
        smtp_server = "smtp.mailersend.net"
        smtp_port = 587  # TLS port
        smtp_user = "MS_Pvh4Gm@trial-zr6ke4nn7v34on12.mlsender.net"
        smtp_password = "u5NttfFgmP0TZl09"  # Replace with your App Password

        try:
            # Create the email message
            msg = EmailMessage()
            msg["Subject"] = "Network Analysis Report"
            msg["From"] = formataddr(("Report Manager", sender_email))
            msg["To"] = recipient_email
            msg.set_content("Please find the attached network analysis report.")

            # Attach the report file
            with open(self.filename, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(self.filename)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Upgrade the connection to TLS
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            print(f"Report sent successfully to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def save_and_email_report():
        """Saves the report to a file and optionally emails it."""
        
        recipient_email = input("Enter the recipient email address (or leave blank to skip): ").strip()
        if recipient_email:
            ReportManager.email_report(recipient_email)
        else:
            ReportManager.save_report()
            print("No email entered. Report saved locally.")

