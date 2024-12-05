from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.LeRangePaternType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE1M \n
		Snippet: value: enums.LeRangePaternType = driver.configure.tconnection.packets.pattern.lowEnergy.get_le_1_m() \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.LeRangePaternType)

	def set_le_1_m(self, pattern_type: enums.LeRangePaternType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE1M \n
		Snippet: driver.configure.tconnection.packets.pattern.lowEnergy.set_le_1_m(pattern_type = enums.LeRangePaternType.ALL0) \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.LeRangePaternType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE1M {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.LeRangePaternType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE2M \n
		Snippet: value: enums.LeRangePaternType = driver.configure.tconnection.packets.pattern.lowEnergy.get_le_2_m() \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.LeRangePaternType)

	def set_le_2_m(self, pattern_type: enums.LeRangePaternType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE2M \n
		Snippet: driver.configure.tconnection.packets.pattern.lowEnergy.set_le_2_m(pattern_type = enums.LeRangePaternType.ALL0) \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.LeRangePaternType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LE2M {param}')

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.LeRangePaternType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LRANge \n
		Snippet: value: enums.LeRangePaternType = driver.configure.tconnection.packets.pattern.lowEnergy.get_lrange() \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.LeRangePaternType)

	def set_lrange(self, pattern_type: enums.LeRangePaternType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LRANge \n
		Snippet: driver.configure.tconnection.packets.pattern.lowEnergy.set_lrange(pattern_type = enums.LeRangePaternType.ALL0) \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.LeRangePaternType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PACKets:PATTern:LENergy:LRANge {param}')
