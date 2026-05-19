class DealPackage:

    def __init__(
            self,
            package_id: str,
            price: float,
            hours: float
    ) -> None:

        self.__package_id = package_id
        self.__price = price
        self.__hours = hours

    def get_package_id(self) -> str:
        return self.__package_id

    def get_price(self) -> float:
        return self.__price

    def get_hours(self) -> float:
        return self.__hours

    def set_package_id(self, package_id: str) -> None:
        self.__package_id = package_id

    def set_price(self, price: float) -> None:
        self.__price = price

    def set_hours(self, hours: float) -> None:
        self.__hours = hours
