import pyvisa

# Global variable for verbosity
verbose = False

def set_verbosity(enable: bool):
    """
    Enables or disables verbosity in the library.

    Parameters:
        enable (bool): If True, enables print statements. If False, disables them.
    """
    global verbose
    verbose = enable

class InstrumentConnectionError(Exception):
    """Custom exception for instrument connection errors."""
    pass

def connect_to_instrument(identifier: str):
    """
    Connects to an instrument based on the given identifier.

    Parameters:
        identifier (str): The model, IDN substring, or address of the instrument.

    Returns:
        pyvisa.resources.Resource: The connected instrument resource.

    Raises:
        InstrumentConnectionError: If no instrument matches the identifier.
    """
    global verbose
    try:
        # Initialize PyVISA resource manager
        rm = pyvisa.ResourceManager()
        
        # Get all available resources
        resources = rm.list_resources()
        if not resources:
            raise InstrumentConnectionError("No instruments found.")
        
        # Scan resources for a match
        for address in resources:
            try:
                # Open the resource and query its IDN
                instrument = rm.open_resource(address)
                idn = instrument.query("*IDN?").strip()
                if identifier in idn or identifier in address:
                    if verbose:
                        print(f"Connected to instrument at {address} with IDN: {idn}")
                    return instrument
            except pyvisa.VisaIOError:
                # Skip resources that don't support *IDN?
                continue
        
        # If no match found, raise an error
        raise InstrumentConnectionError(f"No instrument found matching identifier: {identifier}")
    
    except pyvisa.VisaIOError as e:
        raise InstrumentConnectionError(f"VISA error occurred: {str(e)}")

def list_available_resources():
    """
    Lists all available resources and their IDNs (if available).

    Returns:
        list: A list of dictionaries containing the address and IDN of each resource.
    """
    global verbose
    try:
        # Initialize PyVISA resource manager
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()

        if verbose:
            print(f"Found resources: {resources}")

        resource_details = []
        for address in resources:
            try:
                # Query IDN if possible
                instrument = rm.open_resource(address)
                idn = instrument.query("*IDN?").strip()
                resource_details.append({"address": address, "idn": idn})
            except pyvisa.VisaIOError:
                # If *IDN? fails, just return the address
                resource_details.append({"address": address, "idn": "Unknown"})
        
        return resource_details

    except pyvisa.VisaIOError as e:
        raise InstrumentConnectionError(f"VISA error occurred while listing resources: {str(e)}")

# Define what is exported when using `import instrument_connector`
__all__ = ['connect_to_instrument', 'InstrumentConnectionError', 'set_verbosity', 'list_available_resources']
