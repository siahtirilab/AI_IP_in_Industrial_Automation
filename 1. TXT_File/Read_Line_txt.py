
user_line = int(input("Enter the number of lines: "))
with open("sampel.txt","r", encoding="utf-8") as f:
    data = list(f)
    for i in range(0,len(data)):
        if i ==user_line:
            print(data[i])