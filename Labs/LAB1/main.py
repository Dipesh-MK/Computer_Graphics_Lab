import dda_line
import bresenham_line
import bresenham_circle

def menu():
    while True:
        print("\n--- CG Algorithms ---")
        print("1. DDA Line")
        print("2. Bresenham Line")
        print("3. Bresenham Circle")
        print("4. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            dda_line.run()
        elif choice == "2":
            bresenham_line.run()
        elif choice == "3":
            bresenham_circle.run()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()