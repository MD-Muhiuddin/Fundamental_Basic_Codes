from linked_list.linked_list import LinkedList

@LinkedList.register_operation
def set_value(self, index, value):
    temp = self.get(index)
    if temp:
        temp.value = value
        return True
    return False