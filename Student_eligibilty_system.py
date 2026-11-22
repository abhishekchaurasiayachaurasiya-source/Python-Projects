import csv
import os

# File ka naam define karna jisme data save hoga
FILE_NAME = "students.csv"
# Predefined courses ka tuple (Requirements ke hisaab se)
COURSES = ("BCCA", "BBA", "MCA", "B.Tech","BCA","M.Tech","BSc","BA")

# CSV file ke headers
FIELDNAMES = ["Roll Number", "Student Name", "Age", "Course", "Marks"]

def initialize_file():
    """CSV file create karta hai agar wo pehle se exist nahi karti."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def get_result_status(marks):
    """Marks ke basis par Pass ya Fail return karta hai."""
    try:
        if float(marks) >= 40:
            return "Pass"
        else:
            return "Fail" 
    except ValueError:
        return "Invalid Marks"

def add_student():
    """Naya student record add karne ke liye."""
    print("\n--- Add Student Record ---")
    roll_no = input("Enter Roll Number: ")
    name = input("Enter Student Name: ")
    age = int(input("Enter Age: "))
    
    # Yahan variable 'marks' (lowercase) use kiya hai taaki consistency rahe
    marks = input("Enter your Marks: ") 
    
    # Course selection with validation
    while True:
        print(f"Available Courses: {COURSES}")
        course = input("Select a course from the above options: ")
        if course in COURSES:
            break
        else:
            print("Invalid course! Please select only from the given options.")
            
    # FIXED: Yahan "Marks" key ko add kar diya gaya hai dictionary mein
    student_data = {
        "Roll Number": roll_no,
        "Student Name": name,
        "Age": age,
        "Course": course,
        "Marks": marks  
    }
    
    # CSV mein data append karna
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(student_data)
        
    print("Student record added successfully!")

def view_students():
    """CSV file se saare student records display karta hai."""
    print("\n--- View All Students ---")
    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        records = list(reader)
        if not records:
            print("No student records found.")
            return
        print(f"{'Roll No':<10} | {'Name':<20} | {'Age':<5} | {'Course':<10} | {'Marks':<40} | {'Status':<5}")
        print("-" * 65)
        for row in records:
            status = get_result_status(row.get('Marks', 0))
            print(f"{row['Roll Number']:<10} | {row['Student Name']:<20} | {row['Age']:<5} | {row['Course']:<10} | {row.get('Marks', 'N/A'):<40} | {status:<5}")

def search_student():
    """Roll Number ke basis par student ko search karta hai."""
    print("\n--- Search Student ---")
    search_roll = input("Enter Roll Number to search: ")
    
    found = False
    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Roll Number'] == search_roll:
                print("\nStudent Found:")
                print(f"Roll Number: {row['Roll Number']}")
                print(f"Name: {row['Student Name']}")
                print(f"Age: {row['Age']}")
                print(f"Course: {row['Course']}")
                print(f"Marks: {row.get('Marks', 'N/A')}")
                print(f"Result Status: {get_result_status(row.get('Marks', 0))}")
                found = True
                break
                
    if not found:
        print("Student Not Found")

def update_student():
    """Existing student details update karta hai (Name, Course, Marks)."""
    print("\n--- Update Student Record ---")
    update_roll = input("Enter Roll Number of student to update: ")
    
    updated_records = []
    found = False
    
    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Roll Number'] == update_roll:
                found = True
                print("Leave blank if you do not want to change a field.")
                new_name = input(f"Enter new Name ({row['Student Name']}): ") or row['Student Name']
                
                while True:
                    new_course = input(f"Enter new Course {COURSES} ({row['Course']}): ") or row['Course']
                    if new_course in COURSES:
                        break
                    else:
                        print("Invalid course! Please select from the given tuple options.")
                
                current_marks = row.get('Marks', '')
                new_marks = input(f"Enter new Marks ({current_marks}): ") or current_marks
                
                row['Student Name'] = new_name
                row['Course'] = new_course
                row['Marks'] = new_marks
                print("Record updated successfully!")
                
            updated_records.append(row)
            
    if not found:
        print("Student Not Found")
        return

    # Update ki hui list ko wapas CSV me likhna
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(updated_records)

def delete_student():
    """Roll Number ke basis par student record delete karta hai."""
    print("\n--- Delete Student Record ---")
    delete_roll = input("Enter Roll Number to delete: ")
    
    remaining_records = []
    found = False
    
    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Roll Number'] == delete_roll:
                found = True
            else:
                remaining_records.append(row)
                
    if found:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(remaining_records)
        print("Student record deleted successfully!")
    else:
        print("Student Not Found")

def main():
    """Main menu loop jo application ko continuously run karta hai."""
    initialize_file()
    
    while True:
        print("\n" + "="*27)
        print("  STUDENT MANAGEMENT SYSTEM")
        print("="*27)
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option from 1 to 6.")

# Program entry point
if __name__ == "__main__":
    main()