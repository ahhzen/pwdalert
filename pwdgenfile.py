import hashlib
import projectinfo as pinfo
from pathlib import Path

FILENAME = pinfo.FILENAME 

def get_pwd():
	pwdlist = []
	while(True):
		try:
			password = input("Enter a password to be hashed (CTRL+C to exit): ")
			if len(password) <= 0:
				raise Exception("IGNORE") 
			pwdlist.append(hashlib.sha1(password.encode("utf-8")).hexdigest().upper()) 
		except KeyboardInterrupt:
			break
		except:
			print("Password cannot be empty!")

	return pwdlist

def store_pwd(pwdlist):
	if len(pwdlist) > 0:
		with open(FILENAME, "a") as file:
			counter = 0
			for i in pwdlist:
				file.write(i + "\n")
				counter += 1
			file.close()
			fullpath = Path(Path().cwd(), FILENAME) 
			print(f"You have entered {counter} password(s) - hashed and store in {fullpath}")

if __name__ == "__main__":
	store_pwd(get_pwd())