import pytest
from instrument_connector import (
    connect_to_instrument,
    list_available_resources,
    set_verbosity,
    InstrumentConnectionError,
)

# Mock di pyvisa
from unittest.mock import patch, MagicMock

# Test 1: Verificare che set_verbosity abiliti/disabiliti i messaggi
def test_set_verbosity():
    set_verbosity(True)
    assert True  # Non solleva errori

    set_verbosity(False)
    assert True  # Non solleva errori


# Test 2: Simulare risorse disponibili e verificare list_available_resources
@patch("instrument_connector.pyvisa.ResourceManager")
def test_list_available_resources(mock_resource_manager):
    # Mock delle risorse e IDN
    mock_rm_instance = mock_resource_manager.return_value
    mock_rm_instance.list_resources.return_value = [
        "USB0::0x1AB1::0x0588::DS1ED141904883::INSTR",
        "TCPIP0::192.168.1.100::INSTR",
    ]
    
    mock_instrument_1 = MagicMock()
    mock_instrument_1.query.return_value = "Rigol Technologies,DS1054Z,DS1ED141904883,00.04.02"

    mock_instrument_2 = MagicMock()
    mock_instrument_2.query.side_effect = Exception("No IDN")

    mock_rm_instance.open_resource.side_effect = [mock_instrument_1, mock_instrument_2]

    resources = list_available_resources()
    assert len(resources) == 2
    assert resources[0]["idn"] == "Rigol Technologies,DS1054Z,DS1ED141904883,00.04.02"
    assert resources[1]["idn"] == "Unknown"


# Test 3: Simulare connessione con identificatore valido
@patch("instrument_connector.pyvisa.ResourceManager")
def test_connect_to_instrument_success(mock_resource_manager):
    # Mock delle risorse e IDN
    mock_rm_instance = mock_resource_manager.return_value
    mock_rm_instance.list_resources.return_value = [
        "USB0::0x1AB1::0x0588::DS1ED141904883::INSTR"
    ]

    mock_instrument = MagicMock()
    mock_instrument.query.return_value = "Rigol Technologies,DS1054Z,DS1ED141904883,00.04.02"

    mock_rm_instance.open_resource.return_value = mock_instrument

    instrument = connect_to_instrument("DS1054Z")
    assert instrument.query("*IDN?") == "Rigol Technologies,DS1054Z,DS1ED141904883,00.04.02"


# Test 4: Simulare connessione con identificatore non valido
@patch("instrument_connector.pyvisa.ResourceManager")
def test_connect_to_instrument_failure(mock_resource_manager):
    # Mock delle risorse e IDN
    mock_rm_instance = mock_resource_manager.return_value
    mock_rm_instance.list_resources.return_value = [
        "USB0::0x1AB1::0x0588::DS1ED141904883::INSTR"
    ]

    mock_instrument = MagicMock()
    mock_instrument.query.return_value = "Rigol Technologies,DS1054Z,DS1ED141904883,00.04.02"

    mock_rm_instance.open_resource.return_value = mock_instrument

    with pytest.raises(InstrumentConnectionError):
        connect_to_instrument("InvalidModel")


# Test 5: Nessuna risorsa disponibile
@patch("instrument_connector.pyvisa.ResourceManager")
def test_no_resources_available(mock_resource_manager):
    # Mock delle risorse vuote
    mock_rm_instance = mock_resource_manager.return_value
    mock_rm_instance.list_resources.return_value = []

    with pytest.raises(InstrumentConnectionError):
        connect_to_instrument("AnyModel")
