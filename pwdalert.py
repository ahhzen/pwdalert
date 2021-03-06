import requests
import hashlib
import sys
import projectinfo as pinfo
import smtplib
import credential
from email.message import EmailMessage
from string import Template
from pathlib import Path

pwd_sha1 = ""
pwd_sha1_5 = ""

def send_email(detail):

    email = EmailMessage()
    email["from"] = "PiZen"
    email["to"] = ["dummy@yahoo.com", "dummy@gmail.com"]
    email["subject"] = "You are PWNED!"

    template = populate_template(detail)
    email.set_content(template,"HTML")

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(credential.username, credential.password)
        smtp.send_message(email)
        print("PWNED! Alert has been sent")

def populate_template(detail):
    path_template = Path(get_project_path(), pinfo.TEMPLATE)

    template_field = {"qty": detail}

    template = Template(path_template.read_text())
    template = template.substitute(template_field)
    return template

def request_api_data(query):
    url = "https://api.pwnedpasswords.com/range/" + query
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f"Error fetch : {res.status_code}, check again")
    else:
        return res

def get_password_leak_count(response, tail):
    hashes = (line.split(":") for line in response.text.splitlines() )

    for h, count in hashes:
        if tail == h:
            return count
    return 0

def pwned_api_check(sha1password):
    head, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(head)
    leakcount = int(get_password_leak_count(response, tail))
    return leakcount


def main():
    try:
        pwdlist = read_pwd_file()
        pwned = 0
        for pwd in pwdlist:
            count = pwned_api_check(pwd)
            if count > 0:
                print(f"Your password '{pwd}' has been used {count} before")
                pwned += 1
            else:
                print(f"Your password '{pwd}' seems ok for now. Check again sometime later")

        send_alert(pwned)
    except Exception as err:
        print(f"Something went wrong...{err}")



def send_alert(pwned):
    if pwned > 0:
        send_email(pwned)
    else:
        print("Everything's OK. No alert sent.")

def get_project_path():
    fullpath = Path().home()
    for p in pinfo.PROJECT_DIR:
        fullpath = Path(fullpath, p)
    return fullpath

def read_pwd_file():
    outlist = []

    fullpath = Path(get_project_path(), pinfo.FILENAME)

    try:
        with open(fullpath, "r") as file:
            pwdlist = file.readlines()
            for line in pwdlist:
                line = line.rstrip("\n")
                outlist.append(line)

        return outlist
    except:
        raise Exception(f"{pinfo.FILENAME} not exists".upper())

if __name__ == "__main__":
    sys.exit(main())




