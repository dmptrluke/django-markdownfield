from markdownfield.validators import VALIDATORS, Validator


class TestCustomValidators:
    # custom validator auto-registers in VALIDATORS dict
    def test_custom_validator_registered(self):
        v = Validator(allowed_tags={'p'}, allowed_attrs={}, name='test_custom')
        assert VALIDATORS['test_custom'] is v
