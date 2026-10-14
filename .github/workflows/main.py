import os

name = os.environ.get("NAME", "мир")
print(f"Привет, {name}!")
