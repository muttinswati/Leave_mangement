def run_lms_process():
    import os
    import sys
    import time
    import mysql.connector

    # Path setup
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pybckend')))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pyfront')))

    # Step 1: Trigger leave email (who is on leave)
    import leaveemail  # Assumes it reads leave mail

    print("Waiting a minutes for teachers to respond...")
    time.sleep(90)


    # Step 2: Fetch who applied leave
    from ep import latest_leave_email, latest_date
    from fc2 import get_leave_credentials
    leaver_email = latest_leave_email()
    leave_date = latest_date()

    sqlpass = os.environ.get('mysqlpass')
    mydb = mysql.connector.connect(host='localhost', user='root', passwd=sqlpass, database='ecollege')
    mycursor = mydb.cursor()

    leaver_name = get_leave_credentials(mycursor, leaver_email),runcode()

    # Step 3: Send substitution requests
    import subsemail  # Assumes it sends class booking emails to others

    print("Waiting 2 minutes for teachers to respond...")
    time.sleep(120)  # Wait 2 mins for substitutes to respond (optional delay)

    # Step 4: Fetch confirmations and verify
    from epsec import booking_confirmations as epsec_booking_confirmations
    from rescycle import booking_confirmations, verification

    # Use whichever booking_confirmation function is correct (if one imports the other, just use one)
    data = epsec_booking_confirmations()
    assigned_classes, unassigned_classes = verification(data)

    # Step 5: Prepare email body and send HOD approval request
    # from emailcontent import create_email_body
    # from hodapproval import send_approval_request_to_hod
    # email_body = create_email_body(assigned_classes, unassigned_classes)
    # send_approval_request_to_hod(assigned_classes, leaver_email, leaver_name)

    # # Step 6: Simulated HOD Approval
    # from responsemail import process_button_click
    # hod_response = "APPROVE"
    # process_button_click(hod_response, leaver_email, leaver_name, assigned_classes)

    # Step 7: Final email to all and leave-teacher
    import finallast  # Assumes it sends final status email

    print("LMS automation finished.")

if __name__ == "__main__":
    run_lms_process()
