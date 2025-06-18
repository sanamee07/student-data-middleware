from middleware.publisher.send_to_queue import publish_message
from middleware.config import QUEUE_HIS

class HisCli:
    PREDEFINED_STUDENTS = [
         {
            "id": "1001",
            "name": "ZA",
            "email": "zaza.mueller@example.de",
            "date_of_birth": "2000-05-15",
            "enrollment_date": "2019-10-01",
            "programs": [
                {"name": "Wirtschaftsinformatik", "start_date": "2019-10-01", "credits": 60},
                {"name": "Informatik",            "start_date": "2021-03-01", "credits": 20}
            ]
        },
        {
            "id": "1002",
            "name": "Bob Schmidt",
            "email": "bob.schmidt@example.de",
            "date_of_birth": "1999-11-22",
            "enrollment_date": "2018-10-01",
            "programs": [
                {"name": "Informatik", "start_date": "2018-10-01", "credits": 75}
            ]
        },
        {
            "id": "1003",
            "name": "Clara Lehmann",
            "email": "clara.lehmann@example.de",
            "date_of_birth": "2001-01-30",
            "enrollment_date": "2020-10-01",
            "programs": [
                {"name": "Medieninformatik", "start_date": "2020-10-01", "credits": 45},
                {"name": "Data Science",     "start_date": "2022-04-01", "credits": 10}
            ]
        },
        {
            "id": "1004",
            "name": "David Meier",
            "email": "david.meier@example.de",
            "date_of_birth": "1998-07-12",
            "enrollment_date": "2017-10-01",
            "programs": [
                {"name": "Informatik",        "start_date": "2017-10-01", "credits": 90},
                {"name": "Wirtschaftsinformatik", "start_date": "2021-10-01", "credits": 30}
            ]
        },
        {
            "id": "1005",
            "name": "Eva Fischer",
            "email": "eva.fischer@example.de",
            "date_of_birth": "2002-03-05",
            "enrollment_date": "2021-10-01",
            "programs": [
                {"name": "Software Engineering", "start_date": "2021-10-01", "credits": 50}
            ]
        },
    ]

    def __init__(self):
        pass

    def send_student(self, data: dict):
        publish_message(QUEUE_HIS, data)
        print(f"✅ Gesendet: {data['id']} – {data['name']}")

    def send_predefined(self):
        for student in self.PREDEFINED_STUDENTS:
            self.send_student(student)

    def manual_entry(self):
        data = {}
        data['id'] = input("ID: ")
        data['name'] = input("Name: ")
        data['email'] = input("Email: ")
        data['date_of_birth'] = input("Geburtsdatum (YYYY-MM-DD): ")
        data['enrollment_date'] = input("Einschreibedatum (YYYY-MM-DD): ")
        programs = input("Studiengänge (kommagetrennt): ")
        data['programs'] = [p.strip() for p in programs.split(',')] if programs else []
        self.send_student(data)

    def main_menu(self):
        while True:
            print("\nWas möchtest du tun?")
            print("1) Vordefinierte Daten senden")
            print("2) Manuellen Datensatz eingeben und senden")
            print("0) Beenden")
            choice = input("Auswahl (0/1/2): ")
            if choice == '1':
                self.send_predefined()
            elif choice == '2':
                self.manual_entry()
            elif choice == '0':
                print("Bye!")
                break
            else:
                print("Ungültige Auswahl. Bitte 0, 1 oder 2 eingeben.")
