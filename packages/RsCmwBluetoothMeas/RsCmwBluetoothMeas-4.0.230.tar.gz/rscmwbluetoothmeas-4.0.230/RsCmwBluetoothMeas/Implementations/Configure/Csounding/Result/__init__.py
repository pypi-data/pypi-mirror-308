from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ResultCls:
	"""Result commands group definition. 6 total commands, 1 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("result", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	def get_sphase(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SPHase \n
		Snippet: value: bool = driver.configure.csounding.result.get_sphase() \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SPHase?')
		return Conversions.str_to_bool(response)

	def set_sphase(self, state: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SPHase \n
		Snippet: driver.configure.csounding.result.set_sphase(state = False) \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SPHase {param}')

	def get_sfrequency(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SFRequency \n
		Snippet: value: bool = driver.configure.csounding.result.get_sfrequency() \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SFRequency?')
		return Conversions.str_to_bool(response)

	def set_sfrequency(self, state: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SFRequency \n
		Snippet: driver.configure.csounding.result.set_sfrequency(state = False) \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:SFRequency {param}')

	def get_mspectrum(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:MSPectrum \n
		Snippet: value: bool = driver.configure.csounding.result.get_mspectrum() \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:MSPectrum?')
		return Conversions.str_to_bool(response)

	def set_mspectrum(self, state: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:MSPectrum \n
		Snippet: driver.configure.csounding.result.set_mspectrum(state = False) \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:MSPectrum {param}')

	def get_power_vs_time(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVTime \n
		Snippet: value: bool = driver.configure.csounding.result.get_power_vs_time() \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVTime?')
		return Conversions.str_to_bool(response)

	def set_power_vs_time(self, state: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVTime \n
		Snippet: driver.configure.csounding.result.set_power_vs_time(state = False) \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVTime {param}')

	def get_pva_path(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVAPath \n
		Snippet: value: bool = driver.configure.csounding.result.get_pva_path() \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVAPath?')
		return Conversions.str_to_bool(response)

	def set_pva_path(self, state: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVAPath \n
		Snippet: driver.configure.csounding.result.set_pva_path(state = False) \n
		Enables or disables the evaluation of results in the channel sounding measurements. The last mnemonic denotes the
		measurement type: Modulation spectrum results, power vs antenna path results, power vs time results, step frequency
		results, stable phase results. Use method RsCmwBluetoothMeas.Configure.Csounding.Result.All.set to enable/disable all
		result types. Tip: Use READ...? queries to retrieve results for disabled measurements. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:PVAPath {param}')

	def clone(self) -> 'ResultCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ResultCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
