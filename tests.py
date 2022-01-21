import unittest
from core import *


class TestCore(unittest.TestCase):
    def test_get_user_or_error(self):
        id = 455788012
        user = User.get(id=id)
        self.assertEqual(get_user_or_error(id), user)
        self.assertEqual(get_user_or_error(True), False)
        self.assertEqual(get_user_or_error('string'), False)
        self.assertEqual(get_user_or_error(f'{id}'), user)

    def test_get_profile(self):
        id = 455788012
        user = User.get(id=id)
        orders_count = len(user.orders)
        profile_text = f"<b>Профиль</b>\nid: {user.id}\nИмя: {user.name}\nКол-во заказов: {orders_count}"
        self.assertEqual(get_profile(user), profile_text)
        self.assertEqual(get_profile(1), False)
        self.assertEqual(get_profile('1'), False)
        self.assertEqual(get_profile(True), False)

    def test_get_order(self):
        id = 2  # Существуеющий заказ
        order = Order.get(id=2)
        text = "Статус"
        self.assertEqual(get_order(order)[3:9], text)
        self.assertEqual(get_order(1), False)
        self.assertEqual(get_order(True), False)
        self.assertEqual(get_order('1'), False)


if __name__ == "__main__":
    unittest.main()
