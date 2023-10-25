# Appending the file with new line content using append mode
with open('mydata.txt', 'a') as f:
    # Use a function called write to add new line to the file
    f.write('\nsensor02,50,60,70,80')