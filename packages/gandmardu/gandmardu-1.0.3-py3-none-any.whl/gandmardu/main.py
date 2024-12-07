def print_hello_world_code():
    # The code that would go into the gand.py file
    hello_world_code = '''print("Hello, gandu World!")
    1. Array Implementation of Stack (Using a List)
python
Copy code

    stack = []

def push(item):
    stack.append(item)

def pop():
    if not is_empty():
        return stack.pop()
    return None

def is_empty():
    return len(stack) == 0
2. Application of Stack for Postfix Expression Evaluation and Infix to Postfix Conversion
def evaluate_postfix(expression):
    stack = []
    for token in expression:
        if token.isdigit():
            stack.append(int(token))
        else:
            b, a = stack.pop(), stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(a / b)
    return stack.pop()

# Example: evaluate_postfix("53+82-*")
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack, postfix = [], []
    for token in expression:
        if token.isalnum():
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence.get(stack[-1], 0) >= precedence[token]:
                postfix.append(stack.pop())
            stack.append(token)
    while stack:
        postfix.append(stack.pop())
    return ''.join(postfix)

# Example: infix_to_postfix("3+5*2/(7-2)")
3. Array Implementation of Linear Queue
python
Copy code
queue = []

def enqueue(item):
    queue.append(item)

def dequeue():
    if not is_empty():
        return queue.pop(0)
    return None

def is_empty():
    return len(queue) == 0
4. Array Implementation of Circular Queue
python
Copy code
def create_queue(size):
    return {'queue': [None] * size, 'front': 0, 'rear': -1, 'size': size}

def enqueue(queue, item):
    if (queue['rear'] + 1) % queue['size'] == queue['front']:
        print("Queue is full")
    else:
        queue['rear'] = (queue['rear'] + 1) % queue['size']
        queue['queue'][queue['rear']] = item

def dequeue(queue):
    if queue['front'] == (queue['rear'] + 1) % queue['size']:
        print("Queue is empty")
    else:
        item = queue['queue'][queue['front']]
        queue['queue'][queue['front']] = None
        queue['front'] = (queue['front'] + 1) % queue['size']
        return item
5. Implementation of Singly Linked List
def create_node(value, next_node=None):
    return {'value': value, 'next': next_node}

def insert(head, value):
    if head is None:
        return create_node(value)
    current = head
    while current['next']:
        current = current['next']
    current['next'] = create_node(value)
    return head
6. Implementation of Doubly Linked List
def create_node(value, prev=None, next=None):
    return {'value': value, 'prev': prev, 'next': next}

def insert(head, value):
    if head is None:
        return create_node(value)
    current = head
    while current['next']:
        current = current['next']
    new_node = create_node(value, current)
    current['next'] = new_node
    return head
7. Linked List Implementation of Stack and Queue
Stack using Linked List
python
Copy code
stack = None

def push(value):
    global stack
    stack = create_node(value, stack)

def pop():
    global stack
    if stack:
        value = stack['value']
        stack = stack['next']
        return value
    return None
Queue using Linked List
python
Copy code
queue_front = queue_rear = None

def enqueue(value):
    global queue_front, queue_rear
    new_node = create_node(value)
    if queue_rear:
        queue_rear['next'] = new_node
    queue_rear = new_node
    if queue_front is None:
        queue_front = queue_rear

def dequeue():
    global queue_front
    if queue_front:
        value = queue_front['value']
        queue_front = queue_front['next']
        return value
    return None
8. Implementation of Linear Search and Binary Search Algorithms
def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

    def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
9. Implementation of Hash Table with Collision Resolution (Chaining)
python
Copy code
def create_hash_table(size):
    return [[] for _ in range(size)]

def hash_function(key, size):
    return key % size

def insert(hash_table, key, value):
    index = hash_function(key, len(hash_table))
    hash_table[index].append((key, value))
10. Implementation of Radix Sort Algorithm
python
Copy code
def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

def counting_sort(arr, exp):
    output = [0] * len(arr)
    count = [0] * 10
    for num in arr:
        count[(num // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for num in reversed(arr):
        output[count[(num // exp) % 10] - 1] = num
        count[(num // exp) % 10] -= 1
    for i in range(len(arr)):
        arr[i] = output[i]
11. Implementation of Merge Sort and Quick Sort Algorithms
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

    12. Implementation of Binary Search Tree
python
Copy code
def insert_bst(tree, value):
    if tree is None:
        return {'value': value, 'left': None, 'right': None}
    if value < tree['value']:
        tree['left'] = insert_bst(tree['left'], value)
    else:
        tree['right'] = insert_bst(tree['right'], value)
    return tree
x = 5   #if else condition
if x > 10:
    print("x is greater than 10")
else:
    print("x is not greater than 10")

x = 5   #if elif else ladder
if x > 10:
    print("x is greater than 10")
elif x<20:
    print("x is greater than 20")
else:
    print("x is not greater than 10 and 20")

for i in range(11):
    print(i) #for loop

num = 2 #while loop
while num <= 10:
    print(num)
    num = num + 1

num = int(input("Enter a number: "))
factorial = 1             #to find the  value of a number
# check if the number is negative, positive or zero
if num < 0:
   print("Sorry, factorial does not exist for negative numbers") 
elif num==0:
    print("The factorial of 0 is 1")
else:
  for i in range(1,num + 1):
      factorial = factorial*i
  print("The factorial of", num,"is", factorial)

string=input(("Enter a string: ")) 
if(string==string[::-1]):
      print("The string is a palindrome")
else:
      print("Not a palindrome")


def print_pattern(n):
# Outer for Loop for number of rows
    for row in range(n):
# Inner for Loop columns
        for column in range(n):
# prints first and last and middle row
            if ((row == 0 or row == n - 1 or row == n // 2) or 
                # prints first column
                    column == 0):
                print("*", end="")
            else:
                print(" ", end="")
        print()
size = int(input("Enter size: \t")) 
if size < 8:
    print("Enter a size greater than 8")
else:
    print_pattern(size)

x = input("Input comma separated sequence words:")
words = [word for word in x.split(",")]
print(",".join(sorted(list(set(words)))))


def fun(s):
    for i in s:
        if i.isalnum():
           print("True")
        else:
           print("False")
        if i.isalpha():
           print("True")
        else:
           print("False")
        if i.isdigit():
           print("True")
        else:
           print("False")
        if i.isupper():
           print("True")
        else:
           print("False")
        if i.islower():
           print("True")
        else:
           print("False")
s=input().split()
fun(s)

def str_count(x): 
    dict={} 
    for n in x: 
        keys=dict.keys()
        if n in keys:
            dict[n]+=1
        else:
            dict[n]=1
        return dict
print(str_count('welcome to python'))

n = int(input("enter the number of the letter on each line:"))
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
start=0 
end =n 
for i in range(0,len(alphabet)+1,n):
    print(alphabet[i:i+n])     
    start = end     
    end+=n     
    file = open("pythonwrite.txt", 'w')     
    file.write(alphabet)     
    file.close

n=int(input("\n\t\Enter lines to read:")) 
f=open("pjyr.txt","r") 
for i in range(n): 
    print(f.readline())

list=[12, 54, 3, 41, 32, 8, 6, 33]     #5 exp start
list.sort() 
print(list)
print("The second smallest number is:")
print(list[1:2])
print("The second largest number is :") 
print(list[7:8])

list=[1,2,8,3,2,2,2,5,1] 
print("Elements | Frequency") 
print("1|", list.count(1)) 
print("2|", list.count(2)) 
print("3|", list.count(3)) 
print("5|", list.count(5)) 
print("8|", list.count(8))

a = [10,20,30,20,10,50,60,40,80,50,40] 
print(set(a))

list=[1,2,3,4,5,6] 
list.sort(reverse=True) 
print(list)

inventory ={"{gold": 500, "pouch": ["flint", "twine", "gemstone"], "backpack": ["xylophone", "dagger", "bedroll", "bread loaf"]} 
inventory["pocket"]=["seashell", "strange berry", "lint"]
print(inventory)
inventory["backpack"].sort()                         # Exp no 6
print(inventory)
inventory["backpack"].remove("dagger")
inventory["gold" ]=550
print(inventory)

total=0
prices = {"banana" :4, "apple" :2, "orange":1.5, "pear":3} 
stock = {"banana":6, "apple":9, "orange":5, "pear":10} 
for i in prices:
    print(i)
    print("price:%s" %prices[i]) 
    print("stock:%s" %stock[i])
for x in prices:
    money = prices[x]*stock[x]
    total+=money 
print(total)


class Patient:
    def _init_(self, name, age, gender, diagnosis): 
        self.name = name
        self.age = age           #Exp no 7
        self.gender = gender
        self.diagnosis = diagnosis
    
    def display_info(self):
        print("Patient Name:", self.name)
        print("Age:", self.age)
        print("Gender:", self.gender) 
        print("Diagnosis:", self.diagnosis)
        
class Hospital:
    def _init_(self):
        self.patients = []
    def add_patient (self, patient): 
        self.patients.append(patient)
    def display_patients (self):
        print("Patients in the hospital: ") 
        for patient in self.patients:
            patient.display_info()

def main():
    hospital=Hospital()
    patient1=Patient ("john", 35, "Male", "Fever") 
    patient2=Patient("smith", 50, "Male", "chicken pox")
    
    hospital.add_patient (patient1) 
    hospital.add_patient (patient2)
    
    hospital.display_patients()
main()


from PIL import Image, ImageFilter 
image Image.open("lung.jpeg") 
width, height=image.size
#image.show() 
c_h=height/2
c_w=width/2
cropped_image=image.crop ((20,20,c_h,c_w))
cropped_image.show()
rotated_image=image.rotate(145)
rotated_image.show()
resized_image=image.resize((50,70))
resized_image.show()
flip_image=image.transpose(Image.TRANSPOSE)
flip_image.show()
bg_image=image.convert("1")
bg_image.show()
blur_image=image.filter(ImageFilter.GaussianBlur(15))
blur_image.show()
    
    '''
    
    # Print the code to the terminal
    print(f"Here is the code that would go into 'gand.py':\n")
    print(hello_world_code)

# Function to execute when the script is run directly
if __name__ == "__main__":
    print_hello_world_code()
