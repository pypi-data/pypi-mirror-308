from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 5 total commands, 0 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	class LeSignalingStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Pow_Flag: enums.PowerFlag: NONE | MIN | MAX NONE: no new message MIN: minimum power command accepted MAX: maximum power command accepted
			- Pow_Delta: int: decimal Returns the power difference before and after the command execution Range: -100 dB to +100 dB
			- Current_Power: int: decimal Returns the actual Tx power level of the DUT Range: -200 dBm to +100 dBm
			- Eut_State: enums.EutState: FAIL | OK Checks the command execution."""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pow_Flag', enums.PowerFlag),
			ArgStruct.scalar_int('Pow_Delta'),
			ArgStruct.scalar_int('Current_Power'),
			ArgStruct.scalar_enum('Eut_State', enums.EutState)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pow_Flag: enums.PowerFlag = None
			self.Pow_Delta: int = None
			self.Current_Power: int = None
			self.Eut_State: enums.EutState = None

	def get_le_signaling(self) -> LeSignalingStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:LESignaling \n
		Snippet: value: LeSignalingStruct = driver.sense.eut.powerControl.state.get_le_signaling() \n
		Displays the DUT's responses to the power control state commands for low energy. \n
			:return: structure: for return value, see the help for LeSignalingStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:LESignaling?', self.__class__.LeSignalingStruct())

	# noinspection PyTypeChecker
	class GfskStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Power_Change: enums.PowerChange: NNE | UP | DOWN | MAX NNE: none UP: power up command accepted DOWN: power down command accepted MAX: maximum power command accepted
			- Power_Min_Max: enums.PowerMinMax: NOTS | CHANged | MAX | MIN | NNM NOTS: not supported (command not accepted by the EUT) CHANged: changed one step MAX: max power reached MIN: min power reached NNM: no new message"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Power_Change', enums.PowerChange),
			ArgStruct.scalar_enum('Power_Min_Max', enums.PowerMinMax)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power_Change: enums.PowerChange = None
			self.Power_Min_Max: enums.PowerMinMax = None

	def get_gfsk(self) -> GfskStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:GFSK \n
		Snippet: value: GfskStruct = driver.sense.eut.powerControl.state.get_gfsk() \n
		Displays the EUT responses to the enhanced power control state commands for GFSK-modulated BR and Pi/4 DQPSK or
		8DPSK-modulated EDR packets. The modulation is indicated by the last mnemonic. \n
			:return: structure: for return value, see the help for GfskStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:GFSK?', self.__class__.GfskStruct())

	# noinspection PyTypeChecker
	class DqpskStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Power_Change: enums.PowerChange: NNE | UP | DOWN | MAX NNE: none UP: power up command accepted DOWN: power down command accepted MAX: maximum power command accepted
			- Power_Min_Max: enums.PowerMinMax: NOTS | CHANged | MAX | MIN | NNM NOTS: not supported (command not accepted by the EUT) CHANged: changed one step MAX: max power reached MIN: min power reached NNM: no new message"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Power_Change', enums.PowerChange),
			ArgStruct.scalar_enum('Power_Min_Max', enums.PowerMinMax)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power_Change: enums.PowerChange = None
			self.Power_Min_Max: enums.PowerMinMax = None

	def get_dqpsk(self) -> DqpskStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:DQPSk \n
		Snippet: value: DqpskStruct = driver.sense.eut.powerControl.state.get_dqpsk() \n
		Displays the EUT responses to the enhanced power control state commands for GFSK-modulated BR and Pi/4 DQPSK or
		8DPSK-modulated EDR packets. The modulation is indicated by the last mnemonic. \n
			:return: structure: for return value, see the help for DqpskStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:DQPSk?', self.__class__.DqpskStruct())

	# noinspection PyTypeChecker
	class DpskStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Power_Change: enums.PowerChange: NNE | UP | DOWN | MAX NNE: none UP: power up command accepted DOWN: power down command accepted MAX: maximum power command accepted
			- Power_Min_Max: enums.PowerMinMax: NOTS | CHANged | MAX | MIN | NNM NOTS: not supported (command not accepted by the EUT) CHANged: changed one step MAX: max power reached MIN: min power reached NNM: no new message"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Power_Change', enums.PowerChange),
			ArgStruct.scalar_enum('Power_Min_Max', enums.PowerMinMax)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power_Change: enums.PowerChange = None
			self.Power_Min_Max: enums.PowerMinMax = None

	def get_dpsk(self) -> DpskStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:DPSK \n
		Snippet: value: DpskStruct = driver.sense.eut.powerControl.state.get_dpsk() \n
		Displays the EUT responses to the enhanced power control state commands for GFSK-modulated BR and Pi/4 DQPSK or
		8DPSK-modulated EDR packets. The modulation is indicated by the last mnemonic. \n
			:return: structure: for return value, see the help for DpskStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe:DPSK?', self.__class__.DpskStruct())

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Pow_Change_Gfsk: enums.PowerChange: NNE | UP | DOWN | MAX NNE: none UP: power up command accepted DOWN: power down command accepted MAX: maximum power command accepted
			- Pow_Min_Max_Gfsk: enums.PowerMinMax: NOTS | CHANged | MAX | MIN | NNM NOTS: not supported (command not accepted by the EUT) CHANged: changed one step MAX: max power reached MIN: min power reached NNM: no new message
			- Pow_Change_Dqpsk: enums.PowerChange: NNE | UP | DOWN | MAX
			- Pow_Min_Max_Dqpsk: enums.PowerMinMax: NOTS | CHANged | MAX | MIN | NNM
			- Pow_Change_Dpsk: enums.PowerChange: NNE | UP | DOWN | MAX
			- Pow_Min_Max_Dpsk: enums.PowerMinMax: NOTS | CHANged | MAX | MIN | NNM"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Pow_Change_Gfsk', enums.PowerChange),
			ArgStruct.scalar_enum('Pow_Min_Max_Gfsk', enums.PowerMinMax),
			ArgStruct.scalar_enum('Pow_Change_Dqpsk', enums.PowerChange),
			ArgStruct.scalar_enum('Pow_Min_Max_Dqpsk', enums.PowerMinMax),
			ArgStruct.scalar_enum('Pow_Change_Dpsk', enums.PowerChange),
			ArgStruct.scalar_enum('Pow_Min_Max_Dpsk', enums.PowerMinMax)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pow_Change_Gfsk: enums.PowerChange = None
			self.Pow_Min_Max_Gfsk: enums.PowerMinMax = None
			self.Pow_Change_Dqpsk: enums.PowerChange = None
			self.Pow_Min_Max_Dqpsk: enums.PowerMinMax = None
			self.Pow_Change_Dpsk: enums.PowerChange = None
			self.Pow_Min_Max_Dpsk: enums.PowerMinMax = None

	def get_value(self) -> ValueStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe \n
		Snippet: value: ValueStruct = driver.sense.eut.powerControl.state.get_value() \n
		Displays the EUT responses to the enhanced power control state commands for GFSK-modulated BR and Pi/4 DQPSK and
		8DPSK-modulated EDR packets. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:PCONtrol:STATe?', self.__class__.ValueStruct())
