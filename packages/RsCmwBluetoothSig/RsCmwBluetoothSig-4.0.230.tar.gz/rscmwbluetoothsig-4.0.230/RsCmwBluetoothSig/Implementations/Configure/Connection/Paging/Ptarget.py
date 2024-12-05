from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PtargetCls:
	"""Ptarget commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ptarget", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget:LESignaling \n
		Snippet: value: int = driver.configure.connection.paging.ptarget.get_le_signaling() \n
		Selects the EUT for paging. The default device is 0. For the inquiry results, see method RsCmwBluetoothSig.Configure.
		Connection.Inquiry.Ptargets.Catalog.leSignaling. \n
			:return: target: numeric Sequence number of device listed in inquiry results.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, target: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget:LESignaling \n
		Snippet: driver.configure.connection.paging.ptarget.set_le_signaling(target = 1) \n
		Selects the EUT for paging. The default device is 0. For the inquiry results, see method RsCmwBluetoothSig.Configure.
		Connection.Inquiry.Ptargets.Catalog.leSignaling. \n
			:param target: numeric Sequence number of device listed in inquiry results.
		"""
		param = Conversions.decimal_value_to_str(target)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget:LESignaling {param}')

	def get_value(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget \n
		Snippet: value: int = driver.configure.connection.paging.ptarget.get_value() \n
		Selects the device to page from the paging target catalog (see method RsCmwBluetoothSig.Configure.Connection.Inquiry.
		Ptargets.Catalog.value) . After a reset, if no inquiry was made before or if no device was detected during the previous
		inquiry, only the default device (<Target>=0) can be selected. After a successful inquiry, the first discovered device
		(<Target>=1) is pre-selected. \n
			:return: target: numeric Index of the device in the paging target catalog, where 0 always corresponds to the default device. If an invalid index is selected, an error message is returned. Range: Integer = 0
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget?')
		return Conversions.str_to_int(response)

	def set_value(self, target: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget \n
		Snippet: driver.configure.connection.paging.ptarget.set_value(target = 1) \n
		Selects the device to page from the paging target catalog (see method RsCmwBluetoothSig.Configure.Connection.Inquiry.
		Ptargets.Catalog.value) . After a reset, if no inquiry was made before or if no device was detected during the previous
		inquiry, only the default device (<Target>=0) can be selected. After a successful inquiry, the first discovered device
		(<Target>=1) is pre-selected. \n
			:param target: numeric Index of the device in the paging target catalog, where 0 always corresponds to the default device. If an invalid index is selected, an error message is returned. Range: Integer = 0
		"""
		param = Conversions.decimal_value_to_str(target)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PTARget {param}')
