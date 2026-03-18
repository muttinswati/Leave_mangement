# Leave Management System (LMS) Automation

## Overview
This project automates the **faculty leave management process** for educational institutions. It streamlines class substitutions, email notifications, and administrative approvals, reducing manual work and ensuring that all classes are properly assigned when a teacher is on leave.

**Unique Approach / Highlights**
- Fully automated leave management **without any front-end interface**.
- All interactions happen through **Gmail emails**, making it lightweight and easily deployable.
- Handles **substitute allocation, approval workflow, and notifications** entirely via backend logic.

**Key Features:**
- Detects leave requests sent via Gmail automatically.
- Identifies unassigned classes and finds substitute teachers.
- Sends detailed email notifications to both the **HOD** and the teacher on leave.
- Allows the HOD to **approve or reject** the substitution.
  - If **approved**, the leave teacher is notified with the final class assignments.
  - If **rejected**, the HOD manually reassigns classes.
- Maintains a record of assigned and unassigned classes for reporting.

## Workflow (High-Level)
1. Teacher sends a **leave request via Gmail**.
2. System fetches the email and extracts:
   - Teacher’s email
   - Leave date
   - Reason for leave
3. Queries the database to identify **vacant classes**.
4. Finds eligible **substitute teachers** and sends class allocation emails.
5. **Collects confirmations** from substitutes.
6. Sends **HOD approval email** with:
   - List of assigned and unassigned classes
   - Details of substitutes for each class
   - Approve/Reject buttons
7. Based on HOD response:
   - If approved → leave teacher receives final assignment confirmation.
   - If rejected → HOD manually handles reassignments.

## Technologies Used
- **Python** – Automation, email handling, and backend logic
- **MySQL** – Database for teacher, timetable, and class records
- **Gmail IMAP** – Automatic email retrieval and parsing

## Setup & Run (Local Only)
1. Clone the repository.
2. Set environment variables:
   - `mysqlpass` → MySQL password
   - `emailpass` → Gmail app password
3. Run the main process:
```bash
python run_lms_process.py
```
4. System will handle leave detection, substitution, HOD approval, and final notifications automatically.

<img width="950" height="358" alt="image" src="https://github.com/user-attachments/assets/c3af64a6-3054-4cd1-83bf-9c3bb890ca7c" />
fig 1: Leave request notification email

<img width="995" height="601" alt="image" src="https://github.com/user-attachments/assets/23420f27-109f-4dc6-b756-adfd3687ecf5" />

<img width="893" height="553" alt="image" src="https://github.com/user-attachments/assets/6b2605cd-8615-477a-8d97-9f56a4fdd5cb" />

<img width="1002" height="446" alt="image" src="https://github.com/user-attachments/assets/34b49a1a-9b66-4df0-88d5-6f454edf5ffc" />


