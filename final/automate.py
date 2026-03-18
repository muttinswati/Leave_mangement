def run_lms_process():
    import os
    import mysql.connector
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pybckend')))

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pyfront')))

    import leaveemail
    from ep import latest_leave_email,latest_date
    from fc2 import get_leave_credentials,runcode
    import subsemail
    from epsec import booking_confirmations
    from rescycle import booking_confirmations,verification
    import finallast

    sqlpass = os.environ.get('mysqlpass')
    mydb = mysql.connector.connect(host='localhost', user='root', passwd=sqlpass, database='ecollege')
    mycursor = mydb.cursor()

    data = booking_confirmations()
    assigned_classes, unassigned_classes = verification(data)
    leaver_email = latest_leave_email()
    leaver_name = get_leave_credentials(mycursor, leaver_email)

    email_body = create_email_body(assigned_classes, unassigned_classes)
    send_approval_request_to_hod(assigned_classes, leaver_email, leaver_name)

    # Simulated approval for automation purposes
    hod_response = "APPROVE"
    process_button_click(hod_response, leaver_email, leaver_name, assigned_classes)

    send_email(["boltmuttin35@gmail.com"], "Leave Confirmation Report", email_body)

if __name__ == "__main__":
    run_lms_process()
