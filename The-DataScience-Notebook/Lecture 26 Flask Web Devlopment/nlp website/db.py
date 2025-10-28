import json
import os


class Database:

    def insert(self, name, email, password):
        # Define the path of the file
        file_path = os.path.join(os.getcwd(), "user.json")

        # Check if the file exists
        if not os.path.exists(file_path):
            users = {}
        else:
            with open(file_path, "r") as f:
                users = json.load(f)

        if email in users:
            return 0  # Email already exists
        else:
            users[email] = [name, password]

        # Write the updated data to the file
        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)
            return 1  # Registration successful

    def search(self, email, password):
        with open("user.json", "r") as f:
            users = json.load(f)

            if email in users:
                if users[email][1] == password:
                    return 1  # Login successful
                else:
                    return 0
            else:
                return 0