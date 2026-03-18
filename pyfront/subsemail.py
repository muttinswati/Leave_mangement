#  sending list of class to other teachers 

import mysql.connector
from email.message import EmailMessage
import ssl
import smtplib
import os
import sys
import urllib.parse

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pybckend import fc2

# Load environment variables
sqlpass = os.environ.get('mysqlpass')
password = os.environ.get("emailpass")
leaver_email = fc2.leaver_email

# Connect to MySQL
mydb = mysql.connector.connect(
    host='localhost', user='root', passwd=sqlpass, database='ecollege')
mycursor = mydb.cursor()

# 📨 FUNCTION: Get allowed emails excluding the leave-taker
def get_receiver_emails(leaver_email):
    allowed_emails = [
        'muttinswati9@gmail.com',
        'erenmika009@gmail.com',
        'animexstar1935@gmail.com',
        'delicatebrowns35@gmail.com',
        'muttinbharatraj8@gmail.com', 
        'harrystylesmendes1456@gmail.com'
    ]
    
    placeholders = ','.join(['%s'] * len(allowed_emails))
    query = f"SELECT email FROM teachers WHERE email IN ({placeholders}) AND email != %s"
    mycursor.execute(query, (*allowed_emails, leaver_email))
    results = mycursor.fetchall()
    return [row[0] for row in results]

# Get filtered teacher emails
receiver_emails = get_receiver_emails(leaver_email)

# 🧠 Get classes needing substitutes
results = fc2.runcode()

# 📚 Build HTML booking buttons
sender = "staranimex35@gmail.com"
button_html = ""

for timing, day, divs, subname, unique_code in results:
    time_str = str(timing)[:-3]  # Removing seconds from the timedelta
    subject_line = f"Booking Confirmation - {divs} {subname} class at {time_str}"
    body_line = f"I will take the class for {divs} - {subname} at {time_str}\nYour unique code: {unique_code}"
    
    encoded_subject = urllib.parse.quote(subject_line)
    encoded_body = urllib.parse.quote(body_line)
    
    button_html += f"""
    <p>
      <a href="mailto:{sender}?subject={encoded_subject}&body={encoded_body}">
        <button style="padding:10px 20px;background-color:#ffc0cb;color:black;border:none;border-radius:10px;font-size:16px;">
          📚 Book {divs} - {subname} at {time_str}
        </button>
      </a>
    </p>
    """



# 📨 Compose HTML email
html = f"""
<html>
  <body>
    <p>Dear Teacher,<br><br>
      The following classes need substitutes. Please click the button for the class you’d like to take.
    </p>
    {button_html}
    <br>
    <p>Thank you!<br>Admin</p>
  </body>
</html>
"""

# 💌 Construct and Send Email
em = EmailMessage()
em["From"] = sender
em["To"] = ", ".join(receiver_emails)
em["Subject"] = "Class Booking Request - Substitute Needed"
em.set_content("Please use an HTML-compatible email client to see the booking options.")
em.add_alternative(html, subtype='html')

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as mail:
    mail.login(sender, password)
    mail.send_message(em)

print("✅ Email with dynamic booking buttons sent successfully!")
