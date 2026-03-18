import mysql.connector
import smtplib
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Add backend folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybckend')))

from rescycle import booking_confirmations, verification
from ep import latest_leave_email
from fc2 import get_leave_credentials, runcode

sqlpass = os.environ.get('mysqlpass')

mydb = mysql.connector.connect(host='localhost', user='root', passwd=sqlpass, database='ecollege')
mycursor = mydb.cursor()

# Get confirmation data and process it
# rcode=runcode()
leaver_email = latest_leave_email
data = booking_confirmations()
assigned_classes, unassigned_classes = verification(data)
leaver_name = get_leave_credentials(mycursor, leaver_email)

# Parse code like "KE03#2025-05-06$13:30:00@4C"
def parse_vacantcode(code):
    try:
        parts = code.split('#')
        date_part = parts[1].split('$')[0]
        time_part = parts[1].split('$')[1].split('@')[0]
        class_part = parts[1].split('@')[1]
        return date_part, time_part, class_part
    except:
        return "Unknown", "Unknown", "Unknown"

# Generate class assignment list for emails
def generate_class_assignment_list(assigned_classes):
    class_list = ""
    for entry in assigned_classes:
        for teacher in entry[0]:
            fname, lname, fid, email, gender, classcode = teacher
            date, time, class_name = parse_vacantcode(classcode)
            salutation = "Mr." if gender.lower() == "male" else "Ms."
            class_list += f"<p>{salutation} {fname} {lname} will take class <strong>{class_name}</strong> at <strong>{time}</strong> on <strong>{date}</strong>.</p>\n"
    return class_list

# Clean email body builder
def create_email_body(assigned_classes, unassigned_classes):
    if leaver_name:
        fname, lname = leaver_name[0]
        message = f"<p>Dear HOD,<br><br>This is a class assignment update for <strong>{fname} {lname}</strong>'s leave request.</p>"
    else:
        message = "<p>Dear HOD<br><br>This is a class assignment update for the leave request.</p>"

    # Handle assigned classes
    if assigned_classes:
        message += "<h3>Assigned Classes:</h3>"
        message += generate_class_assignment_list(assigned_classes)
    else:
        message += "<p><strong>No classes have been assigned yet.</strong></p>"

    # Handle unassigned classes
    if unassigned_classes:
        message += "<h3>Unassigned Classes:</h3><ul>"
        for class_code in unassigned_classes:
            date, time, class_name = parse_vacantcode(class_code)
            message += f"<li>Class <strong>{class_name}</strong> scheduled for <strong>{date}</strong> at <strong>{time}</strong> is still unassigned.</li>"
        message += "</ul>"
    else:
        message += "<p><strong>All classes have been successfully assigned.</strong></p>"

    message += "<br><p>Regards,<br>Auto Email System</p>"
    return message

# Send email function
def send_email(to_emails, subject, html_content):
    from_email = "staranimex35@gmail.com"
    app_password = os.environ.get("emailpass")  # Use your Gmail App password securely

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(from_email, app_password)
        smtp.send_message(msg)
        print("Email sent!")

# Approval function for HOD to approve/reject using buttons
def send_approval_request_to_hod(assigned_classes, leaver_email, leaver_name):
    approval_body = f"<p>Dear HOD,</p>"
    approval_body += f"<p>This is a class assignment update for <strong>{leaver_name[0]} {leaver_name[1]}</strong>'s leave request.</p>"

    approval_body += "<h3>Assigned Classes:</h3>"
    approval_body += generate_class_assignment_list(assigned_classes)

    approval_body += f"""
    <p>Click below to approve or reject:</p>
    <a href="mailto:staranimex35@gmail.com?subject=Approve&body=APPROVE:{leaver_email}" style="padding: 10px 20px; background-color: green; color: white; text-decoration: none; border-radius: 5px; margin-right: 20px;">Approve</a>
    <a href="mailto:staranimex35@gmail.com?subject=Reject&body=REJECT:{leaver_email}" style="padding: 10px 20px; background-color: red; color: white; text-decoration: none; border-radius: 5px;">Reject</a>
    <p>Regards,<br>Auto Email System</p>
    """
    send_email(["boltmuttin35@gmail.com"], "Booking Approval Request", approval_body)

# Process the approval/rejection button clicks (mocked here)
def process_button_click(response, leaver_email, leaver_name):
    if "APPROVE" in response:
        confirmation_body = f"<p>Dear {leaver_name[0]},</p>"
        confirmation_body += "<p>Your leave request has been approved. Below are the confirmed class assignments:</p>"
        confirmation_body += generate_class_assignment_list(assigned_classes)
        confirmation_body += "<p>Regards,<br>Auto Email System</p>"
        send_email([leaver_email], "Leave Approved", confirmation_body)

    elif "REJECT" in response:
        rejection_body = f"<p>Dear {leaver_name[0]},</p><p>Your leave request has been <strong>rejected</strong> by HOD.</p><p>Please follow up manually if needed.</p>"
        send_email([leaver_email], "Leave Rejected", rejection_body)

# Main flow
email_body = create_email_body(assigned_classes, unassigned_classes)

# Step 1: Send email to HOD with approval request
send_approval_request_to_hod(assigned_classes, leaver_email, leaver_name[0])

# Step 2: Process the approval/rejection response
# (for testing purposes, simulating the HOD decision - In reality, this would be an automated process)
hod_response = "APPROVE"  # Or "REJECT" - Simulated response for testing
process_button_click(hod_response, leaver_email, leaver_name[0])

# Optional: Send the confirmation to admin or log
send_email(["boltmuttin35@gmail.com"], "Leave Confirmation Report", email_body)
