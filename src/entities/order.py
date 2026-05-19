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
        self.__promo_code_used = None

    def get_booking(self):
        return self.__booking

    def get_order_id(self):
        return self.__order_id

    def get_price(self):
        return self.__price

    def get_promo_discount(self):
        return self.__promo_discount

    def get_payment_method(self):
        return self.__payment_method

    def get_final_price(self):
        return self.__final_price

    def get_promo_code_used(self):
        return self.__promo_code_used

    def set_promo_discount(self, discount):

        self.__promo_discount = discount

        self.__final_price = max(
            0,
            self.__price - discount
        )

    def set_payment_method(self, method):

        self.__payment_method = method

    def set_promo_code_used(self, code):

        self.__promo_code_used = code

    def calculate_final_price(self):

        self.__final_price = max(
            0,
            self.__price - self.__promo_discount
        )

        return self.__final_price
