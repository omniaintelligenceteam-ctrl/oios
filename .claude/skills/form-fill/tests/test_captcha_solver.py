# tests/test_captcha_solver.py
import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from captcha_solver import solve_recaptcha, solve_hcaptcha

def test_solve_recaptcha_returns_token():
    with patch('captcha_solver.TwoCaptcha') as MockSolver:
        instance = MockSolver.return_value
        instance.recaptcha.return_value = {'code': 'test-token-123'}
        result = solve_recaptcha('fake-site-key', 'https://example.com', 'fake-api-key')
        assert result == 'test-token-123'

def test_solve_hcaptcha_returns_token():
    with patch('captcha_solver.TwoCaptcha') as MockSolver:
        instance = MockSolver.return_value
        instance.hcaptcha.return_value = {'code': 'hcap-token-456'}
        result = solve_hcaptcha('fake-site-key', 'https://example.com', 'fake-api-key')
        assert result == 'hcap-token-456'

def test_solve_recaptcha_raises_on_failure():
    with patch('captcha_solver.TwoCaptcha') as MockSolver:
        instance = MockSolver.return_value
        instance.recaptcha.side_effect = Exception("API error")
        with pytest.raises(Exception, match="API error"):
            solve_recaptcha('bad-key', 'https://example.com', 'fake-api-key')
