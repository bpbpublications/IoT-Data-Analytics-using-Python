str1 = "Hello, I live in an AI world!" # Creating a string variable
str2 = "I am Robot!" # Creating another string variable
print("Concatenation of two string :", str1 + " "+ str2)
print("Accessing specific characters in a string: ", str1[0])  # Output will be H
print("str1[-1]: ", str1[-1])  # Output: !
print("Extracting substring using slicing with starting position and length of extraction", str1[0:5])  # Output: Hello
print("Slicing string from 7th character onwards: ", str1[7:])  # Output: I live in an AI world!
print("String Repetition: ", str1 * 2)  # Hello, I live in an AI world!Hello, I live in an AI world!
print("Finding length of the string: ", len(str1))  # Output: 29, includes space between letters.
print("Making the string to all lower case: ", str1.lower())  # Output: hello, i live in an ai world!
print("Making the string to all upper case: ", str1.upper())  # Output: HELLO, I LIVE IN AN AI WORLD!
print("Making initial letter capitalized: ", str1.capitalize())  # Output: Hello, i live in an ai world!
print("Counting specific letter in a string 'n': ", str1.count('n'))  # Output: 2
print("Find 'AI': ", str1.find('AI'))  # Output: 20
print("Replace 'AI' with 'Artificial Intelligence': ", str1.replace('AI', 'Artificial Intelligence'))  # Output:  Hello, I live in an Artificial Intelligence world!
