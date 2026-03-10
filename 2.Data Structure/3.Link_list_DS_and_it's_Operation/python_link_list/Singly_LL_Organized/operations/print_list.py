
from linked_list.linked_list import LinkedList

@LinkedList.register_operation
def print_list(self):
    temp = self.head
    if not temp:
        print("Empty List")
        return
    while temp is not None:
        print(temp.value, end=" -> " if temp.next else "\n")
        temp = temp.next