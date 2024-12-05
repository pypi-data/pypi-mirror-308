from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StErrorCls:
	"""StError commands group definition. 11 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stError", core, parent)

	@property
	def nmode(self):
		"""nmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmode'):
			from .Nmode import NmodeCls
			self._nmode = NmodeCls(self._core, self._cmd_group)
		return self._nmode

	@property
	def tmode(self):
		"""tmode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import TmodeCls
			self._tmode = TmodeCls(self._core, self._cmd_group)
		return self._tmode

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	# noinspection PyTypeChecker
	def get_edrate(self) -> enums.SymbolTimeError:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:EDRate \n
		Snippet: value: enums.SymbolTimeError = driver.configure.rfSettings.dtx.sing.stError.get_edrate() \n
		Specify the symbol timing error of the signal. \n
			:return: symbol_time_err: OFF | NEG20 | POS20 No symbol timing error, - 20 ppm or 20 ppm
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:EDRate?')
		return Conversions.str_to_scalar_enum(response, enums.SymbolTimeError)

	def set_edrate(self, symbol_time_err: enums.SymbolTimeError) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:EDRate \n
		Snippet: driver.configure.rfSettings.dtx.sing.stError.set_edrate(symbol_time_err = enums.SymbolTimeError.NEG20) \n
		Specify the symbol timing error of the signal. \n
			:param symbol_time_err: OFF | NEG20 | POS20 No symbol timing error, - 20 ppm or 20 ppm
		"""
		param = Conversions.enum_scalar_to_str(symbol_time_err, enums.SymbolTimeError)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:EDRate {param}')

	# noinspection PyTypeChecker
	def get_brate(self) -> enums.SymbolTimeError:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:BRATe \n
		Snippet: value: enums.SymbolTimeError = driver.configure.rfSettings.dtx.sing.stError.get_brate() \n
		Specify the symbol timing error of the signal. \n
			:return: symbol_time_err: OFF | NEG20 | POS20 No symbol timing error, - 20 ppm or 20 ppm
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:BRATe?')
		return Conversions.str_to_scalar_enum(response, enums.SymbolTimeError)

	def set_brate(self, symbol_time_err: enums.SymbolTimeError) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:BRATe \n
		Snippet: driver.configure.rfSettings.dtx.sing.stError.set_brate(symbol_time_err = enums.SymbolTimeError.NEG20) \n
		Specify the symbol timing error of the signal. \n
			:param symbol_time_err: OFF | NEG20 | POS20 No symbol timing error, - 20 ppm or 20 ppm
		"""
		param = Conversions.enum_scalar_to_str(symbol_time_err, enums.SymbolTimeError)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:STERror:BRATe {param}')

	def clone(self) -> 'StErrorCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StErrorCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
