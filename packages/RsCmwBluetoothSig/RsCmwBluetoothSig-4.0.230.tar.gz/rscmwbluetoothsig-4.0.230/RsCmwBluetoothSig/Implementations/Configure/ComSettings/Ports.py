from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PortsCls:
	"""Ports commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ports", core, parent)

	# noinspection PyTypeChecker
	class CatalogStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- No_Devices: int: decimal Number of all COM ports, where a connected EUT has been recognized
			- Item_Number: List[int]: decimal The number of a list item
			- Discovered_Port: List[str]: string Number of the virtual COM port, to which the used USB port has been mapped"""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Devices'),
			ArgStruct('Item_Number', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Discovered_Port', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Devices: int = None
			self.Item_Number: List[int] = None
			self.Discovered_Port: List[str] = None

	def get_catalog(self) -> CatalogStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings:PORTs:CATalog \n
		Snippet: value: CatalogStruct = driver.configure.comSettings.ports.get_catalog() \n
		Queries the COM ports used by an EUT. The command is relevant for the USB connection with USB-to-serial converter ('HW
		Interface' = USB to RS232 adapter) . Results are returned for each used USB port: <NoDevices>, {1, <DiscoveredPort>}1, ...
		, {<NoDevices>, <DiscoveredPort>}<NoDevices> \n
			:return: structure: for return value, see the help for CatalogStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings:PORTs:CATalog?', self.__class__.CatalogStruct())
