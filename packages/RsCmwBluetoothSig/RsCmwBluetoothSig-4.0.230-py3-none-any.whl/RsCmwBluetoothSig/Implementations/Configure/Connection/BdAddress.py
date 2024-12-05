from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BdAddressCls:
	"""BdAddress commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bdAddress", core, parent)

	def get_cmw(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:CMW \n
		Snippet: value: str = driver.configure.connection.bdAddress.get_cmw() \n
		Sets/gets the Bluetooth device address (BD_ADDR) of the R&S CMW. \n
			:return: bd_address: hex Range: #H0 to #HFFFFFFFFFFFF (12 hexadecimal digits)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:CMW?')
		return trim_str_response(response)

	def set_cmw(self, bd_address: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:CMW \n
		Snippet: driver.configure.connection.bdAddress.set_cmw(bd_address = rawAbc) \n
		Sets/gets the Bluetooth device address (BD_ADDR) of the R&S CMW. \n
			:param bd_address: hex Range: #H0 to #HFFFFFFFFFFFF (12 hexadecimal digits)
		"""
		param = Conversions.value_to_str(bd_address)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:CMW {param}')

	def get_eut(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:EUT \n
		Snippet: value: str = driver.configure.connection.bdAddress.get_eut() \n
		Sets/gets the Bluetooth device address (BD_ADDR) of a default device to attempt a connection to. If no inquiry was made
		before, this BD_ADDR is used for paging; otherwise, the device to page can be set via method RsCmwBluetoothSig.Configure.
		Connection.Paging.Ptarget.value. \n
			:return: bd_address: hex Range: #H0 to #HFFFFFFFFFFFF (12 hexadecimal digits)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:EUT?')
		return trim_str_response(response)

	def set_eut(self, bd_address: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:EUT \n
		Snippet: driver.configure.connection.bdAddress.set_eut(bd_address = rawAbc) \n
		Sets/gets the Bluetooth device address (BD_ADDR) of a default device to attempt a connection to. If no inquiry was made
		before, this BD_ADDR is used for paging; otherwise, the device to page can be set via method RsCmwBluetoothSig.Configure.
		Connection.Paging.Ptarget.value. \n
			:param bd_address: hex Range: #H0 to #HFFFFFFFFFFFF (12 hexadecimal digits)
		"""
		param = Conversions.value_to_str(bd_address)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BDADdress:EUT {param}')
