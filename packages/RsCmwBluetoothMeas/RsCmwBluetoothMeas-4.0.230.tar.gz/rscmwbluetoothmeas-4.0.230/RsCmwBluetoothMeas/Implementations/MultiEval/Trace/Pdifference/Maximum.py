from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaximumCls:
	"""Maximum commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDIFference:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.pdifference.maximum.fetch() \n
		Returns the values of the phase difference traces. The results of the current, average minimum and maximum traces can be
		retrieved. The phase difference traces are available for EDR bursts (method RsCmwBluetoothMeas.Configure.InputSignal.
		btype EDR) . \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: phase_difference: float N phase difference results, depending on the packet type and payload length; see 'Phase difference trace points (EDR) '. Range: -1.00 rad/Pi to 1.00 rad/Pi , Unit: rad/Pi"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDIFference:MAXimum?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDIFference:MAXimum \n
		Snippet: value: List[float] = driver.multiEval.trace.pdifference.maximum.read() \n
		Returns the values of the phase difference traces. The results of the current, average minimum and maximum traces can be
		retrieved. The phase difference traces are available for EDR bursts (method RsCmwBluetoothMeas.Configure.InputSignal.
		btype EDR) . \n
		Use RsCmwBluetoothMeas.reliability.last_value to read the updated reliability indicator. \n
			:return: phase_difference: float N phase difference results, depending on the packet type and payload length; see 'Phase difference trace points (EDR) '. Range: -1.00 rad/Pi to 1.00 rad/Pi , Unit: rad/Pi"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:TRACe:PDIFference:MAXimum?', suppressed)
		return response
