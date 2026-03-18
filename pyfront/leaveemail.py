# file 1 sends email to all teachers 

#main1 program
from email.message import EmailMessage
import ssl
import smtplib
import os

# Email setup
sender = "staranimex35@gmail.com"
receiver_emails = ["muttinswati9@gmail.com", "erenmika009@gmail.com","animexstar1935@gmail.com","delicatebrowns35@gmail.com","arahjain19@gmail.com","harrystylesmendes1456@gmail.com"]  # List of teachers who may apply for leave
password = os.environ.get("EMAIL_PASS")

# Cute leave request form HTML
leave_form_html = """
<html>
  <body style="font-family:Arial,sans-serif;">
    <p style="font-size:16px;">Hello,<br><br>
      Click the button below to request your leave. You only need to mention the <b>date</b> of leave and a <b>reason</b> (optional).
    </p>
    <p>
      <a href="mailto:staranimex35@gmail.com?subject=Leave%20Request&body=Date%20of%20Leave:%20_____%0AReason%20(optional):%20_____">
        <button style="padding:12px 22px;background-color:#f5a3c7;color:white;border:none;border-radius:10px;font-size:15px;">
          📧 Request Leave
        </button>
      </a>
    </p>
    <p style="font-size:14px;">Thanks!<br>Admin</p>
  </body>
</html>
"""

# Construct Email
em = EmailMessage()
em["From"] = sender
em["To"] = ", ".join(receiver_emails)
em["Subject"] = "Submit Leave Request"
em.set_content("Please use an HTML-compatible email client to use the leave request button.")
em.add_alternative(leave_form_html, subtype='html')

# Send Email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as mail:
    mail.login(sender, password)
    mail.send_message(em)

print("📧 Leave request form sent successfully to teachers.")
