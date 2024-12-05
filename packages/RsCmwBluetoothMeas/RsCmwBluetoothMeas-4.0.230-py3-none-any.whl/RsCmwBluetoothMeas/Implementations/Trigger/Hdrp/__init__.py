from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HdrpCls:
	"""Hdrp commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hdrp", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	def get_threshold(self) -> float or bool:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:HDRP:THReshold \n
		Snippet: value: float or bool = driver.trigger.hdrp.get_threshold() \n
		No command help available \n
			:return: power: (float or boolean) No help available
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:HDRP:THReshold?')
		return Conversions.str_to_float_or_bool(response)

	def set_threshold(self, power: float or bool) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:HDRP:THReshold \n
		Snippet: driver.trigger.hdrp.set_threshold(power = 1.0) \n
		No command help available \n
			:param power: (float or boolean) No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(power)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:HDRP:THReshold {param}')

	def get_timeout(self) -> int or bool:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:HDRP:TOUT \n
		Snippet: value: int or bool = driver.trigger.hdrp.get_timeout() \n
		No command help available \n
			:return: timeout: (integer or boolean) No help available
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:HDRP:TOUT?')
		return Conversions.str_to_int_or_bool(response)

	def set_timeout(self, timeout: int or bool) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:HDRP:TOUT \n
		Snippet: driver.trigger.hdrp.set_timeout(timeout = 1) \n
		No command help available \n
			:param timeout: (integer or boolean) No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(timeout)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:HDRP:TOUT {param}')

	def get_source(self) -> str:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:HDRP:SOURce \n
		Snippet: value: str = driver.trigger.hdrp.get_source() \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:HDRP:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:HDRP:SOURce \n
		Snippet: driver.trigger.hdrp.set_source(source = 'abc') \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:HDRP:SOURce {param}')

	def clone(self) -> 'HdrpCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HdrpCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
