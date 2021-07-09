import os
from typing import Dict

import pytest
from pytest_mock import MockFixture


def test_success():
    # --- Arrange
    event = {'user_id': 'user', 'unit_id': 'unit',
             'interaction_id': 'interaction', 'title': 'title'}
    context: Dict[str, str] = {}
    expected_response = {'id': 'id', 'group_id': 'id'}

    # --- Act
    from main import lambda_handler
    response: Dict = lambda_handler(event, context)

    # --- Assert
    assert response == expected_response
