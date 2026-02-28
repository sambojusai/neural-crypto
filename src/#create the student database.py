#create the student database

#key elements name,age,clg,branch,rollno,year,type,gender,fname,mname,address,marks

class person:
   def __init__(self,name,age,clg,branch,rollno,year,type,gender,fname,mname,address,marks):
        self.name=name
        self.age=age
        self.clg=clg
        self.branch=branch
        self.rollno=rollno
        self.year=year
        self.year=year
        self.type=type
        self.gender=gender
        self.fname=fname
        self.mname=mname
        self.address=address
        self.marks=marks
p1=person("Raghu",22,"CJITS","ECE","22681A0407","4th year","CONVENOR","MALE","YELLAIAH","MANEMMA","JANGAON","7.5CGPA")

X1=str(input("Enter your name: "))
X2=str(input("Enter your age: "))
X3=str(input("Enter your college: "))
X4=str(input("Enter your department: "))
X5=str(input("Enter your roll no: "))
X6=str(input("Enter your  year: "))
X7=str(input("Enter your seat type: "))
X8=str(input("Enter your gender: "))
X9=str(input("Enter your father name: "))
X10=str(input("Enter your mother name: "))
X11=str(input("Enter your address: "))
X12=str(input("Enter your marks: "))

print("NAME:",X1)
print("AGE:",X2)
print("COLLEGE:",X3)
print("DEPARTMENT:",X4)
print("ROLL NO:",X5)
print("YEAR:",X6)
print("SEAT TYPE:",X7)
print("GENDER:",X8)
print("FATHER'S NAME:",X9)
print("MOTHER'S NAME:",X10)
print("ADDRESS:",X11)
print("CGPA:",X12)