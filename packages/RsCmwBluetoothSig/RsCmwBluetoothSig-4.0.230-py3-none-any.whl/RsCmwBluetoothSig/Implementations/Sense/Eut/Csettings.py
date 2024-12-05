from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsettingsCls:
	"""Csettings commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csettings", core, parent)

	# noinspection PyTypeChecker
	class LeSignalingStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Connection_Int: float: float Range: 6 to 3200
			- Supervision_Tout: float: float Supervision timeout Range: 100 ms to 32E+3 ms
			- Slave_Latency: float: float Slave latency Range: 0 to 499"""
		__meta_args_list = [
			ArgStruct.scalar_float('Connection_Int'),
			ArgStruct.scalar_float('Supervision_Tout'),
			ArgStruct.scalar_float('Slave_Latency')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Connection_Int: float = None
			self.Supervision_Tout: float = None
			self.Slave_Latency: float = None

	def get_le_signaling(self) -> LeSignalingStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:CSETtings:LESignaling \n
		Snippet: value: LeSignalingStruct = driver.sense.eut.csettings.get_le_signaling() \n
		Queries the connection parameters for LE normal mode. \n
			:return: structure: for return value, see the help for LeSignalingStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:CSETtings:LESignaling?', self.__class__.LeSignalingStruct())
