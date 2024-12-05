from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioCls:
	"""Audio commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("audio", core, parent)

	# noinspection PyTypeChecker
	def get_prf_role(self) -> enums.ProfileRole:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:PRFRole \n
		Snippet: value: enums.ProfileRole = driver.configure.audio.get_prf_role() \n
		Specifies the audio profile role of the DUT. \n
			:return: profile_role: HNDFree | ADGate | ASINk Hands free, hands free - audio gateway, A2DP sink, BAP
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:PRFRole?')
		return Conversions.str_to_scalar_enum(response, enums.ProfileRole)

	def set_prf_role(self, profile_role: enums.ProfileRole) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:PRFRole \n
		Snippet: driver.configure.audio.set_prf_role(profile_role = enums.ProfileRole.ADGate) \n
		Specifies the audio profile role of the DUT. \n
			:param profile_role: HNDFree | ADGate | ASINk Hands free, hands free - audio gateway, A2DP sink, BAP
		"""
		param = Conversions.enum_scalar_to_str(profile_role, enums.ProfileRole)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:PRFRole {param}')

	# noinspection PyTypeChecker
	def get_cmw_role(self) -> enums.PriorityRole:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:CMWRole \n
		Snippet: value: enums.PriorityRole = driver.configure.audio.get_cmw_role() \n
		No command help available \n
			:return: cmw_role: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:CMWRole?')
		return Conversions.str_to_scalar_enum(response, enums.PriorityRole)

	def set_cmw_role(self, cmw_role: enums.PriorityRole) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:CMWRole \n
		Snippet: driver.configure.audio.set_cmw_role(cmw_role = enums.PriorityRole.MASTer) \n
		No command help available \n
			:param cmw_role: No help available
		"""
		param = Conversions.enum_scalar_to_str(cmw_role, enums.PriorityRole)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:AUDio:CMWRole {param}')
