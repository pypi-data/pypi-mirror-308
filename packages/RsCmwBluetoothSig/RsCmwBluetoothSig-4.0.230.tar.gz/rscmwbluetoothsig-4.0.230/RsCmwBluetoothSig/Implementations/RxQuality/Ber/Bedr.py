from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BedrCls:
	"""Bedr commands group definition. 6 total commands, 0 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bedr", core, parent)

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:BLUetooth:SIGNaling<Instance>:RXQuality:BER[:BEDR] \n
		Snippet: driver.rxQuality.ber.bedr.abort() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:BLUetooth:SIGNaling<Instance>:RXQuality:BER:BEDR', opc_timeout_ms)

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:BLUetooth:SIGNaling<Instance>:RXQuality:BER[:BEDR] \n
		Snippet: driver.rxQuality.ber.bedr.initiate() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:BLUetooth:SIGNaling<Instance>:RXQuality:BER:BEDR', opc_timeout_ms)

	def stop(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:BLUetooth:SIGNaling<Instance>:RXQuality:BER[:BEDR] \n
		Snippet: driver.rxQuality.ber.bedr.stop() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:BLUetooth:SIGNaling<Instance>:RXQuality:BER:BEDR', opc_timeout_ms)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Ber: float: float Bit error rate Range: 0 % to 100 %, Unit: %
			- Per: float: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Bit_Errors: int: decimal Sum of received erroneous data bits Range: 0 to 9.22337203685477E+18
			- Missing_Packets: float: float Difference between the number of packets sent and the number of packets received in percentage Range: 0 % to 100 %, Unit: %
			- Nak: float: float Percentage of packets not acknowledged by the EUT positively Range: 0 % to 100 %, Unit: %
			- Hec_Errors: float: float Percentage of packets with the bit errors in the header Range: 0 % to 100 %, Unit: %
			- Crc_Errors: float: float Percentage of packets with the bit errors in the payload Range: 0 % to 100 %, Unit: %
			- Wrong_Packet_Rate: float: No parameter help available
			- Wrong_Payload_Rat: float: No parameter help available
			- Packets_Received: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Ber'),
			ArgStruct.scalar_float('Per'),
			ArgStruct.scalar_int('Bit_Errors'),
			ArgStruct.scalar_float('Missing_Packets'),
			ArgStruct.scalar_float('Nak'),
			ArgStruct.scalar_float('Hec_Errors'),
			ArgStruct.scalar_float('Crc_Errors'),
			ArgStruct.scalar_float('Wrong_Packet_Rate'),
			ArgStruct.scalar_float('Wrong_Payload_Rat'),
			ArgStruct.scalar_int('Packets_Received')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ber: float = None
			self.Per: float = None
			self.Bit_Errors: int = None
			self.Missing_Packets: float = None
			self.Nak: float = None
			self.Hec_Errors: float = None
			self.Crc_Errors: float = None
			self.Wrong_Packet_Rate: float = None
			self.Wrong_Payload_Rat: float = None
			self.Packets_Received: int = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:SIGNaling<Instance>:RXQuality:BER[:BEDR] \n
		Snippet: value: ResultData = driver.rxQuality.ber.bedr.read() \n
		Return all results of the signaling BER measurement. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:SIGNaling<Instance>:RXQuality:BER:BEDR?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:BER[:BEDR] \n
		Snippet: value: ResultData = driver.rxQuality.ber.bedr.fetch() \n
		Return all results of the signaling BER measurement. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:SIGNaling<Instance>:RXQuality:BER:BEDR?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal See 'Reliability indicator'
			- Ber: float or bool: float Bit error rate Range: 0 % to 100 %, Unit: %
			- Per: float or bool: float Packet error rate Range: 0 % to 100 %, Unit: %
			- Bit_Errors: float or bool: decimal Sum of received erroneous data bits Range: 0 to 9.22337203685477E+18
			- Missing_Packets: float or bool: float Difference between the number of packets sent and the number of packets received in percentage Range: 0 % to 100 %, Unit: %
			- Nak: float or bool: float Percentage of packets not acknowledged by the EUT positively Range: 0 % to 100 %, Unit: %
			- Hec_Errors: float or bool: float Percentage of packets with the bit errors in the header Range: 0 % to 100 %, Unit: %
			- Crc_Errors: float or bool: float Percentage of packets with the bit errors in the payload Range: 0 % to 100 %, Unit: %
			- Wrong_Packet_Rate: float or bool: No parameter help available
			- Wrong_Payload_Rat: float or bool: No parameter help available
			- Packets_Received: float or bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Ber'),
			ArgStruct.scalar_float_ext('Per'),
			ArgStruct.scalar_float_ext('Bit_Errors'),
			ArgStruct.scalar_float_ext('Missing_Packets'),
			ArgStruct.scalar_float_ext('Nak'),
			ArgStruct.scalar_float_ext('Hec_Errors'),
			ArgStruct.scalar_float_ext('Crc_Errors'),
			ArgStruct.scalar_float_ext('Wrong_Packet_Rate'),
			ArgStruct.scalar_float_ext('Wrong_Payload_Rat'),
			ArgStruct.scalar_float_ext('Packets_Received')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Ber: float or bool = None
			self.Per: float or bool = None
			self.Bit_Errors: float or bool = None
			self.Missing_Packets: float or bool = None
			self.Nak: float or bool = None
			self.Hec_Errors: float or bool = None
			self.Crc_Errors: float or bool = None
			self.Wrong_Packet_Rate: float or bool = None
			self.Wrong_Payload_Rat: float or bool = None
			self.Packets_Received: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:BER[:BEDR] \n
		Snippet: value: CalculateStruct = driver.rxQuality.ber.bedr.calculate() \n
		Return all results of the signaling BER measurement. The values described below are returned by FETCh and READ commands.
		CALCulate commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:SIGNaling<Instance>:RXQuality:BER:BEDR?', self.__class__.CalculateStruct())
