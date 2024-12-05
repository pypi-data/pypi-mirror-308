from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LeSignalingCls:
	"""LeSignaling commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("leSignaling", core, parent)

	def get_ccentral(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CCENtral \n
		Snippet: value: bool = driver.configure.connection.iencryption.leSignaling.get_ccentral() \n
		Indicates the R&S CMW support of encryption in central (..:CCENtral) or peripheral (..:CPERipheral) LE role. The command
		is relevant for LE connection tests. \n
			:return: ind_encryption: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CCENtral?')
		return Conversions.str_to_bool(response)

	def set_ccentral(self, ind_encryption: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CCENtral \n
		Snippet: driver.configure.connection.iencryption.leSignaling.set_ccentral(ind_encryption = False) \n
		Indicates the R&S CMW support of encryption in central (..:CCENtral) or peripheral (..:CPERipheral) LE role. The command
		is relevant for LE connection tests. \n
			:param ind_encryption: OFF | ON
		"""
		param = Conversions.bool_to_str(ind_encryption)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CCENtral {param}')

	def get_cperipheral(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CPERipheral \n
		Snippet: value: bool = driver.configure.connection.iencryption.leSignaling.get_cperipheral() \n
		Indicates the R&S CMW support of encryption in central (..:CCENtral) or peripheral (..:CPERipheral) LE role. The command
		is relevant for LE connection tests. \n
			:return: ind_encryption: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CPERipheral?')
		return Conversions.str_to_bool(response)

	def set_cperipheral(self, ind_encryption: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CPERipheral \n
		Snippet: driver.configure.connection.iencryption.leSignaling.set_cperipheral(ind_encryption = False) \n
		Indicates the R&S CMW support of encryption in central (..:CCENtral) or peripheral (..:CPERipheral) LE role. The command
		is relevant for LE connection tests. \n
			:param ind_encryption: OFF | ON
		"""
		param = Conversions.bool_to_str(ind_encryption)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:IENCryption:LESignaling:CPERipheral {param}')
