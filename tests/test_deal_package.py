from src.entities.deal_package import DealPackage


def test_deal_package_stores_package_details():
    deal_package = DealPackage("DP001", 100.0, 12.0)

    assert deal_package.get_package_id() == "DP001"
    assert deal_package.get_price() == 100.0
    assert deal_package.get_hours() == 12.0
