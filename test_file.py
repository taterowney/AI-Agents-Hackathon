
```
# greet_friends.py

class Friend:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

def send_greeting(friend):
    print(f"Happy Birthday to our dear friend {friend.name}!")

# Define friends with their birthdays
friends = [
    Friend("John", "1990-02-12"),
    Friend("Alice", "1995-08-25"),
    Friend("Bob", "1980-01-01")
]

# Simulate today's date (replace with current date for real usage)
from datetime import datetime
today = datetime(2023, 2, 12)

# Check if today is a friend's birthday and send greeting
for friend in friends:
    birthday_date = datetime.strptime(friend.birthday, "%Y-%m-%d")
    if (birthday_date.month == today.month) and (birthday_date.day == today.day):
        send_greeting(friend)
```
