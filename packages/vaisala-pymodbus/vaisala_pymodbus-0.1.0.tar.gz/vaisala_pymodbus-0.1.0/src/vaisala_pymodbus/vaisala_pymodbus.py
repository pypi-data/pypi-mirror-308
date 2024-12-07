
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
import logging
import serial.tools.list_ports

# Enable logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG) # comment out to enable debuggin mode, note more verbiose

class ModbusSensorClient:
    # Floating point measurement data registers (read-only)
    float_registers = {
        'relative_humidity': 0x0000,
        'temperature': 0x0002,
        'dew_point_temperature': 0x0006,
        'dew_frost_point_temperature': 0x0008,
        'dew_frost_point_temperature_at_1_atm': 0x000A,
        'dew_point_temperature_at_1_atm': 0x000C,
        'absolute_humidity': 0x000E,
        'mixing_ratio': 0x0010,
        'wet_bulb_temperature': 0x0012,
        'water_concentration': 0x0014,
        'water_vapor_pressure': 0x0016,
        'water_vapor_saturation_pressure': 0x0018,
        'enthalpy': 0x001A,
        'water_activity': 0x001C,
        'dew_point_temperature_difference': 0x001E,
        'absolute_humidity_at_NTP': 0x0020,
        'water_concentration_in_oil': 0x0022,
        'relative_saturation': 0x0028,
        'water_concentration_wet_basis': 0x002A,
        'relative_humidity_dew_frost': 0x002C,
        'water_mass_fraction': 0x0040,
        'floating_point': 0x1F01,
    }

    # Integer measurement data registers (read-only)
    int_registers = {
        'relative_humidity_int': (0x0100, 100, 0),  # (address, scale_factor, offset)
        'temperature_int': (0x0101, 100, 0),
        'dew_point_temperature_int': (0x0103, 100, 0),
        'dew_frost_point_temperature_int': (0x0104, 100, 0),
        'dew_frost_point_temperature_at_1_atm_int': (0x0105, 100, 0),
        'dew_point_temperature_at_1_atm_int': (0x0106, 100, 0),
        'absolute_humidity_int': (0x0107, 100, 0),
        'mixing_ratio_int': (0x0108, 100, 0),
        'wet_bulb_temperature_int': (0x0109, 100, 0),
        'water_concentration_int': (0x010A, 1, 0),
        'water_vapor_pressure_int': (0x010B, 10, 0),
        'water_vapor_saturation_pressure_int': (0x010C, 10, 0),
        'enthalpy_int': (0x010D, 100, 0),
        'water_activity_int': (0x010E, 10000, 0),
        'dew_point_temperature_difference_int': (0x010F, 10, 0),
        'absolute_humidity_at_NTP_int': (0x0110, 100, 0),
        'water_concentration_in_oil_int': (0x0111, 1, 0),
        'relative_saturation_int': (0x0114, 100, 0),
        'water_concentration_wet_basis_int': (0x0115, 100, 0),
        'relative_humidity_dew_frost_int': (0x0116, 100, 0),
        'water_vapor_mass_fraction_int': (0x0120, 1, 0),
        'signed_integer': (0x1F00, 1, 0),  
    }


    def __init__(self, comport, unit_id=240):
        """
        Initialize the ModbusSensorClient with a COM port and device address.

        Parameters:
        comport (str): The COM port for the Modbus device.
        unit_id (int): The Modbus slave address (default is 240).
        """
        
        
        def find_vaisala_port():
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if "Vaisala" in port.description:
                    return port.device
            return None
        
        # Store the Vaisala port in a variable
        vaisala_port = find_vaisala_port()
        
        # Display the result
        if vaisala_port:
            print(f"Vaisala device found on: {vaisala_port}")
        else:
            print("No Vaisala device found.")
        
        comport = vaisala_port
        
          
        self.comport = comport
        self.unit_id = unit_id
        self.client = ModbusSerialClient(
            method='rtu',
            port=self.comport,
            baudrate=19200,
            stopbits=2,
            bytesize=8,
            parity='N',
            timeout=1
        )

    def connect(self):
        """Establish connection to the Modbus device."""
        if not self.client.connect():
            print("Unable to connect to the Modbus device.")
            return False
        return True
    
    #support for more verbiose simple output
    def humidity(self):
        return self.read_measurement('relative_humidity')

    def temperature(self):
        return self.read_measurement('temperature')

    def dew_point_temperature(self):
        return self.read_measurement('dew_point_temperature')

    def dew_frost_point_temperature(self):
        return self.read_measurement('dew_frost_point_temperature')

    def dew_frost_point_temperature_at_1_atm(self):
        return self.read_measurement('dew_frost_point_temperature_at_1_atm')

    def dew_point_temperature_at_1_atm(self):
        return self.read_measurement('dew_point_temperature_at_1_atm')

    def absolute_humidity(self):
        return self.read_measurement('absolute_humidity')

    def mixing_ratio(self):
        return self.read_measurement('mixing_ratio')

    def wet_bulb_temperature(self):
        return self.read_measurement('wet_bulb_temperature')

    def water_concentration(self):
        return self.read_measurement('water_concentration')

    def water_vapor_pressure(self):
        return self.read_measurement('water_vapor_pressure')

    def water_vapor_saturation_pressure(self):
        return self.read_measurement('water_vapor_saturation_pressure')

    def enthalpy(self):
        return self.read_measurement('enthalpy')

    def water_activity(self):
        return self.read_measurement('water_activity')

    def dew_point_temperature_difference(self):
        return self.read_measurement('dew_point_temperature_difference')

    def absolute_humidity_at_NTP(self):
        return self.read_measurement('absolute_humidity_at_NTP')

    def water_concentration_in_oil(self):
        return self.read_measurement('water_concentration_in_oil')

    def relative_saturation(self):
        return self.read_measurement('relative_saturation')

    def water_concentration_wet_basis(self):
        return self.read_measurement('water_concentration_wet_basis')

    def relative_humidity_dew_frost(self):
        return self.read_measurement('relative_humidity_dew_frost')

    def water_mass_fraction(self):
        return self.read_measurement('water_mass_fraction')

    # Integer versions of similar measurements
    def humidity_int(self):
        return self.read_measurement('relative_humidity_int')

    def temperature_int(self):
        return self.read_measurement('temperature_int')

    def dew_point_temperature_int(self):
        return self.read_measurement('dew_point_temperature_int')

    def dew_frost_point_temperature_int(self):
        return self.read_measurement('dew_frost_point_temperature_int')

    def dew_frost_point_temperature_at_1_atm_int(self):
        return self.read_measurement('dew_frost_point_temperature_at_1_atm_int')

    def dew_point_temperature_at_1_atm_int(self):
        return self.read_measurement('dew_point_temperature_at_1_atm_int')

    def absolute_humidity_int(self):
        return self.read_measurement('absolute_humidity_int')

    def mixing_ratio_int(self):
        return self.read_measurement('mixing_ratio_int')

    def wet_bulb_temperature_int(self):
        return self.read_measurement('wet_bulb_temperature_int')

    def water_concentration_int(self):
        return self.read_measurement('water_concentration_int')

    def water_vapor_pressure_int(self):
        return self.read_measurement('water_vapor_pressure_int')

    def water_vapor_saturation_pressure_int(self):
        return self.read_measurement('water_vapor_saturation_pressure_int')

    def enthalpy_int(self):
        return self.read_measurement('enthalpy_int')

    def water_activity_int(self):
        return self.read_measurement('water_activity_int')

    def dew_point_temperature_difference_int(self):
        return self.read_measurement('dew_point_temperature_difference_int')

    def absolute_humidity_at_NTP_int(self):
        return self.read_measurement('absolute_humidity_at_NTP_int')

    def water_concentration_in_oil_int(self):
        return self.read_measurement('water_concentration_in_oil_int')

    def relative_saturation_int(self):
        return self.read_measurement('relative_saturation_int')

    def water_concentration_wet_basis_int(self):
        return self.read_measurement('water_concentration_wet_basis_int')

    def relative_humidity_dew_frost_int(self):
        return self.read_measurement('relative_humidity_dew_frost_int')

    def water_mass_fraction_int(self):
        return self.read_measurement('water_vapor_mass_fraction_int')
    
    def read_measurement(self, parameter_name):
        """
        Reads a single measurement specified by the parameter_name.

        Parameters:
            parameter_name (str): The name of the measurement parameter to read.

        Returns:
            float or None: The measurement value or None if reading fails.
        """
        # Check if the parameter is in the float or int registers
        if parameter_name in self.float_registers:
            address = self.float_registers[parameter_name]
            count = 2  # 32-bit float uses 2 registers
            datatype = 'float'
        elif parameter_name in self.int_registers:
            address, scale_factor, offset = self.int_registers[parameter_name]
            count = 1  # 16-bit integer uses 1 register
            datatype = 'int'
        else:
            print(f"Parameter '{parameter_name}' is not recognized.")
            return None


        # Read registers from the device
        response = self.client.read_holding_registers(address=address, count=count, unit=self.unit_id)

        # Check for errors
        if response.isError():
            print(f"Error reading registers: {response}")
            return None
        else:
            # Decode the register data
            if datatype == 'float':
                decoder = BinaryPayloadDecoder.fromRegisters(
                    response.registers,
                    byteorder=Endian.Big,
                    wordorder=Endian.Little
                )
                value = decoder.decode_32bit_float()
                if str(value) == 'nan':
                    # print(f"{parameter_name.replace('_', ' ').capitalize()} value is not available.")
                    return None
                return value
    
            elif datatype == 'int':
                decoder = BinaryPayloadDecoder.fromRegisters(
                    response.registers,
                    byteorder=Endian.Big
                )
                raw_value = decoder.decode_16bit_int()
                if raw_value > 32767:
                    raw_value -= 65536
                    if raw_value == -32768:
                        # print(f"{parameter_name.replace('_', ' ').capitalize()} value is not available.")
                        return None
                if raw_value == 32767:
                    value = 32767 / scale_factor + offset
                elif raw_value == -32767:
                    value = -32767 / scale_factor + offset
                else:
                    value = (raw_value / scale_factor) + offset
                return value


            # print(f"{parameter_name.replace('_', ' ').capitalize()}: {value}")
            return value

    def read_measurements(self, parameters):
        """
        Reads multiple measurement parameters.

        Parameters:
        parameters (list): A list of measurement parameter names to read.

        Returns:
        dict: A dictionary mapping parameter names to their measurement values.
        """
        results = {}

        if not self.connect():
            return None
        
        for parameter in parameters:
            value = self.read_measurement(parameter)
            results[parameter] = value

        return results

    def write_configuration(self, parameter, value):
        """
        Writes a value to a configuration register.

        Parameters:
        parameter (str): The configuration parameter to write.
        value: The value to write.

        Returns:
        bool: True if write was successful, False otherwise.
        """
        # Configuration registers
        config_registers = {
            'condensation_prevention': (0x0506, 'bool'),  # Condensation prevention on/off
            'pressure_compensation': (0x0300, 'float'),    # Pressure compensation setpoint
            'temperature_compensation': (0x0334, 'float'), # Temperature compensation setpoint
            'sensor_purge_interval': (0x0304, 'float'),    # Sensor purge interval
            'interval_purge_on_off': (0x0502, 'bool'),     # Interval purge on/off
            'startup_purge_on_off': (0x0503, 'bool'),      # Startup purge on/off
            'measurement_filtering_factor': (0x031A, 'float'), # Measurement filtering factor
            'filtering_on_off': (0x0501, 'bool'),          # Enable/disable measurement filtering
            'modbus_address': (0x0600, 'int'),             # Modbus address
            'bit_rate': (0x0601, 'enum'),                  # Bit rate
            'parity_data_stop_bits': (0x0602, 'enum'),     # Parity, data, stop bits
            'response_delay': (0x0603, 'int'),             # Response delay
            # Add other configuration registers as needed
        }

        if parameter not in config_registers:
            print(f"Configuration parameter '{parameter}' is not recognized.")
            return False

        addr, data_type = config_registers[parameter]

        if not self.connect():
            return False

        if data_type == 'float':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
            builder.add_32bit_float(value)
            payload = builder.to_registers()
            count = 2
        elif data_type == 'int':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_int(int(value))
            payload = builder.to_registers()
            count = 1
        elif data_type == 'bool':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_int(1 if value else 0)
            payload = builder.to_registers()
            count = 1
        elif data_type == 'enum':
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_16bit_int(int(value))
            payload = builder.to_registers()
            count = 1
        else:
            print(f"Unsupported data type '{data_type}' for parameter '{parameter}'.")
            return False

        # Write multiple registers function code 16 (0x10)
        response = self.client.write_registers(address=addr, values=payload, unit=self.unit_id)

        if response.isError():
            print(f"Error writing to register {hex(addr)}: {response}")
            return False

        # Optionally, read back the register to verify
        # ...

        return True

    def read_status(self):
        """
        Reads the status registers.

        Returns:
        dict: A dictionary containing status information.
        """
        status_registers = {
            'error_status': 0x0200,
            'online_status': 0x0201,
            'error_code': 0x0203,
            'security_hash': 0x0205,
            'RH_measurement_status': 0x0207,
            'T_measurement_status': 0x0208,
            'Td_f_measurement_status': 0x0209,
            'device_status': 0x020A,
            # Add other status registers as needed
        }

        results = {}

        if not self.connect():
            return None

        addresses = []
        for name, addr in status_registers.items():
            addresses.append((addr, 1, name))  # Status registers are 16-bit

        # Sort addresses
        addresses.sort(key=lambda x: x[0])

        # Read all status registers in one block if possible
        start_addr = addresses[0][0]
        end_addr = addresses[-1][0] + 1
        count = end_addr - start_addr

        response = self.client.read_holding_registers(address=start_addr, count=count, unit=self.unit_id)
        if response.isError():
            print(f"Error reading status registers starting at {hex(start_addr)}: {response}")
            return None

        regs = response.registers
        reg_dict = {}
        for i in range(len(regs)):
            reg_addr = start_addr + i
            reg_dict[reg_addr] = regs[i]

        for addr, _, name in addresses:
            raw_value = reg_dict.get(addr, None)
            if raw_value is not None:
                results[name] = raw_value
            else:
                results[name] = None

        return results
    
    def read_test_values(self):
        """
        Reads known test values to verify Modbus implementation.
    
        Returns:
        dict: A dictionary containing the test values.
        """
        # Define test register parameters
        test_parameters = {
            'signed_integer': 'signed_integer',
            'floating_point': 'floating_point',
        }
    
        test_registers = {
            'signed_integer': 'signed_integer',    # 16-bit integer test value
            'floating_point': 'floating_point',    # 32-bit float test value
        }
    
        # Read each test parameter using the measurement function
        test_values = {}
        for param, register in test_registers.items():
            test_values[param] = self.read_measurement(register)
    
        return test_values

    def start_sensor_purge(self):
        """
        Initiates the sensor purge function.

        Returns:
        bool: True if the command was accepted, False otherwise.
        """
        register_address = 0x0504  # Start sensor purge

        if not self.connect():
            return False

        # Write value 1 to start sensor purge
        response = self.client.write_register(address=register_address, value=1, unit=self.unit_id)

        if response.isError():
            print(f"Error starting sensor purge: {response}")
            return False

        # Optionally, monitor the register to see the progress
        # The register value counts up from 0 to 100 during purge
        # ...

        return True

    def restart_device(self):
        """
        Restarts the device.

        Returns:
        bool: True if the command was accepted, False otherwise.
        """
        register_address = 0x0605  # Restart device

        if not self.connect():
            return False

        # Write value 1 to restart the device
        response = self.client.write_register(address=register_address, value=1, unit=self.unit_id)


        if response.isError():
            print(f"Error restarting device: {response}")
            return False

        return True


# Usage example:
if __name__ == "__main__":
    client = ModbusSensorClient(comport='COM15', unit_id=240)
    parameters_to_read = [
        'relative_humidity',
        'temperature',
        'dew_point_temperature',
        'absolute_humidity',
        'relative_humidity_int',
        'temperature_int',
        'dew_point_temperature_int',
        'absolute_humidity_int',
        # Add other parameters as needed
    ]
    measurements = client.read_measurements(parameters_to_read)
    print("Measurements:")
    for param, value in measurements.items():
        print(f"{param}: {value}")

    # Read status registers
    status = client.read_status()
    print("\nStatus:")
    for key, value in status.items():
        print(f"{key}: {value}")

    # Write configuration example
    success = client.write_configuration('pressure_compensation', 1013.25)
    print(f"\nPressure compensation set: {success}")

    # Read test values
    test_values = client.read_test_values()
    print("\nTest Values:")
    for key, value in test_values.items():
        print(f"{key}: {value}")
