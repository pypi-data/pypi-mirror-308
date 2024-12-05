from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	# noinspection PyTypeChecker
	def get_lrange(self) -> enums.ModIndexType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LRANge \n
		Snippet: value: enums.ModIndexType = driver.configure.rfSettings.dtx.mindex.mode.tmode.lowEnergy.get_lrange() \n
		No command help available \n
			:return: mod_index_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LRANge?')
		return Conversions.str_to_scalar_enum(response, enums.ModIndexType)

	def set_lrange(self, mod_index_type: enums.ModIndexType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LRANge \n
		Snippet: driver.configure.rfSettings.dtx.mindex.mode.tmode.lowEnergy.set_lrange(mod_index_type = enums.ModIndexType.STAB) \n
		No command help available \n
			:param mod_index_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(mod_index_type, enums.ModIndexType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LRANge {param}')

	# noinspection PyTypeChecker
	def get_le_2_m(self) -> enums.ModIndexType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE2M \n
		Snippet: value: enums.ModIndexType = driver.configure.rfSettings.dtx.mindex.mode.tmode.lowEnergy.get_le_2_m() \n
		No command help available \n
			:return: mod_index_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE2M?')
		return Conversions.str_to_scalar_enum(response, enums.ModIndexType)

	def set_le_2_m(self, mod_index_type: enums.ModIndexType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE2M \n
		Snippet: driver.configure.rfSettings.dtx.mindex.mode.tmode.lowEnergy.set_le_2_m(mod_index_type = enums.ModIndexType.STAB) \n
		No command help available \n
			:param mod_index_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(mod_index_type, enums.ModIndexType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE2M {param}')

	# noinspection PyTypeChecker
	def get_le_1_m(self) -> enums.ModIndexType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE1M \n
		Snippet: value: enums.ModIndexType = driver.configure.rfSettings.dtx.mindex.mode.tmode.lowEnergy.get_le_1_m() \n
		No command help available \n
			:return: mod_index_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE1M?')
		return Conversions.str_to_scalar_enum(response, enums.ModIndexType)

	def set_le_1_m(self, mod_index_type: enums.ModIndexType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE1M \n
		Snippet: driver.configure.rfSettings.dtx.mindex.mode.tmode.lowEnergy.set_le_1_m(mod_index_type = enums.ModIndexType.STAB) \n
		No command help available \n
			:param mod_index_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(mod_index_type, enums.ModIndexType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:MINDex:MODE:TMODe:LENergy:LE1M {param}')
