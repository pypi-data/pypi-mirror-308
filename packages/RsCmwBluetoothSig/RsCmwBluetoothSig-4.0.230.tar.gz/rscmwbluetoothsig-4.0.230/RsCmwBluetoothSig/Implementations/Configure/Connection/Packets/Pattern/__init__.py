from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PatternCls:
	"""Pattern commands group definition. 5 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pattern", core, parent)

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	# noinspection PyTypeChecker
	def get_brate(self) -> enums.LeRangePaternType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:BRATe \n
		Snippet: value: enums.LeRangePaternType = driver.configure.connection.packets.pattern.get_brate() \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:BRATe?')
		return Conversions.str_to_scalar_enum(response, enums.LeRangePaternType)

	def set_brate(self, pattern_type: enums.LeRangePaternType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:BRATe \n
		Snippet: driver.configure.connection.packets.pattern.set_brate(pattern_type = enums.LeRangePaternType.ALL0) \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.LeRangePaternType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:BRATe {param}')

	# noinspection PyTypeChecker
	def get_edrate(self) -> enums.LeRangePaternType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:EDRate \n
		Snippet: value: enums.LeRangePaternType = driver.configure.connection.packets.pattern.get_edrate() \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:return: pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:EDRate?')
		return Conversions.str_to_scalar_enum(response, enums.LeRangePaternType)

	def set_edrate(self, pattern_type: enums.LeRangePaternType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:EDRate \n
		Snippet: driver.configure.connection.packets.pattern.set_edrate(pattern_type = enums.LeRangePaternType.ALL0) \n
		Select the bit pattern to be used for tests.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Commands for test mode classic: For BR (...:BRATe...) , EDR (...:EDRate...)
			- Commands for LE direct test mode: For LE 1M PHY (...:LE1M...) , LE 2M PHY (...:LE2M...)
			- Commands for LE UTP test mode: ..:TCONnection:.. \n
			:param pattern_type: ALL0 | ALL1 | P11 | P44 | PRBS9 | ALT ALL0: 00000000 ALL1: 11111111 P11: 10101010 P44: 11110000 PRBS9: Pseudo random bit sequences of a length of 9 bits (transmission of identical packet series) ALT: the periodical alternation of the pattern P11 and P44
		"""
		param = Conversions.enum_scalar_to_str(pattern_type, enums.LeRangePaternType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:PATTern:EDRate {param}')

	def clone(self) -> 'PatternCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PatternCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
