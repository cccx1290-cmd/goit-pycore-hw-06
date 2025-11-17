from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Обов'язкове поле"""
    pass


class Phone(Field):
    """10 цифр"""

    def __init__(self, value: str):
        self._validate(value)
        super().__init__(value)

    @staticmethod
    def _validate(value: str) -> None:
        # Дозволяємо тільки рівно 10 цифр
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")

    @Field.value.setter
    def value(self, new_value: str) -> None:
        self._validate(new_value)
        self._value = new_value

    @property
    def value(self) -> str:
        return self._value


class Record:
    """
    Запис у книзі контактів: ім'я + список телефонів.
    """

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Додати новий телефон до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видалити телефон за значенням."""
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінити існуючий телефон на новий.
        """
        phone_obj = self.find_phone(old_phone)
        if not phone_obj:
            raise ValueError("Old phone number not found.")
        # Валідація всередині Phone
        phone_obj.value = new_phone

    def find_phone(self, phone: str) -> Phone | None:
        """Пошук телефону в записі."""
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        """Додати запис до книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Знайти запис за ім'ям."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видалити запис за ім'ям."""
        if name in self.data:
            del self.data[name]
