from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if new_value:
            self.__value = new_value

    def __str__(self):
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            self._value = datetime.strptime(new_value, '%d/%m/%Y').date()
        except ValueError:
            raise ValueError("Date is not valid")


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        new_value = str(new_value)
        if new_value.isdigit() and len(new_value) == 10:
            self.__value = new_value
        else:
            raise ValueError("Number not valid")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday:Birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        if phone.value not in (p.value for p in self.phones):
            self.phones.append(phone)
            return f"Phone {phone} added to contact {self.name}."
        return f"{phone} is in contact {self.name}."

    def edit_phone(self, old_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if old_phone.value == phone.value:
                self.phones[index] = new_phone
                return f"Old phone {old_phone} is changed to new phone {new_phone}."

        return f"{old_phone} is not present in contact {self.name}."

    def days_to_birthday(self):
        current_day = datetime.now()
        if self.birthday and current_day.month == self.birthday.value.month and current_day.day == self.birthday.value.day:
            return f"Happy birthday to {self.name}."

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f'Contact {record}  added successfully.'

    def __iter__(self):
        self.current_record = 0
        return self

    def __next__(self):
        if self.current_record < len(self.data):
            self.current_record += 1
            return self.current_record
        else:
            raise StopIteration

    def save_to_file(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def read_from_file(self,filename):
        try:
            with open(filename, "rb") as f:
                self.data = pickle.load(f)
        except (FileNotFoundError,EOFError):
            self.data = {}
    
    def search_contact(self, search_item):
        result = []
        for record in self.data.values():
            if search_item.lower() in str(record).lower():
                result.append(record)

        return "\n".join(str(rec) for rec in result) if result else "Contact not found"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
