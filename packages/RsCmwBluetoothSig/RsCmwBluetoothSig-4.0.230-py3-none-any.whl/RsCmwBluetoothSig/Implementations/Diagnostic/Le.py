from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LeCls:
	"""Le commands group definition. 5 total commands, 0 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le", core, parent)

	def get_mode(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:MODE \n
		Snippet: value: bool = driver.diagnostic.le.get_mode() \n
		No command help available \n
			:return: le_test_mode: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, le_test_mode: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:MODE \n
		Snippet: driver.diagnostic.le.set_mode(le_test_mode = False) \n
		No command help available \n
			:param le_test_mode: No help available
		"""
		param = Conversions.bool_to_str(le_test_mode)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:MODE {param}')

	# noinspection PyTypeChecker
	def get_state(self) -> enums.LeDiagState:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:STATe \n
		Snippet: value: enums.LeDiagState = driver.diagnostic.le.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.LeDiagState)

	def get_packet_length(self) -> int:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PLENgth \n
		Snippet: value: int = driver.diagnostic.le.get_packet_length() \n
		No command help available \n
			:return: payload_length: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PLENgth?')
		return Conversions.str_to_int(response)

	def set_packet_length(self, payload_length: int) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PLENgth \n
		Snippet: driver.diagnostic.le.set_packet_length(payload_length = 1) \n
		No command help available \n
			:param payload_length: No help available
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PLENgth {param}')

	def get_channel(self) -> int:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:CHANnel \n
		Snippet: value: int = driver.diagnostic.le.get_channel() \n
		No command help available \n
			:return: channel: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:CHANnel?')
		return Conversions.str_to_int(response)

	def set_channel(self, channel: int) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:CHANnel \n
		Snippet: driver.diagnostic.le.set_channel(channel = 1) \n
		No command help available \n
			:param channel: No help available
		"""
		param = Conversions.decimal_value_to_str(channel)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:CHANnel {param}')

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.LeRangePaternType:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PATTern \n
		Snippet: value: enums.LeRangePaternType = driver.diagnostic.le.get_pattern() \n
		No command help available \n
			:return: pattern: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.LeRangePaternType)

	def set_pattern(self, pattern: enums.LeRangePaternType) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PATTern \n
		Snippet: driver.diagnostic.le.set_pattern(pattern = enums.LeRangePaternType.ALL0) \n
		No command help available \n
			:param pattern: No help available
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.LeRangePaternType)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:LE:PATTern {param}')
