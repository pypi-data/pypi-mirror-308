from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CsoundingCls:
	"""Csounding commands group definition. 75 total commands, 7 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("csounding", core, parent)

	@property
	def trace(self):
		"""trace commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import TraceCls
			self._trace = TraceCls(self._core, self._cmd_group)
		return self._trace

	@property
	def sphase(self):
		"""sphase commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sphase'):
			from .Sphase import SphaseCls
			self._sphase = SphaseCls(self._core, self._cmd_group)
		return self._sphase

	@property
	def mspectrum(self):
		"""mspectrum commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mspectrum'):
			from .Mspectrum import MspectrumCls
			self._mspectrum = MspectrumCls(self._core, self._cmd_group)
		return self._mspectrum

	@property
	def sfrequency(self):
		"""sfrequency commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sfrequency'):
			from .Sfrequency import SfrequencyCls
			self._sfrequency = SfrequencyCls(self._core, self._cmd_group)
		return self._sfrequency

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .PowerVsTime import PowerVsTimeCls
			self._powerVsTime = PowerVsTimeCls(self._core, self._cmd_group)
		return self._powerVsTime

	@property
	def pvaPath(self):
		"""pvaPath commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pvaPath'):
			from .PvaPath import PvaPathCls
			self._pvaPath = PvaPathCls(self._core, self._cmd_group)
		return self._pvaPath

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def abort(self) -> None:
		"""SCPI: ABORt:BLUetooth:MEASurement<Instance>:CSOunding \n
		Snippet: driver.csounding.abort() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'ABORt:BLUetooth:MEASurement<Instance>:CSOunding')

	def abort_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:BLUetooth:MEASurement<Instance>:CSOunding \n
		Snippet: driver.csounding.abort_with_opc() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:BLUetooth:MEASurement<Instance>:CSOunding', opc_timeout_ms)

	def stop(self) -> None:
		"""SCPI: STOP:BLUetooth:MEASurement<Instance>:CSOunding \n
		Snippet: driver.csounding.stop() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'STOP:BLUetooth:MEASurement<Instance>:CSOunding')

	def stop_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:BLUetooth:MEASurement<Instance>:CSOunding \n
		Snippet: driver.csounding.stop_with_opc() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:BLUetooth:MEASurement<Instance>:CSOunding', opc_timeout_ms)

	def initiate(self) -> None:
		"""SCPI: INITiate:BLUetooth:MEASurement<Instance>:CSOunding \n
		Snippet: driver.csounding.initiate() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		"""
		self._core.io.write(f'INITiate:BLUetooth:MEASurement<Instance>:CSOunding')

	def initiate_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:BLUetooth:MEASurement<Instance>:CSOunding \n
		Snippet: driver.csounding.initiate_with_opc() \n
			INTRO_CMD_HELP: Starts, stops or aborts the measurement: \n
			- INITiate... starts or restarts the measurement. The measurement enters the 'RUN' state.
			- STOP... halts the measurement immediately. The measurement enters the 'RDY' state. Measurement results are kept. The resources remain allocated to the measurement.
			- ABORt... halts the measurement immediately. The measurement enters the 'OFF' state. All measurement values are set to NAV. Allocated resources are released.
		Use FETCh...STATe? to query the current measurement state. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCmwBluetoothMeas.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:BLUetooth:MEASurement<Instance>:CSOunding', opc_timeout_ms)

	def clone(self) -> 'CsoundingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CsoundingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
