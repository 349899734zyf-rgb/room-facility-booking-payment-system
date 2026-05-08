class Order:

    def __init__(
            self,
            order_id,
            booking,
            price,
            payment_method
    ):

        self.__order_id = order_id
        self.__booking = booking
        self.__price = price
        self.__promo_discount = 0
        self.__final_price = price
        self.__payment_method = payment_method

    def get_booking(self):
        return self.__booking

    def get_payment_method(self):
        return self.__payment_method

    def get_final_price(self):
        return self.__final_price

    def set_promo_discount(self, discount):

        self.__promo_discount = discount

        self.__final_price = max(
            0,
            self.__price - discount
        )