from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsoundingCls:
	"""Csounding commands group definition. 5 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csounding", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import CatalogCls
			self._catalog = CatalogCls(self._core, self._cmd_group)
		return self._catalog

	def get_threshold(self) -> float or bool:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:THReshold \n
		Snippet: value: float or bool = driver.trigger.csounding.get_threshold() \n
		Defines the trigger threshold for the power trigger. \n
			:return: power: (float or boolean) float | ON | OFF Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:THReshold?')
		return Conversions.str_to_float_or_bool(response)

	def set_threshold(self, power: float or bool) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:THReshold \n
		Snippet: driver.trigger.csounding.set_threshold(power = 1.0) \n
		Defines the trigger threshold for the power trigger. \n
			:param power: (float or boolean) float | ON | OFF Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to reference level minus external attenuation)
		"""
		param = Conversions.decimal_or_bool_value_to_str(power)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:THReshold {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.csounding.get_slope() \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse (valid for
		external and power trigger sources) . \n
			:return: slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SLOPe \n
		Snippet: driver.trigger.csounding.set_slope(slope = enums.SignalSlope.FEDGe) \n
		Qualifies whether the trigger event is generated at the rising or at the falling edge of the trigger pulse (valid for
		external and power trigger sources) . \n
			:param slope: REDGe | FEDGe REDGe: Rising edge FEDGe: Falling edge
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SLOPe {param}')

	def get_timeout(self) -> int or bool:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:TOUT \n
		Snippet: value: int or bool = driver.trigger.csounding.get_timeout() \n
		Selects the maximum time that the measurement waits for a trigger event before it stops in remote control mode or
		indicates a trigger timeout in manual operation mode. \n
			:return: timeout: (integer or boolean) float | ON | OFF Range: 0.01 s to 167.77215E+3 s Additional parameters: OFF | ON (disables timeout | enables timeout using the previous/default values) .
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:TOUT?')
		return Conversions.str_to_int_or_bool(response)

	def set_timeout(self, timeout: int or bool) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:TOUT \n
		Snippet: driver.trigger.csounding.set_timeout(timeout = 1) \n
		Selects the maximum time that the measurement waits for a trigger event before it stops in remote control mode or
		indicates a trigger timeout in manual operation mode. \n
			:param timeout: (integer or boolean) float | ON | OFF Range: 0.01 s to 167.77215E+3 s Additional parameters: OFF | ON (disables timeout | enables timeout using the previous/default values) .
		"""
		param = Conversions.decimal_or_bool_value_to_str(timeout)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:TOUT {param}')

	def get_source(self) -> str:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SOURce \n
		Snippet: value: str = driver.trigger.csounding.get_source() \n
		Selects the source of the trigger events. Some values are always available. They are listed below. Depending on the
		installed options, additional values are available. You can query a list of all supported values via TRIGger:...
		:CATalog:SOURce?. In combined signal path, the Bluetooth signaling application can also provide the suitable trigger. \n
			:return: source: string 'Power': power trigger (received RF power)
		"""
		response = self._core.io.query_str('TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SOURce \n
		Snippet: driver.trigger.csounding.set_source(source = 'abc') \n
		Selects the source of the trigger events. Some values are always available. They are listed below. Depending on the
		installed options, additional values are available. You can query a list of all supported values via TRIGger:...
		:CATalog:SOURce?. In combined signal path, the Bluetooth signaling application can also provide the suitable trigger. \n
			:param source: string 'Power': power trigger (received RF power)
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:BLUetooth:MEASurement<Instance>:CSOunding:SOURce {param}')

	def clone(self) -> 'CsoundingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsoundingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
