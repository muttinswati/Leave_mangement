#  verification n assigns class

import mysql.connector
import os
from datetime import datetime
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.','pybckend')))

from epsec import booking_confirmations
from fc2 import runcode

sqlpass=os.environ.get('mysqlpass')
mydb=mysql.connector.connect(host='localhost',user='root',passwd=sqlpass,database='ecollege')
mycursor=mydb.cursor()


# q = """ALTER TABLE subteacher MODIFY COLUMN subsemail VARCHAR(225)"""
# mycursor.execute(q)
# r = mycursor.fetchone()
# print("altered")

# var=runcode()

data=booking_confirmations()
print(data)


def extraction(vacantcode):
    eid=vacantcode.split('#')[0]
    print(eid)
    return eid 


def verify_email(subsemail):
    q4=""" SELECT email FROM teachers WHERE email=%s"""
    mycursor.execute(q4, (subsemail,))
    r4=mycursor.fetchone()
    return r4

def check_vacant_code(vacantcode):
        q3="""select vacantcode from subteacher where vacantcode=%s"""
        mycursor.execute(q3,(vacantcode,))
        r3=mycursor.fetchone()
        return r3 is not None 

def check_subteacher_email(vacantcode):
    q2 = "SELECT COUNT(*) FROM subteacher WHERE vacantcode = %s AND subsemail IS NULL"
    mycursor.execute(q2, (vacantcode,))
    r2 = mycursor.fetchone()
    return r2[0] != 0


def set_email(subsemail,vacantcode):
    valid_entry="""UPDATE subteacher SET subsemail = %s 
    WHERE vacantcode = %s AND subsemail IS NULL"""
    mycursor.execute(valid_entry,(subsemail,vacantcode))
    mydb.commit()
    print("email added")

def check_email1(eid):
    q2="""SELECT COUNT(*),at_id FROM subteacher WHERE at_id=%s and subsemail IS NULL"""
    mycursor.execute(q2,(eid,))
    r2=mycursor.fetchone()
    return r2[0] != 0 


def selection(at_id):
    q="""SELECT vacantcode,subsemail FROM subteacher WHERE at_id=%s"""
    mycursor.execute(q,(at_id,))
    re=mycursor.fetchall()

    for i in re:
        print(i)
    return re

def delete_row(fid):
    q="""Delete FROM subteacher WHERE at_id=%s"""
    mycursor.execute(q,(fid,))
    mydb.commit()




# var=final_check(list)
def get_subteacher(eid):
    q = """
    SELECT t.fname, t.lname, t.fid, t.email, t.gender, s.vacantcode
    FROM teachers t
    JOIN subteacher s ON t.email = s.subsemail
    WHERE s.at_id = %s
    """
    mycursor.execute(q, (eid,))
    result = mycursor.fetchall()
    
    for row in result:
        print(row)
    return result  # List of tuples with teacher info + which class they took






# def booked(subsemail):
#     q="""select subsemail from subteacher WHERE subsemail=%s """
#     mycursor.execute(q,(subsemail,))
#     r=mycursor.fetchone()
#     return r is not None
# def unassigned_clases(fid)



# check in response its good
def verification(data):
    assigned_classes = []
    unassigned_classes = []
    for subsemail, vacantcode, fid in data:
        r4 = verify_email(subsemail)
        if r4:
            r3 = check_vacant_code(vacantcode)
            if r3:
                val = check_subteacher_email(vacantcode) # is  
                if val:
                    set_email(subsemail, vacantcode) # insert the email into subteacher
                    eid=extraction(vacantcode)
                    if eid:
                        if check_email1(eid):
                            print("Not all classes are assigned ")
                        else:
                            print("all classes are assigned (now) to other teachers")
                            mail_info=get_subteacher(eid)
                            print("fetched info for mail")
                            assigned_classes.append((mail_info,))
                            delete_row(fid)
                            print("deleted")
                        # print(mail_info)

                else:
                    print("class assigned to other teacher")
            else:
                print("the vacant code is not in db")
        else:
            print("email not in db")

    #  for unassigned classes 
    q = "SELECT vacantcode FROM subteacher WHERE subsemail IS NULL"
    mycursor.execute(q)
    r = mycursor.fetchall()
    for row in r:
        unassigned_classes.append(row[0])  # now you're collecting all unassigned codes
    
    print(unassigned_classes)
    return assigned_classes,unassigned_classes


# def final_check(data):
#     assigned_classes = []
#     # unassigned_classes = []

#     for subsemail, vacantcode, at_id in data:
#         final_var1 = check_email1(at_id)
#         if final_var1:
#             print("Not all classes yet assigned")
#         else:
#             print("All classes are assigned to other teachers")
#             selected = selection(at_id)
#             assigned_classes.extend(selected)  # FLATTEN list of (vacantcode, subsemail)
#             # delete_row(at_id)

    
    # Optional: remove duplicates from both lists
    # assigned_classes = list(set(assigned_classes))
    # # unassigned_classes = list(set(unassigned_classes))

    # return assigned_classes

# def unassigned_classes():





if __name__ =="__main__":
    # insertion_table(data)
    ass,us=verification(data)
    print(ass)
    print("assigned classes completed")
    print(us)
    # assigned_classes=final_check(data)
    # ls=get_subteacher(assigned_classes)
    

