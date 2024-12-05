from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AverageCls:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:PVTime:AVERage \n
		Snippet: value: List[float] = driver.csounding.trace.powerVsTime.average.read() \n
		Returns the values of the power vs time traces. The results of the current, average, minimum, and maximum traces can be
		retrieved. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pvt_trace: float N power vs time results. The number of results depends on the packet type and payload length. Range: -128.0 dBm to 30.0 dBm , Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:PVTime:AVERage?', suppressed)
		return response

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:PVTime:AVERage \n
		Snippet: value: List[float] = driver.csounding.trace.powerVsTime.average.fetch() \n
		Returns the values of the power vs time traces. The results of the current, average, minimum, and maximum traces can be
		retrieved. \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: pvt_trace: float N power vs time results. The number of results depends on the packet type and payload length. Range: -128.0 dBm to 30.0 dBm , Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:TRACe:PVTime:AVERage?', suppressed)
		return response
