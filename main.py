from b_plus_tree import BPlusTree
from users_manager import UserManager


def main():
    tree = BPlusTree()
    user_manager = UserManager(tree)

    while True:
        print("\nMenu:")
        print("1. Add User")
        print("2. Search User")
        print("3. Delete User")
        print("4. Search Users Greater Than")
        print("5. Search Users Less Than")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name to add: ")
            user_manager.add_user(name)
        elif choice == "2":
            name = input("Enter name to search: ")
            user_manager.search_user(name)
        elif choice == "3":
            name = input("Enter name to delete: ")
            user_manager.delete_user(name)
        elif choice == "4":
            name = input("Enter name to search greater than: ")
            user_manager.search_greater_or_less(name, True)
        elif choice == "5":
            name = input("Enter name to search less than: ")
            user_manager.search_greater_or_less(name, False)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
