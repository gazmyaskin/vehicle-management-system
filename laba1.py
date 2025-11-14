import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import os


# Собственное исключение
class VehicleError(Exception):
    """Пользовательское исключение для ошибок транспортных средств"""
    pass


class Vehicle(ABC):
    """Абстрактный базовый класс для транспортных средств"""

    def __init__(self, brand: str, model: str, year: int, color: str, price: float):
        self._brand = brand
        self._model = model
        self._year = year
        self._color = color
        self._price = price

    @abstractmethod
    def calculate_tax(self) -> float:
        """Рассчитать налог на транспортное средство"""
        pass

    @abstractmethod
    def get_vehicle_type(self) -> str:
        """Получить тип транспортного средства"""
        pass

    def get_age(self) -> int:
        """Получить возраст транспортного средства"""
        current_year = datetime.now().year
        return current_year - self._year

    def to_dict(self) -> Dict:
        """Преобразовать объект в словарь"""
        return {
            'type': self.get_vehicle_type(),
            'brand': self._brand,
            'model': self._model,
            'year': self._year,
            'color': self._color,
            'price': self._price
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Vehicle':
        """Создать объект из словаря"""
        vehicle_type = data.get('type', '')
        if vehicle_type == 'Car':
            return Car(data['brand'], data['model'], data['year'],
                       data['color'], data['price'], data.get('seats', 5))
        elif vehicle_type == 'Motorcycle':
            return Motorcycle(data['brand'], data['model'], data['year'],
                              data['color'], data['price'], data.get('engine_cc', 0))
        elif vehicle_type == 'Truck':
            return Truck(data['brand'], data['model'], data['year'],
                         data['color'], data['price'], data.get('load_capacity', 0))
        elif vehicle_type == 'Bus':
            return Bus(data['brand'], data['model'], data['year'],
                       data['color'], data['price'], data.get('passenger_capacity', 0))
        else:
            raise VehicleError(f"Неизвестный тип транспортного средства: {vehicle_type}")

    # Геттеры и сеттеры с проверкой исключений
    @property
    def brand(self) -> str:
        return self._brand

    @brand.setter
    def brand(self, value: str):
        if not value or not isinstance(value, str):
            raise VehicleError("Марка должна быть непустой строкой")
        self._brand = value

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        if not value or not isinstance(value, str):
            raise VehicleError("Модель должна быть непустой строкой")
        self._model = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int):
        current_year = datetime.now().year
        if not isinstance(value, int) or value < 1900 or value > current_year:
            raise VehicleError(f"Год должен быть между 1900 и {current_year}")
        self._year = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if not isinstance(value, (int, float)) or value < 0:
            raise VehicleError("Цена должна быть положительным числом")
        self._price = float(value)

    def __str__(self) -> str:
        return f"{self.get_vehicle_type()} {self._brand} {self._model} ({self._year})"


class Car(Vehicle):
    """Класс для легковых автомобилей"""

    def __init__(self, brand: str, model: str, year: int, color: str,
                 price: float, seats: int = 5):
        super().__init__(brand, model, year, color, price)
        self.seats = seats

    def calculate_tax(self) -> float:
        """Рассчитать налог для автомобиля"""
        base_tax = self._price * 0.02
        age_multiplier = max(0.1, 1 - self.get_age() * 0.05)
        return base_tax * age_multiplier

    def get_vehicle_type(self) -> str:
        return "Car"

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['seats'] = self.seats
        return data


class Motorcycle(Vehicle):
    """Класс для мотоциклов"""

    def __init__(self, brand: str, model: str, year: int, color: str,
                 price: float, engine_cc: int):
        super().__init__(brand, model, year, color, price)
        self.engine_cc = engine_cc

    def calculate_tax(self) -> float:
        """Рассчитать налог для мотоцикла"""
        base_tax = self._price * 0.015
        engine_tax = self.engine_cc * 0.1
        return base_tax + engine_tax

    def get_vehicle_type(self) -> str:
        return "Motorcycle"

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['engine_cc'] = self.engine_cc
        return data


class Truck(Vehicle):
    """Класс для грузовиков"""

    def __init__(self, brand: str, model: str, year: int, color: str,
                 price: float, load_capacity: float):
        super().__init__(brand, model, year, color, price)
        self.load_capacity = load_capacity

    def calculate_tax(self) -> float:
        """Рассчитать налог для грузовика"""
        base_tax = self._price * 0.025
        capacity_tax = self.load_capacity * 50
        return base_tax + capacity_tax

    def get_vehicle_type(self) -> str:
        return "Truck"

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['load_capacity'] = self.load_capacity
        return data


class Bus(Vehicle):
    """Класс для автобусов"""

    def __init__(self, brand: str, model: str, year: int, color: str,
                 price: float, passenger_capacity: int):
        super().__init__(brand, model, year, color, price)
        self.passenger_capacity = passenger_capacity

    def calculate_tax(self) -> float:
        """Рассчитать налог для автобуса"""
        base_tax = self._price * 0.02
        passenger_tax = self.passenger_capacity * 100
        return base_tax + passenger_tax

    def get_vehicle_type(self) -> str:
        return "Bus"

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['passenger_capacity'] = self.passenger_capacity
        return data


class VehicleManager:
    """Менеджер для работы с транспортными средствами"""

    def __init__(self):
        self._vehicles: List[Vehicle] = []

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Добавить транспортное средство"""
        self._vehicles.append(vehicle)

    def remove_vehicle(self, index: int) -> bool:
        """Удалить транспортное средство по индексу"""
        try:
            if 0 <= index < len(self._vehicles):
                del self._vehicles[index]
                return True
            return False
        except (IndexError, TypeError):
            raise VehicleError("Неверный индекс для удаления")

    def get_vehicle(self, index: int) -> Optional[Vehicle]:
        """Получить транспортное средство по индексу"""
        try:
            if 0 <= index < len(self._vehicles):
                return self._vehicles[index]
            return None
        except (IndexError, TypeError):
            raise VehicleError("Неверный индекс")

    def update_vehicle(self, index: int, **kwargs) -> bool:
        """Обновить данные транспортного средства"""
        try:
            vehicle = self.get_vehicle(index)
            if vehicle:
                for key, value in kwargs.items():
                    if hasattr(vehicle, key):
                        setattr(vehicle, key, value)
                return True
            return False
        except Exception as e:
            raise VehicleError(f"Ошибка при обновлении: {str(e)}")

    def get_all_vehicles(self) -> List[Vehicle]:
        """Получить все транспортные средства"""
        return self._vehicles.copy()

    def get_vehicles_by_type(self, vehicle_type: str) -> List[Vehicle]:
        """Получить транспортные средства по типу"""
        return [v for v in self._vehicles if v.get_vehicle_type() == vehicle_type]

    def get_total_value(self) -> float:
        """Получить общую стоимость всех транспортных средств"""
        return sum(vehicle.price for vehicle in self._vehicles)

    def save_to_json(self, filename: str) -> None:
        """Сохранить данные в JSON файл"""
        try:
            data = {
                'vehicles': [vehicle.to_dict() for vehicle in self._vehicles],
                'total_count': len(self._vehicles),
                'total_value': self.get_total_value(),
                'save_date': datetime.now().isoformat()
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Данные успешно сохранены в {filename}")
        except Exception as e:
            raise VehicleError(f"Ошибка при сохранении в JSON: {str(e)}")

    def load_from_json(self, filename: str) -> None:
        """Загрузить данные из JSON файла"""
        try:
            if not os.path.exists(filename):
                raise VehicleError(f"Файл {filename} не существует")

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._vehicles.clear()
            for vehicle_data in data.get('vehicles', []):
                vehicle = Vehicle.from_dict(vehicle_data)
                self._vehicles.append(vehicle)

            print(f"Данные успешно загружены из {filename}")
        except Exception as e:
            raise VehicleError(f"Ошибка при загрузке из JSON: {str(e)}")

    def save_to_xml(self, filename: str) -> None:
        """Сохранить данные в XML файл"""
        try:
            root = ET.Element('VehicleCollection')
            root.set('total_count', str(len(self._vehicles)))
            root.set('total_value', str(self.get_total_value()))
            root.set('save_date', datetime.now().isoformat())

            for vehicle in self._vehicles:
                vehicle_elem = ET.SubElement(root, 'Vehicle')
                vehicle_elem.set('type', vehicle.get_vehicle_type())

                ET.SubElement(vehicle_elem, 'Brand').text = vehicle.brand
                ET.SubElement(vehicle_elem, 'Model').text = vehicle.model
                ET.SubElement(vehicle_elem, 'Year').text = str(vehicle.year)
                ET.SubElement(vehicle_elem, 'Color').text = vehicle._color
                ET.SubElement(vehicle_elem, 'Price').text = str(vehicle.price)

                # Добавляем специфические поля
                if isinstance(vehicle, Car):
                    ET.SubElement(vehicle_elem, 'Seats').text = str(vehicle.seats)
                elif isinstance(vehicle, Motorcycle):
                    ET.SubElement(vehicle_elem, 'EngineCC').text = str(vehicle.engine_cc)
                elif isinstance(vehicle, Truck):
                    ET.SubElement(vehicle_elem, 'LoadCapacity').text = str(vehicle.load_capacity)
                elif isinstance(vehicle, Bus):
                    ET.SubElement(vehicle_elem, 'PassengerCapacity').text = str(vehicle.passenger_capacity)

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
            print(f"Данные успешно сохранены в {filename}")
        except Exception as e:
            raise VehicleError(f"Ошибка при сохранении в XML: {str(e)}")

    def load_from_xml(self, filename: str) -> None:
        """Загрузить данные из XML файла"""
        try:
            if not os.path.exists(filename):
                raise VehicleError(f"Файл {filename} не существует")

            tree = ET.parse(filename)
            root = tree.getroot()

            self._vehicles.clear()

            for vehicle_elem in root.findall('Vehicle'):
                vehicle_type = vehicle_elem.get('type')
                brand = vehicle_elem.find('Brand').text
                model = vehicle_elem.find('Model').text
                year = int(vehicle_elem.find('Year').text)
                color = vehicle_elem.find('Color').text
                price = float(vehicle_elem.find('Price').text)

                if vehicle_type == 'Car':
                    seats = int(vehicle_elem.find('Seats').text)
                    vehicle = Car(brand, model, year, color, price, seats)
                elif vehicle_type == 'Motorcycle':
                    engine_cc = int(vehicle_elem.find('EngineCC').text)
                    vehicle = Motorcycle(brand, model, year, color, price, engine_cc)
                elif vehicle_type == 'Truck':
                    load_capacity = float(vehicle_elem.find('LoadCapacity').text)
                    vehicle = Truck(brand, model, year, color, price, load_capacity)
                elif vehicle_type == 'Bus':
                    passenger_capacity = int(vehicle_elem.find('PassengerCapacity').text)
                    vehicle = Bus(brand, model, year, color, price, passenger_capacity)
                else:
                    continue

                self._vehicles.append(vehicle)

            print(f"Данные успешно загружены из {filename}")
        except Exception as e:
            raise VehicleError(f"Ошибка при загрузке из XML: {str(e)}")


def create_sample_data() -> VehicleManager:
    """Создать пример данных для тестирования"""
    manager = VehicleManager()

    # Добавляем примеры транспортных средств
    manager.add_vehicle(Car("Toyota", "Camry", 2020, "Black", 25000, 5))
    manager.add_vehicle(Car("Honda", "Civic", 2018, "White", 20000, 5))
    manager.add_vehicle(Motorcycle("Yamaha", "YZF-R3", 2021, "Blue", 5000, 321))
    manager.add_vehicle(Truck("Volvo", "FH16", 2019, "Red", 80000, 20000))
    manager.add_vehicle(Bus("Mercedes", "Tourismo", 2022, "Silver", 120000, 50))

    return manager


def display_menu():
    """Отобразить меню"""
    print("\n=== Система управления транспортными средствами ===")
    print("1. Показать все транспортные средства")
    print("2. Добавить транспортное средство")
    print("3. Удалить транспортное средство")
    print("4. Обновить транспортное средство")
    print("5. Сохранить в JSON")
    print("6. Загрузить из JSON")
    print("7. Сохранить в XML")
    print("8. Загрузить из XML")
    print("9. Показать статистику")
    print("0. Выход")


def get_vehicle_input():
    """Получить данные транспортного средства от пользователя"""
    print("\nВыберите тип транспортного средства:")
    print("1. Легковой автомобиль")
    print("2. Мотоцикл")
    print("3. Грузовик")
    print("4. Автобус")

    try:
        choice = int(input("Ваш выбор: "))

        brand = input("Марка: ")
        model = input("Модель: ")
        year = int(input("Год: "))
        color = input("Цвет: ")
        price = float(input("Цена: "))

        if choice == 1:
            seats = int(input("Количество мест: "))
            return Car(brand, model, year, color, price, seats)
        elif choice == 2:
            engine_cc = int(input("Объем двигателя (cc): "))
            return Motorcycle(brand, model, year, color, price, engine_cc)
        elif choice == 3:
            load_capacity = float(input("Грузоподъемность (кг): "))
            return Truck(brand, model, year, color, price, load_capacity)
        elif choice == 4:
            passenger_capacity = int(input("Вместимость пассажиров: "))
            return Bus(brand, model, year, color, price, passenger_capacity)
        else:
            raise VehicleError("Неверный выбор типа транспортного средства")
    except ValueError as e:
        raise VehicleError("Ошибка ввода данных: убедитесь, что числовые поля заполнены правильно")


def test_exceptions():
    """Тестирование обработки исключений"""
    print("\n" + "=" * 60)
    print(" ТЕСТИРОВАНИЕ ОБРАБОТКИ ИСКЛЮЧЕНИЙ")
    print("=" * 60)

    try:
        print("Попытка создать автомобиль  с некорректным годом...")
        Car("Toyota", "Camry", 1800, "Black", 25000, 5)
    except VehicleError as e:
        print(f" Поймана ошибка: {e}")

    try:
        print("Попытка создать мотоцикл  с отрицательной ценой...")
        Motorcycle("Yamaha", "R3", 2021, "Blue", -5000, 321)
    except VehicleError as e:
        print(f" Поймана ошибка: {e}")

    try:
        print("Попытка создать автомобиль  с пустой маркой...")
        Car("", "Model", 2020, "Red", 20000, 5)
    except VehicleError as e:
        print(f" Поймана ошибка: {e}")

    print("=" * 60)
    print(" Все исключения успешно обработаны! Программа продолжает работу.")
    print("=" * 60)

def main():
    """Основная функция программы"""
    manager = create_sample_data()

    test_exceptions()

    while True:
        try:
            display_menu()
            choice = input("\nВыберите действие: ")

            if choice == '1':
                # Показать все транспортные средства
                vehicles = manager.get_all_vehicles()
                if not vehicles:
                    print("Нет транспортных средств")
                else:
                    print("\nСписок транспортных средств:")
                    for i, vehicle in enumerate(vehicles):
                        tax = vehicle.calculate_tax()
                        print(f"{i}. {vehicle} | Цена: ${vehicle.price:.2f} | Налог: ${tax:.2f}")

            elif choice == '2':
                # Добавить транспортное средство
                try:
                    vehicle = get_vehicle_input()
                    manager.add_vehicle(vehicle)
                    print("Транспортное средство успешно добавлено!")
                except VehicleError as e:
                    print(f"Ошибка: {e}")

            elif choice == '3':
                # Удалить транспортное средство
                try:
                    index = int(input("Введите индекс для удаления: "))
                    if manager.remove_vehicle(index):
                        print("Транспортное средство успешно удалено!")
                    else:
                        print("Неверный индекс")
                except (ValueError, VehicleError) as e:
                    print(f"Ошибка: {e}")

            elif choice == '4':
                # Обновить транспортное средство
                try:
                    index = int(input("Введите индекс для обновления: "))
                    vehicle = manager.get_vehicle(index)
                    if vehicle:
                        print(f"Обновление: {vehicle}")
                        # Здесь можно добавить логику для обновления конкретных полей
                        new_price = float(input("Новая цена: "))
                        manager.update_vehicle(index, price=new_price)
                        print("Транспортное средство успешно обновлено!")
                    else:
                        print("Неверный индекс")
                except (ValueError, VehicleError) as e:
                    print(f"Ошибка: {e}")

            elif choice == '5':
                # Сохранить в JSON
                try:
                    filename = input("Имя файла JSON (по умолчанию: vehicles.json): ") or "vehicles.json"
                    manager.save_to_json(filename)
                except VehicleError as e:
                    print(f"Ошибка: {e}")

            elif choice == '6':
                # Загрузить из JSON
                try:
                    filename = input("Имя файла JSON (по умолчанию: vehicles.json): ") or "vehicles.json"
                    manager.load_from_json(filename)
                except VehicleError as e:
                    print(f"Ошибка: {e}")

            elif choice == '7':
                # Сохранить в XML
                try:
                    filename = input("Имя файла XML (по умолчанию: vehicles.xml): ") or "vehicles.xml"
                    manager.save_to_xml(filename)
                except VehicleError as e:
                    print(f"Ошибка: {e}")

            elif choice == '8':
                # Загрузить из XML
                try:
                    filename = input("Имя файла XML (по умолчанию: vehicles.xml): ") or "vehicles.xml"
                    manager.load_from_xml(filename)
                except VehicleError as e:
                    print(f"Ошибка: {e}")

            elif choice == '9':
                # Показать статистику
                vehicles = manager.get_all_vehicles()
                print(f"\nСтатистика:")
                print(f"Всего транспортных средств: {len(vehicles)}")
                print(f"Общая стоимость: ${manager.get_total_value():.2f}")

                types_count = {}
                for vehicle in vehicles:
                    v_type = vehicle.get_vehicle_type()
                    types_count[v_type] = types_count.get(v_type, 0) + 1

                print("По типам:")
                for v_type, count in types_count.items():
                    print(f"  {v_type}: {count}")

            elif choice == '0':
                print("Выход из программы...")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()