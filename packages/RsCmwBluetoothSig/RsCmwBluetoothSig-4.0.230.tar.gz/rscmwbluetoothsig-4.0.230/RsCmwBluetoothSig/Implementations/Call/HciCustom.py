from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HciCustomCls:
	"""HciCustom commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hciCustom", core, parent)

	def send(self, custom_hci_byte: List[str] = None) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:HCICustom:SEND \n
		Snippet: driver.call.hciCustom.send(custom_hci_byte = ['rawAbc1', 'rawAbc2', 'rawAbc3']) \n
		Sends specified bytes in hexadecimal format as an HCI command via USB interface. You can send multiple bytes separated by
		comma. \n
			:param custom_hci_byte: hex Comma-separated hexadecimal string Range: #H0 to #HFF
		"""
		param = ''
		if custom_hci_byte:
			param = Conversions.list_to_csv_str(custom_hci_byte)
		self._core.io.write(f'CALL:BLUetooth:SIGNaling<Instance>:HCICustom:SEND {param}'.strip())
