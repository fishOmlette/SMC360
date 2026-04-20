from unittest.mock import patch
from smc360.cli import main

@patch('smc360.cli.SocialMediaConnector')
def test_main_with_config(mock_connector):
    config_path = "path/to/config"
    main(['-c', config_path])
    mock_connector.assert_called_with(config_path)
    mock_connector.return_value.run.assert_called_once()

@patch('smc360.cli.explorer')
def test_main_explorer(mock_explorer):
    main(['-e'])
    mock_explorer.assert_called_once()

@patch('smc360.cli.print')
def test_main_with_no_param(mock_no_param):
    main([])
    mock_no_param.assert_called_once()
