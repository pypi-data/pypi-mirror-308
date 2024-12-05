from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScountCls:
	"""Scount commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scount", core, parent)

	def get_sphase(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SPHase \n
		Snippet: value: int = driver.configure.csounding.scount.get_sphase() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:return: stat_count: numeric Number of measurement intervals
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SPHase?')
		return Conversions.str_to_int(response)

	def set_sphase(self, stat_count: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SPHase \n
		Snippet: driver.configure.csounding.scount.set_sphase(stat_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:param stat_count: numeric Number of measurement intervals
		"""
		param = Conversions.decimal_value_to_str(stat_count)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SPHase {param}')

	def get_sfrequency(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SFRequency \n
		Snippet: value: int = driver.configure.csounding.scount.get_sfrequency() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:return: stat_count: numeric Number of measurement intervals
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SFRequency?')
		return Conversions.str_to_int(response)

	def set_sfrequency(self, stat_count: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SFRequency \n
		Snippet: driver.configure.csounding.scount.set_sfrequency(stat_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:param stat_count: numeric Number of measurement intervals
		"""
		param = Conversions.decimal_value_to_str(stat_count)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:SFRequency {param}')

	def get_mspectrum(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:MSPectrum \n
		Snippet: value: int = driver.configure.csounding.scount.get_mspectrum() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:return: stat_count: numeric Number of measurement intervals
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:MSPectrum?')
		return Conversions.str_to_int(response)

	def set_mspectrum(self, stat_count: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:MSPectrum \n
		Snippet: driver.configure.csounding.scount.set_mspectrum(stat_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:param stat_count: numeric Number of measurement intervals
		"""
		param = Conversions.decimal_value_to_str(stat_count)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:MSPectrum {param}')

	def get_power(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:POWer \n
		Snippet: value: int = driver.configure.csounding.scount.get_power() \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:return: stat_count: numeric Number of measurement intervals
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:POWer?')
		return Conversions.str_to_int(response)

	def set_power(self, stat_count: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:POWer \n
		Snippet: driver.configure.csounding.scount.set_power(stat_count = 1) \n
		Specifies the statistic count of the measurement. The statistic count is equal to the number of measurement intervals per
		single shot. The last mnemonic denotes the measurement type: Modulation spectrum, power vs time, step frequency, and
		stable phase measurement. \n
			:param stat_count: numeric Number of measurement intervals
		"""
		param = Conversions.decimal_value_to_str(stat_count)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:SCOunt:POWer {param}')
