from src.promotion import Promotion

def test_promotion_once():
    promo = Promotion("NEWBEE20")

    price = promo.apply(100)
    assert price == 80

    price2 = promo.apply(100)
    assert price2 == 100  # 第二次无效S