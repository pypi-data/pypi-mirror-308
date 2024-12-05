from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.CodingScheme:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:FEC:LENergy:LRANge \n
		Snippet: value: enums.CodingScheme = driver.configure.tconnection.fec.lowEnergy.get_lrange() \n
		Defines the coding S for LE coded PHY according to the core specification version 5.0 for Bluetooth wireless technology.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE direct test mode: ..:FEC:LENergy..
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE connection tests (normal mode) : ..:FEC:NMODe:LENergy..
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE UTP test mode: ..:TCONnection:FEC:LENergy.. \n
			:return: coding_scheme: S8 | S2 Coding S = 8 or S = 2
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:FEC:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.CodingScheme)

	def set_lrange(self, coding_scheme: enums.CodingScheme) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:FEC:LENergy:LRANge \n
		Snippet: driver.configure.tconnection.fec.lowEnergy.set_lrange(coding_scheme = enums.CodingScheme.S2) \n
		Defines the coding S for LE coded PHY according to the core specification version 5.0 for Bluetooth wireless technology.
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE direct test mode: ..:FEC:LENergy..
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE connection tests (normal mode) : ..:FEC:NMODe:LENergy..
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- Command for LE UTP test mode: ..:TCONnection:FEC:LENergy.. \n
			:param coding_scheme: S8 | S2 Coding S = 8 or S = 2
		"""
		param = Conversions.enum_scalar_to_str(coding_scheme, enums.CodingScheme)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:FEC:LENergy:LRANge {param}')
