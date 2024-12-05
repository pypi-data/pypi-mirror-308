from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RoleCls:
	"""Role commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("role", core, parent)

	# noinspection PyTypeChecker
	def get_le_signaling(self) -> enums.SignalingCmwRole:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE:LESignaling \n
		Snippet: value: enums.SignalingCmwRole = driver.configure.connection.cmw.role.get_le_signaling() \n
		Sets the LE role of the instrument for LE connection tests. \n
			:return: sig_cmw_role: CENTral | PERipheral
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.SignalingCmwRole)

	def set_le_signaling(self, sig_cmw_role: enums.SignalingCmwRole) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE:LESignaling \n
		Snippet: driver.configure.connection.cmw.role.set_le_signaling(sig_cmw_role = enums.SignalingCmwRole.CENTral) \n
		Sets the LE role of the instrument for LE connection tests. \n
			:param sig_cmw_role: CENTral | PERipheral
		"""
		param = Conversions.enum_scalar_to_str(sig_cmw_role, enums.SignalingCmwRole)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE:LESignaling {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.PriorityRole:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE \n
		Snippet: value: enums.PriorityRole = driver.configure.connection.cmw.role.get_value() \n
		Specifies the connection control role of the R&S CMW for audio connections. \n
			:return: role: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE?')
		return Conversions.str_to_scalar_enum(response, enums.PriorityRole)

	def set_value(self, role: enums.PriorityRole) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE \n
		Snippet: driver.configure.connection.cmw.role.set_value(role = enums.PriorityRole.MASTer) \n
		Specifies the connection control role of the R&S CMW for audio connections. \n
			:param role: MASTer | SLAVe
		"""
		param = Conversions.enum_scalar_to_str(role, enums.PriorityRole)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:CMW:ROLE {param}')
