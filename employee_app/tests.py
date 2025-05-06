# from django.test import TestCase
from django.template.defaultfilters import length


# Create your tests here.
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def append(self,value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length+=1
        return True

    def prepend(self,value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length+=1
        return True

    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length-=1
        if self.length ==0:
            self.tail = None
        return temp


    def pop_end(self):
        if self.length == 0:
            return None
        temp = self.head
        pre= self.head
        while(temp.next):
            pre = temp
            temp = temp.next
        self.tail = pre
        self.tail.next = None
        self.length-=1
        if self.length == 0:
            self.tail = None
            self.head = None
        return temp

    def get(self, index):
        if index <0 or index>=self.length:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp

    def set_value(self, value, index):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False




my_linked_list = LinkedList(1)
my_linked_list.append(2)
my_linked_list.append(3)
my_linked_list.append(4)
# my_linked_list.print_list()
# my_linked_list.pop_end()
# print('---------------------')
# my_linked_list.print_list()
# my_linked_list.pop_end()
# print('---------------------')
# my_linked_list.print_list()
# my_linked_list.pop_end()
# print('---------------------')
# my_linked_list.print_list()
#
# my_linked_list.prepend(5)
#
# my_linked_list.append(6)
#
# my_linked_list.append(7)
# print('==========')
#
# my_linked_list.print_list()
#
#
# print('====+++++++======')
# my_linked_list.pop_first()
# my_linked_list.print_list()
#
# print('====+++++++======')
# my_linked_list.pop_first()
# my_linked_list.print_list()
#
# print('====+++++++======')
# my_linked_list.pop_first()
my_linked_list.print_list()
# print('-===-=-=-=-=')
print(my_linked_list.get(2),'--------------index')
print(my_linked_list.set_value(2, 3),'--------')
my_linked_list.print_list()