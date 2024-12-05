from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsoundingCls:
	"""Csounding commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csounding", core, parent)

	def get_mag_delay(self) -> float:
		"""SCPI: DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:MAGDelay \n
		Snippet: value: float = driver.diagnostic.csounding.get_mag_delay() \n
		No command help available \n
			:return: magic_deplay: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:MAGDelay?')
		return Conversions.str_to_float(response)

	def set_mag_delay(self, magic_deplay: float) -> None:
		"""SCPI: DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:MAGDelay \n
		Snippet: driver.diagnostic.csounding.set_mag_delay(magic_deplay = 1.0) \n
		No command help available \n
			:param magic_deplay: No help available
		"""
		param = Conversions.decimal_value_to_str(magic_deplay)
		self._core.io.write(f'DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:MAGDelay {param}')

	def get_rsz_period(self) -> float:
		"""SCPI: DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:RSZPeriod \n
		Snippet: value: float = driver.diagnostic.csounding.get_rsz_period() \n
		No command help available \n
			:return: rsz_period: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:RSZPeriod?')
		return Conversions.str_to_float(response)

	def set_rsz_period(self, rsz_period: float) -> None:
		"""SCPI: DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:RSZPeriod \n
		Snippet: driver.diagnostic.csounding.set_rsz_period(rsz_period = 1.0) \n
		No command help available \n
			:param rsz_period: No help available
		"""
		param = Conversions.decimal_value_to_str(rsz_period)
		self._core.io.write(f'DIAGnostic:BLUetooth:MEASurement<Instance>:CSOunding:RSZPeriod {param}')
