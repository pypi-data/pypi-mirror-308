from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhyCls:
	"""Phy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phy", core, parent)

	# noinspection PyTypeChecker
	def get_low_energy(self) -> enums.LePhysicalType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PHY:LENergy \n
		Snippet: value: enums.LePhysicalType = driver.configure.tconnection.phy.get_low_energy() \n
		Selects the physical layer used for LE connections.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE direct test mode: ..:PHY:LENergy
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE connection tests (normal mode) : ..:PHY:NMODe:LENergy
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE UTP test mode: ..:TCONnection:PHY:LENergy \n
			:return: phy: LE1M | LE2M | LELR LE1M: LE 1 Msymbol/s uncoded PHY LE2M: LE 2 Msymbol/s uncoded PHY LELR: LE 1 Msymbol/s long range (LE coded PHY)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PHY:LENergy?')
		return Conversions.str_to_scalar_enum(response, enums.LePhysicalType)

	def set_low_energy(self, phy: enums.LePhysicalType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PHY:LENergy \n
		Snippet: driver.configure.tconnection.phy.set_low_energy(phy = enums.LePhysicalType.LE1M) \n
		Selects the physical layer used for LE connections.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE direct test mode: ..:PHY:LENergy
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE connection tests (normal mode) : ..:PHY:NMODe:LENergy
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE UTP test mode: ..:TCONnection:PHY:LENergy \n
			:param phy: LE1M | LE2M | LELR LE1M: LE 1 Msymbol/s uncoded PHY LE2M: LE 2 Msymbol/s uncoded PHY LELR: LE 1 Msymbol/s long range (LE coded PHY)
		"""
		param = Conversions.enum_scalar_to_str(phy, enums.LePhysicalType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:PHY:LENergy {param}')
