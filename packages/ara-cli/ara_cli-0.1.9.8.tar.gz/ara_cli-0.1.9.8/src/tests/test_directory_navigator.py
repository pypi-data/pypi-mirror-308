from src.directory_navigator import DirectoryNavigator
import pytest


@pytest.fixture
def navigator():
    return DirectoryNavigator()
