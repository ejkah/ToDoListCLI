# import sys

# if len(sys.argv) > 1:
#     print(f"Hello, {sys.argv[1]}!")
# else:
#     print("Please provide a name as an argument.")

from datetime import date
import sqlite3


def todo_list_menu():
    print("-------------")
    print("Enter number to select option: ")
    print("-------------")
    print("1) Add item to todo list")
    print("2) List items in todo list")
    print("3) View current todo item")
    print("4) Delete current item")
    print("5) Delete specific item")
    print("6) Set specific item to complete")
    print("7) Exit program")

    print(" ")


def display_todo_list():
    print("Todo List - " + str(today))
    print("-------------------------")
    n = 0
    while n < len(todo_list):
        print(str(n + 1) + ". " + str(todo_list[n]))
        n += 1


def add_whitespace():
    print(" ")
    print(" ")


# def read_file():
#     with open("/Users/ec/PycharmProjects/pythonToDoListCLI/ToDoLists/testlist.txt") as f:
#         for x in f:
#             stripped = x.strip()
#             if stripped:
#                 todo_list.append(stripped)


# def write_to_file(todo_item):
#     with open("/Users/ec/PycharmProjects/pythonToDoListCLI/ToDoLists/testlist.txt", "a") as f:
#         f.write(todo_item + "\n")


def read_from_db():
    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()
    cursor.execute("SELECT to_do_item from tdl")
    output = cursor.fetchall()
    for to_do_item in output:
        tuple_to_string = str(to_do_item)
        stripped_to_do_item = tuple_to_string.strip("('',)")
        todo_list.append(stripped_to_do_item)

    conn.commit()
    conn.close()


def write_to_db(todo_item):
    # Add todo_item into db
    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tdl (to_do_item) VALUES (?)", (todo_item,))
    conn.commit()
    conn.close()


def delete_item(index_number):
    conn = sqlite3.connect('todolist.db')
    conn.executescript("""
    BEGIN TRANSACTION;

    CREATE TABLE tdl_new AS
    SELECT 
        ROW_NUMBER() OVER (ORDER BY id) AS id,
        to_do_item
    FROM tdl;

    DROP TABLE tdl;
    ALTER TABLE tdl_new RENAME TO tdl;
    
    COMMIT;

    """)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tdl WHERE id = ?", (index_number,))

    conn.commit()
    conn.close()


enter_loop = True
todo_list = []
today = date.today()
read_from_db()

print(" ")
print("To Do List")  # Add date here
print(" ")

while enter_loop:

    todo_list_menu()
    selection = input()

    if selection == '1':
        add_whitespace()
        print("Enter item in todo list: ")
        item = input()
        # write to file
        write_to_db(item)
        # append to list
        todo_list.append(item)
        add_whitespace()

    elif selection == '2':
        add_whitespace()
        display_todo_list()
        add_whitespace()

    elif selection == '3':
        add_whitespace()
        print(todo_list[0])
        add_whitespace()

    # TODO: selection 4 and 5 are not updating the text file. Add db.
    elif selection == '4':
        add_whitespace()
        todo_list.pop(0)
        # how to delete first item in file?
        display_todo_list()
        add_whitespace()

    elif selection == '5':
        add_whitespace()
        display_todo_list()
        print(" ")  # Refactor add_whitespace method to take in int param to customize how many white space to add
        print("Enter number of item to delete: ")
        item_number = input()
        int_number = int(item_number)
        # TODO: pop index out of range error
        popped_item = todo_list.pop(int_number - 1)
        print(" ")
        delete_item(int_number)
        display_todo_list()
        add_whitespace()

    elif selection == '6':
        add_whitespace()
        display_todo_list()
        print(" ")  # Refactor add_whitespace method to take in int param to customize how many white space to add
        print("Enter number of item to set complete: ")
        item_number = input()  # 1

        n = 0
        while n < len(todo_list):
            if n == (int(item_number) - 1):
                todo_list[int(item_number) - 1] = todo_list[int(item_number) - 1] + " - COMPLETE"
                break
            n += 1

        print(" ")
        display_todo_list()
        add_whitespace()

    elif selection == '7':
        add_whitespace()
        print("Exiting program.")
        add_whitespace()
        enter_loop = False

    else:
        add_whitespace()
        print("Select one of the given options.")
        add_whitespace()