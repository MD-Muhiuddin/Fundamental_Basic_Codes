from linked_list.linked_list import LinkedList
# This import is what 'glues' the operations to the LinkedList class
import operations 

def main():
    # Initialize list
    my_ll = LinkedList(10)
    
    # Test Operations
    print("--- Adding Elements ---")
    my_ll.append(20)
    my_ll.append(30)
    my_ll.prepend(5)
    my_ll.print_list()  # Output: 5 -> 10 -> 20 -> 30

    print("\n--- Popping First ---")
    popped = my_ll.pop_first()
    print(f"Popped value: {popped.value if popped else 'None'}")
    my_ll.print_list()  # Output: 10 -> 20 -> 30

    print("\n ---- prepending more elements ---")
    my_ll.prepend(1)
    my_ll.prepend(0)
    my_ll.print_list()  # Output: 0 -> 1 -> 10 ->

    print("\n--- Reversing List ---")
    my_ll.reverse()
    my_ll.print_list()  # Output: 30 -> 20 -> 10 -> 1 -> 0

if __name__ == "__main__":
    main()