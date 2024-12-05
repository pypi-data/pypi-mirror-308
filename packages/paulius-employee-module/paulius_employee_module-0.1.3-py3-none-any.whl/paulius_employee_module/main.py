from paulius_employee_module.employee import Employee

darb1 = Employee("Paulius", "Lapienis", 2000)

# this is a comment
if input().strip() == "with hello":
    print(f"Hello, {darb1}!")
else:
    print(darb1)