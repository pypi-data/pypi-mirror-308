from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CatalogCls:
	"""Catalog commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	# noinspection PyTypeChecker
	class LeSignalingStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- No_Discovered_Devices: int: No parameter help available
			- Item_Number: List[int]: No parameter help available
			- Discovered_Eut: List[str]: string A comma-separated list of Bluetooth devices, where each device is represented by an item number and its Address in hexadecimal notation. Item number 0 always represents the default target."""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Discovered_Devices'),
			ArgStruct('Item_Number', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Discovered_Eut', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Discovered_Devices: int = None
			self.Item_Number: List[int] = None
			self.Discovered_Eut: List[str] = None

	def get_le_signaling(self) -> LeSignalingStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:PTARgets:CATalog:LESignaling \n
		Snippet: value: LeSignalingStruct = driver.configure.connection.inquiry.ptargets.catalog.get_le_signaling() \n
		This query returns a list of all targets available for paging, i.e. all LE devices found. If no inquiry was made before,
		this list only contains the default device (see method RsCmwBluetoothSig.Configure.Connection.Address.Eut.leSignaling) .
		After inquiry, it also contains the devices that were responding (in chronological order) . \n
			:return: structure: for return value, see the help for LeSignalingStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:PTARgets:CATalog:LESignaling?', self.__class__.LeSignalingStruct())

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- No_Discovered_Devices: int: No parameter help available
			- Item_Number: List[int]: No parameter help available
			- Discovered_Eut: List[str]: string A comma-separated list of Bluetooth devices, where each device is represented by an item number and its BD_Address in hexadecimal notation. Item number 0 always represents the default target."""
		__meta_args_list = [
			ArgStruct.scalar_int('No_Discovered_Devices'),
			ArgStruct('Item_Number', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Discovered_Eut', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.No_Discovered_Devices: int = None
			self.Item_Number: List[int] = None
			self.Discovered_Eut: List[str] = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:PTARgets:CATalog \n
		Snippet: value: ValueStruct = driver.configure.connection.inquiry.ptargets.catalog.get_value() \n
		This query returns a list of all targets available for paging. If no inquiry was made before, this list only contains the
		default device (see method RsCmwBluetoothSig.Configure.Connection.BdAddress.eut) . After inquiry, it also contains the
		devices that were responding (in chronological order) . \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:PTARgets:CATalog?', self.__class__.ValueStruct())
