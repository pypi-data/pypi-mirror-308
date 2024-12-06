from textdrip.api import TextdripAPI


obj=TextdripAPI()

email = input('Enter your email :')
password = input('Enter your email :')

response=obj.login(email,password)
print(response)