from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InformationCls:
	"""Information commands group definition. 6 total commands, 0 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("information", core, parent)

	def get_bd_address(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:BDADdress \n
		Snippet: value: str = driver.sense.eut.information.get_bd_address() \n
		Gets the address (BD_ADDR) of the connected Bluetooth device. \n
			:return: bd_address: hex The Bluetooth device address in hexadecimal notation. Range: #H0 to #HFFFFFFFFFFFF (12 hexadecimal digits)
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:BDADdress?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class ClassPyStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Major_Dev_Class: str: string
			- Minor_Dev_Class: str: string"""
		__meta_args_list = [
			ArgStruct.scalar_str('Major_Dev_Class'),
			ArgStruct.scalar_str('Minor_Dev_Class')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Major_Dev_Class: str = None
			self.Minor_Dev_Class: str = None

	def get_class_py(self) -> ClassPyStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:CLASs \n
		Snippet: value: ClassPyStruct = driver.sense.eut.information.get_class_py() \n
		Gets the major and the minor device class of the connected EUT as specified in . \n
			:return: structure: for return value, see the help for ClassPyStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:CLASs?', self.__class__.ClassPyStruct())

	def get_company(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:COMPany \n
		Snippet: value: str = driver.sense.eut.information.get_company() \n
		Queries the company identifier (CompId) as defined in \n
			:return: company: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:COMPany?')
		return trim_str_response(response)

	def get_name(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:NAME \n
		Snippet: value: str = driver.sense.eut.information.get_name() \n
		Gets the name of the connected device. \n
			:return: name: string Up to 255 characters
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:NAME?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class VersionStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Lmp: str: string Textual representation of the LMP version (VersNr) as defined in
			- Company: str: string Textual representation of the company identifier (CompId) as defined in
			- Lmp_Subversion: str: string LMP subversion number (SubVersNr) , a company-internal version number"""
		__meta_args_list = [
			ArgStruct.scalar_str('Lmp'),
			ArgStruct.scalar_str('Company'),
			ArgStruct.scalar_str('Lmp_Subversion')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lmp: str = None
			self.Company: str = None
			self.Lmp_Subversion: str = None

	def get_version(self) -> VersionStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:VERSion \n
		Snippet: value: VersionStruct = driver.sense.eut.information.get_version() \n
		Gets LMP_version_res information. \n
			:return: structure: for return value, see the help for VersionStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:VERSion?', self.__class__.VersionStruct())

	# noinspection PyTypeChecker
	class LeSignalingStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Device_Name: str: string
			- Address_Type: enums.AddressTypeExt: PUBLic | RANDom | PIDentity | RSIDentity Public device address, random device address: random private ID, random static ID
			- Gm_Discoverable: bool: OFF | ON GAP mode general discoverable
			- Gm_Limit_Disc: bool: OFF | ON GAP mode limited discoverable
			- Gm_Connectable: bool: OFF | ON GAP mode undirected connectable
			- Gm_Direct_Con: bool: OFF | ON GAP mode directed connectable"""
		__meta_args_list = [
			ArgStruct.scalar_str('Device_Name'),
			ArgStruct.scalar_enum('Address_Type', enums.AddressTypeExt),
			ArgStruct.scalar_bool('Gm_Discoverable'),
			ArgStruct.scalar_bool('Gm_Limit_Disc'),
			ArgStruct.scalar_bool('Gm_Connectable'),
			ArgStruct.scalar_bool('Gm_Direct_Con')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Device_Name: str = None
			self.Address_Type: enums.AddressTypeExt = None
			self.Gm_Discoverable: bool = None
			self.Gm_Limit_Disc: bool = None
			self.Gm_Connectable: bool = None
			self.Gm_Direct_Con: bool = None

	def get_le_signaling(self) -> LeSignalingStruct:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:LESignaling \n
		Snippet: value: LeSignalingStruct = driver.sense.eut.information.get_le_signaling() \n
		Retrieves EUT information as device name, device address and GAP mode. \n
			:return: structure: for return value, see the help for LeSignalingStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:BLUetooth:SIGNaling<Instance>:EUT:INFormation:LESignaling?', self.__class__.LeSignalingStruct())
