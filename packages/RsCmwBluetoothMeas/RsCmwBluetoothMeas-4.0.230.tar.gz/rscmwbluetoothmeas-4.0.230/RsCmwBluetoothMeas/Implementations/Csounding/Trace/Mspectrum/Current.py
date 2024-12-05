from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:MSPectrum:CURRent \n
		Snippet: value: List[float] = driver.csounding.trace.mspectrum.current.read() \n
		Returns the values of the modulation spectrum traces. The results of the current, average, and maximum traces can be
		retrieved. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: sacp_trace: float N spectrum ACP results. The number of results depends on the packet type and payload length. Range: -99.99 dB to 99.99 dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:MSPectrum:CURRent?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:MSPectrum:CURRent \n
		Snippet: value: List[float] = driver.csounding.trace.mspectrum.current.fetch() \n
		Returns the values of the modulation spectrum traces. The results of the current, average, and maximum traces can be
		retrieved. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: sacp_trace: float N spectrum ACP results. The number of results depends on the packet type and payload length. Range: -99.99 dB to 99.99 dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:MSPectrum:CURRent?', suppressed)
		return response
