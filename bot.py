from classes import AddressBook, Name, Phone, Record, Birthday


address_book = AddressBook()


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input. Please enter a valid name and phone number"
        except IndexError:
            return "Invalid input. please try again"
    return wrapper


@handle_errors
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2]) if len(args) > 2 else None
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone, birthday)
    address_book.add_record(rec)
    return "Contact added successfully."


@handle_errors
def greeting(*text):
    return "How can I help you?"


@handle_errors
def exit_command(*args):
    return "See you soon"


@handle_errors
def change(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.edit_phone(old_phone, new_phone)

    return f"No contact {name} in addressbook."


@handle_errors
def phone(*args):
    name = Name(args[0])
    if str(name) in address_book.data:
        contact = address_book.data[str(name)]
        phones_str = ', '.join(str(phone) for phone in contact.phones)
        return f"Phone numbers for {name}: {phones_str}"
    return "Contact not found"


@handle_errors
def find_command(*args):
    if len(args[0]) < 3:
        return "Enter at leaset three characters to seartch"
    return address_book.search_contact(args[0])


@handle_errors
def show_all(*args):
    return address_book


@handle_errors
def birthday_greeting(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        greeting = rec.days_to_birthday()
        if greeting:
           return greeting
        else:
           return f"No  birthday today for {name}"
        
    else:
       return f"No contact with name{name} found"

@handle_errors
def no_command(*args):
    return "Unknown command"


COMMANDS = {add: ("add",),
            change: ("change",),
            phone: ("phone",),
            show_all: ("show all",),
            greeting: ("hello", "hi"),
            exit_command: ("finish", "exit","end"),
            find_command: ('search', 'find',),
            birthday_greeting: ("birthday",),
            }


def parser(text: str) -> tuple[callable, tuple[str] | None]:
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data

    return no_command, []


def main():
    try:
        address_book.read_from_file("Address_book")

    except FileNotFoundError:
        print("File not found. Start the address_book")

    while True:
        user_input = input(">>>>")
        command, data = parser(user_input)
        result = command(*data)
        print(result)

        if command == exit_command:
            address_book.save_to_file("Address_book")
            break


if __name__ == "__main__":
    main()
