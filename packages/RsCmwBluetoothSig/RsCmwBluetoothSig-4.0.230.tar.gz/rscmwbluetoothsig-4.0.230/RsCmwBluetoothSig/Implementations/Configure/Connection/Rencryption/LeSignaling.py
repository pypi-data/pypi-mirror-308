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
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CCENtral \n
		Snippet: value: bool = driver.configure.connection.rencryption.leSignaling.get_ccentral() \n
		Specifies, whether the encryption request from the EUT is accepted or rejected by the R&S CMW in central (..:CCENtral) or
		peripheral (..:CPERipheral) LE role. The command is relevant for LE connection tests. \n
			:return: rej_encryption: OFF | ON OFF: accept encryption request ON: reject encryption request
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CCENtral?')
		return Conversions.str_to_bool(response)

	def set_ccentral(self, rej_encryption: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CCENtral \n
		Snippet: driver.configure.connection.rencryption.leSignaling.set_ccentral(rej_encryption = False) \n
		Specifies, whether the encryption request from the EUT is accepted or rejected by the R&S CMW in central (..:CCENtral) or
		peripheral (..:CPERipheral) LE role. The command is relevant for LE connection tests. \n
			:param rej_encryption: OFF | ON OFF: accept encryption request ON: reject encryption request
		"""
		param = Conversions.bool_to_str(rej_encryption)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CCENtral {param}')

	def get_cperipheral(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CPERipheral \n
		Snippet: value: bool = driver.configure.connection.rencryption.leSignaling.get_cperipheral() \n
		Specifies, whether the encryption request from the EUT is accepted or rejected by the R&S CMW in central (..:CCENtral) or
		peripheral (..:CPERipheral) LE role. The command is relevant for LE connection tests. \n
			:return: rej_encryption: OFF | ON OFF: accept encryption request ON: reject encryption request
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CPERipheral?')
		return Conversions.str_to_bool(response)

	def set_cperipheral(self, rej_encryption: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CPERipheral \n
		Snippet: driver.configure.connection.rencryption.leSignaling.set_cperipheral(rej_encryption = False) \n
		Specifies, whether the encryption request from the EUT is accepted or rejected by the R&S CMW in central (..:CCENtral) or
		peripheral (..:CPERipheral) LE role. The command is relevant for LE connection tests. \n
			:param rej_encryption: OFF | ON OFF: accept encryption request ON: reject encryption request
		"""
		param = Conversions.bool_to_str(rej_encryption)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:RENCryption:LESignaling:CPERipheral {param}')
