import pytest
from unittest.mock import patch, Mock
import requests

from importmap.generator import ImportmapGenerator, ImportmapGeneratorError

def test_generate_success():
    generator = ImportmapGenerator(targets=['react@17', 'react-dom@17'])

    mock_response = Mock()
    mock_response.json.return_value = {
        'map': {
            'imports': {
                "react": "https://ga.jspm.io/npm:react@18.3.1/index.js",
                "react-dom": "https://ga.jspm.io/npm:react-dom@18.3.1/index.js"
            }
        }
    }
    mock_response.raise_for_status = Mock()
    mock_response.status_code = 200

    with patch('requests.post', return_value=mock_response) as mock_post:
        result = generator.generate()
        mock_post.assert_called_with(
            "https://api.jspm.io/generate",
            json={
                "install": ['react@17', 'react-dom@17'],
                "env": ['browser', 'module'],
                "provider": 'jspm',
            },
        )
        assert result == mock_response.json.return_value['map']

def test_generate_error_in_response():
    generator = ImportmapGenerator(targets=['react@17', 'react-dom@17'])

    mock_response = Mock()
    mock_response.json.return_value = {'error': 'Package not found'}
    mock_response.raise_for_status = Mock()
    mock_response.status_code = 200

    with patch('requests.post', return_value=mock_response):
        with pytest.raises(ImportmapGeneratorError) as exc_info:
            generator.generate()
        assert 'Package not found' in str(exc_info.value)

def test_generate_http_error():
    generator = ImportmapGenerator(targets=['react@17', 'react-dom@17'])

    mock_response = Mock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status.side_effect = requests.HTTPError('HTTP Error')
    mock_response.status_code = 500

    with patch('requests.post', return_value=mock_response):
        with pytest.raises(requests.HTTPError) as exc_info:
            generator.generate()
        assert 'HTTP Error' in str(exc_info.value)
