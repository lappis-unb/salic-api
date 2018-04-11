# import pytest

from salic_api.resources.format_utils import cgccpf_mask, sanitize


class TestFormatUtils:
    def test_cgccpf_mask_with_no_data(self):
        """cgccpf_mask with no data should retuen an empty string"""
        assert cgccpf_mask(None) == ""
        assert cgccpf_mask(False) == ""
        assert cgccpf_mask("") == ""

    def test_cgccpf_mask_masks_a_valid_cpf(self):
        """Given a valid cpf it will be masked"""
        cpf = "11438374798"

        assert cgccpf_mask(cpf) == "***%s**" % cpf[3:9]

    def test_cgccpf_mask_wont_mask_an_invalid_cpf(self):
        """Given an invalid cpf it will just return the given input"""
        assert cgccpf_mask("123456789") == "123456789"

    def test_sanitize_given_empty_string_with_no_input(self):
        """Given None input sanitize will just retun an empty string"""
        assert sanitize(None) == ""

