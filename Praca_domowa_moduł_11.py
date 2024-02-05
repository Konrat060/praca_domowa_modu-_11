from datetime import datetime

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def validate(self, value):
        return True


class Phone(Field):
    def validate(self, value):
        return all(char.isdigit() or char in "+-()" for char in value)


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class Name(Field):
    def validate(self, value):
        return all(char.isalpha() or char in " -" for char in value)


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone) if phone else None
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if not self.birthday:
            return None
        now = datetime.now()
        current_year = now.year
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d')
        birthday = birthday.replace(year=current_year)
        if birthday < now:
            birthday = birthday.replace(year=current_year + 1)
        return (birthday - now).days


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def __iter__(self):
        return iter(self.records)

    def paginate_records(self, page_size):
        return [self.records[i:i + page_size] for i in range(0, len(self.records), page_size)]


def main():
    address_book = AddressBook()
    record1 = Record("John Johnson", "+48 123 456 789", "1980-01-01")
    record2 = Record("Andrew Tim", "+48 123 456 789", "1980-05-15")
    address_book.add_record(record1)
    address_book.add_record(record2)

    page_size = 1
    for page, records in enumerate(address_book.paginate_records(page_size)):
        print(f"Page {page + 1}:")
        for record in records:
            print(f"{record.name}: Phone - {record.phone}, Birthday - {record.birthday}, "
                  f"Days to birthday - {record.days_to_birthday()}")


if __name__ == '__main__':
    main()
