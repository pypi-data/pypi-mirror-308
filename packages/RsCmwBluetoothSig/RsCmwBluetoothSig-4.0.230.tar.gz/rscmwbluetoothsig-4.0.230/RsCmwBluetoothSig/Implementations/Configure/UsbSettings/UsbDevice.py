from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsbDeviceCls:
	"""UsbDevice commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("usbDevice", core, parent)

	def set(self, no: int, usbSettings=repcap.UsbSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:USBSettings<nr>:USBDevice \n
		Snippet: driver.configure.usbSettings.usbDevice.set(no = 1, usbSettings = repcap.UsbSettings.Default) \n
		Specifies the USB port to be used for direct USB connection. The command is relevant for the direct USB connection ('HW
		Interface' = USB) . \n
			:param no: 1..2 1: HW interface for LE tests 2: HW interface for BR / EDR tests
			:param usbSettings: optional repeated capability selector. Default value: Sett1 (settable in the interface 'UsbSettings')
		"""
		param = Conversions.decimal_value_to_str(no)
		usbSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(usbSettings, repcap.UsbSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:USBSettings{usbSettings_cmd_val}:USBDevice {param}')

	def get(self, usbSettings=repcap.UsbSettings.Default) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:USBSettings<nr>:USBDevice \n
		Snippet: value: int = driver.configure.usbSettings.usbDevice.get(usbSettings = repcap.UsbSettings.Default) \n
		Specifies the USB port to be used for direct USB connection. The command is relevant for the direct USB connection ('HW
		Interface' = USB) . \n
			:param usbSettings: optional repeated capability selector. Default value: Sett1 (settable in the interface 'UsbSettings')
			:return: no: 1..2 1: HW interface for LE tests 2: HW interface for BR / EDR tests"""
		usbSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(usbSettings, repcap.UsbSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:USBSettings{usbSettings_cmd_val}:USBDevice?')
		return Conversions.str_to_int(response)
