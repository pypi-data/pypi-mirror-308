from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CdirectionCls:
	"""Cdirection commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cdirection", core, parent)

	# noinspection PyTypeChecker
	def get_le_signaling(self) -> enums.LeSigDirection:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CDIRection:LESignaling \n
		Snippet: value: enums.LeSigDirection = driver.configure.connection.audio.cdirection.get_le_signaling() \n
		Sets the direction for LE audio connections. \n
			:return: direction: DUPLex | UPLink | DOWNlink Both directions, uplink only, downlink only
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CDIRection:LESignaling?')
		return Conversions.str_to_scalar_enum(response, enums.LeSigDirection)

	def set_le_signaling(self, direction: enums.LeSigDirection) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CDIRection:LESignaling \n
		Snippet: driver.configure.connection.audio.cdirection.set_le_signaling(direction = enums.LeSigDirection.DOWNlink) \n
		Sets the direction for LE audio connections. \n
			:param direction: DUPLex | UPLink | DOWNlink Both directions, uplink only, downlink only
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.LeSigDirection)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:CDIRection:LESignaling {param}')
