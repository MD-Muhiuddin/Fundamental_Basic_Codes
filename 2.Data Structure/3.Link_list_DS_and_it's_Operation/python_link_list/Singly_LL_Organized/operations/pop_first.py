from linked_list.linked_list import LinkedList

@LinkedList.register_operation
def pop_first(self):
    if self.length == 0:
        return None
    temp = self.head
    if self.length == 1:
        self.head = None
        self.tail = None
    else:
        self.head = self.head.next
        temp.next = None
    self.length -= 1
    return temp