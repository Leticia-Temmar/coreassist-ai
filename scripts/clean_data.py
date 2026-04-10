import pandas as pd
import random

df = pd.read_csv("employees.csv")

df = df[["DepartmentType", "Title"]]

df = df.rename(columns={
    "DepartmentType": "department",
    "Title": "job_title"
})

df = df.sample(n=200, random_state=42)

first_names = ["Sophie", "Karim", "Lucas", "Emma", "Nina", "Yanis"]
last_names = ["Martin", "Benali", "Dupont", "Durand", "Leroy"]

def generate_full_name():
    return random.choice(first_names) + " " + random.choice(last_names)

def generate_email(full_name):
    return full_name.lower().replace(" ", ".") + "@company.com"

def generate_phone():
    return "06" + "".join([str(random.randint(0, 9)) for _ in range(8)])

df["full_name"] = df.apply(lambda x: generate_full_name(), axis=1)
df["email"] = df["full_name"].apply(generate_email)
df["phone"] = df.apply(lambda x: generate_phone(), axis=1)

df = df[["full_name", "email", "phone", "department", "job_title"]]

df.to_csv("clean_employees.csv", index=False)

print("clean_employees.csv created successfully")