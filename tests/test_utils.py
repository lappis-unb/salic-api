from salic_api.utils import pc_quote, encrypt, MLStripper
from mock import patch


class TestUtils:
    def test_pc_quote(self):
        """It quotes a given input"""
        assert pc_quote("abc") == "%{}%".format("abc")

    def test_encrypt_with_no_input(self):
        """It return an empty string if no text is given"""
        assert encrypt(None) == ""

    def test_encrypt_uses_random_iv(self):
        """It uses a random iv when STATIC_IV is None"""
        assert encrypt("test") == "30313233343536373839616263646566a575dfb1"

        with patch("salic_api.utils.STATIC_IV", None):
            assert encrypt(
                "test") != "30313233343536373839616263646566a575dfb1"

    def test_html_stripper_forces_list_on_its_feeder(self):
        """It forces the feeder to be a list"""
        stripper = MLStripper()
        stripper.fed = "not a list"

        assert isinstance(stripper.fed, str)
        stripper.handle_data("<a href='#'>link here</a>")
        assert isinstance(stripper.fed, list)

    def test_html_stripper_wont_fed_with_non_str_data(self):
        """It wont fed non str data"""
        stripper = MLStripper()
        stripper.handle_data(123456)

        assert stripper.get_data() == ""
        stripper.handle_data("123456")
        assert stripper.get_data() == "123456"
