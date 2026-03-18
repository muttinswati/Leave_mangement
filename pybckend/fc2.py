# bkd 1 request cycle

import mysql.connector
import os
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','pybckend')))
from ep import latest_leave_email, latest_date

unique_code=None

sqlpass=os.environ.get('mysqlpass')
leaver_email=latest_leave_email


mydb=mysql.connector.connect(host='localhost',user='root',passwd=sqlpass,database='ecollege') #this step is to connect to db

mycursor=mydb.cursor() # is like pointer pointing to db 

from datetime import datetime

ddatee = latest_date  # '2025-05-06' or '06-05-2025'

from datetime import datetime

# DEBUG: Print the received date string
print(f"DEBUG: ddatee value received = {ddatee}")

# Validate and parse the date
if not ddatee:
    raise ValueError("❌ Date is None — extraction likely failed.")

# Try parsing with both formats
date_obj = None
for fmt in ('%d-%m-%Y', '%Y-%m-%d'):
    try:
        date_obj = datetime.strptime(ddatee.strip(), fmt)
        break
    except ValueError:
        continue

# If both formats fail, raise error
if date_obj is None:
    raise ValueError(f"❌ Date format for '{ddatee}' is invalid. Expected DD-MM-YYYY or YYYY-MM-DD.")

# Get the weekday
days = date_obj.strftime('%A')
print(f"✅ The day of the date ({ddatee}) is {days}")



#  FOR EMAIL

def get_valid_email(mycursor,leaver_email):
    q4=""" SELECT email FROM teachers WHERE email=%s"""
    mycursor.execute(q4, (leaver_email,))
    r4=mycursor.fetchone()

    if r4:
        # for i in r4:
        #     print(i)
        return r4[0]




# for DAY

def get_valid_day(mycursor,days):
    q3=""" SELECT dayname FROM Days WHERE dayname=%s"""
    mycursor.execute(q3,(days,))
    r3=mycursor.fetchone()

    if r3:
        # for i in r3:
        #     print(i)
        return r3[0]


# FOR FID

def get_fid_email(mycursor,leaver_email):

    q1=""" SELECT fid FROM teachers WHERE email=%s """
    mycursor.execute(q1,(leaver_email,))

    r1=mycursor.fetchone()

    # for i in r1:
    #     print('fid:',i)

    return r1[0]

ffid=get_fid_email(mycursor,leaver_email)


# FOR VACANT CLASS

def get_vacant_class(mycursor,f_id,days):
    q="""SELECT timings,dae,divs,subname 
    FROM timetable
    JOIN subject 
    ON timetable.scode=subject.subcode
    where teachid=%s and dae=%s"""
    mycursor.execute(q, (f_id[0], days))  # ✅ Correct: This is a flat tuple with two elements
    r= mycursor.fetchall()

    for i in r:
        timings,dae,divs,subname=i
        print(f"class at {timings} on {dae} for {divs} sub {subname}")
    return r


def get_teachers_credentials(mycursor,f_id):
    q2=""" SELECT fname,lname,email FROM teachers WHERE fid=%s """
    mycursor.execute(q2,f_id)
    r2=mycursor.fetchall()

    for i in r2:
        fname,lname,email=i
        print(f" the {fname}.{lname} teacher's email is {email}")
    return r2


def get_leave_credentials(mycursor,leaver_email):
    q2=""" SELECT fname,lname FROM teachers WHERE email=%s """
    mycursor.execute(q2,(leaver_email,))
    r2=mycursor.fetchall()

    for i in r2:
        fname,lname=i
        print(f"The leave teacher is {fname} {lname}")
    return r2




def runcode():
    results=[]
    inserts=[]
    if leaver_email and days:
        valid_email=get_valid_email(mycursor,leaver_email)
        if valid_email:
            valid_day=get_valid_day(mycursor,days)
            if valid_day:
                f_id=get_fid_email(mycursor,leaver_email)
                if f_id:
                    my_class=get_vacant_class(mycursor,(f_id,),days)
                    for i in my_class:
                        print(i)
                        # tdiv=ffid+"#"+latest_date+"$"+str(i[0])+"@"+i[2]
                        unique_code = f"{ffid}#{latest_date}${str(i[0])}@{i[2]}"
                        # print(tdiv)
                        print(unique_code)
                        inserts.append((unique_code, ffid))
                        results.append((i[0],i[1],i[2],i[3],unique_code))
                        
                    if inserts:
                        q = "INSERT INTO subteacher (vacantcode, at_id) VALUES (%s, %s)"
                        mycursor.executemany(q, inserts)
                        mydb.commit()
                        print(" All entries inserted successfully !!!!!")

                    return results   
                    
                else:
                    print('your are not regitsered')

            else:
                print('Sorry no class on Sunday')

        else:
            print("Email is not available in db")
    return results

# def get_unique_code:
#     query="""INSERT INTO subteacher WHERE fid=%s and dae=%s"""
#     mycursor.execute(query,(f_id[0],days))
#     res=

# insertion="""Alter table subteacher add column subsemail varchar(10)"""
# mycursor.execute(insertion)
# r=mydb.commit()
# print('columns added ')


if __name__=="__main__":
    a=runcode()
    print(a)
    # credentials=get_teachers_credentials(mycursor,f_id)
    
    