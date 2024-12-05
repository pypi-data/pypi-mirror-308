from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InformationCls:
	"""Information commands group definition. 8 total commands, 0 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("information", core, parent)

	def get_dprotocol(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:DPRotocol \n
		Snippet: value: str = driver.sense.usbDevice.information.get_dprotocol() \n
		Returns the supported protocol of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:DPRotocol?')
		return trim_str_response(response)

	def get_dsub_class(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:DSUBclass \n
		Snippet: value: str = driver.sense.usbDevice.information.get_dsub_class() \n
		Returns the device subclass of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:DSUBclass?')
		return trim_str_response(response)

	def get_dclass(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:DCLass \n
		Snippet: value: str = driver.sense.usbDevice.information.get_dclass() \n
		Returns the device class of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:DCLass?')
		return trim_str_response(response)

	def get_idproduct(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:IDPRoduct \n
		Snippet: value: str = driver.sense.usbDevice.information.get_idproduct() \n
		Returns the product ID of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:IDPRoduct?')
		return trim_str_response(response)

	def get_id_vendor(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:IDVendor \n
		Snippet: value: str = driver.sense.usbDevice.information.get_id_vendor() \n
		Returns the vendor ID of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:IDVendor?')
		return trim_str_response(response)

	def get_product(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:PRODuct \n
		Snippet: value: str = driver.sense.usbDevice.information.get_product() \n
		Returns the product name of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:PRODuct?')
		return trim_str_response(response)

	def get_serial(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:SERial \n
		Snippet: value: str = driver.sense.usbDevice.information.get_serial() \n
		Returns the name serial of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:SERial?')
		return trim_str_response(response)

	def get_manufacturer(self) -> str:
		"""SCPI: SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:MANufacturer \n
		Snippet: value: str = driver.sense.usbDevice.information.get_manufacturer() \n
		Returns the name of the manufacturer of the active USB device. \n
			:return: name: string
		"""
		response = self._core.io.query_str('SENSe:BLUetooth:SIGNaling<Instance>:USBDevice:INFormation:MANufacturer?')
		return trim_str_response(response)
