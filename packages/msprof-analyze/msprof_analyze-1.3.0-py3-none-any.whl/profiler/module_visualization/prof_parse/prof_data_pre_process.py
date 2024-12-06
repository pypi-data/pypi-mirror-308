# Copyright (c) 2024 Huawei Technologies Co., Ltd
# All rights reserved.
#
# Licensed under the BSD 3-Clause License  (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os

from profiler.prof_common.file_reader import FileReader
from profiler.prof_common.constant import Constant
from profiler.prof_common.kernel_bean import KernelBean
from profiler.prof_common.trace_event_bean import TraceEventBean


class ProfDataPreProcess:
    def __init__(self, prof_data_path: str):
        self._prof_data_path = prof_data_path
        self._trace_path = ""
        self._kernel_details_path = ""
        self._kernel_pid = None
        self._hccl_pid = None
        self._overlap_analysis_pid = None
        self._result_data = {Constant.CPU_OP_EVENT: [], Constant.MODULE_EVENT: [], Constant.KERNEL_EVENT: [],
                             Constant.TORCH_TO_NPU_FLOW: {}, Constant.FWD_BWD_FLOW: {}, Constant.HCCL_EVENT: [],
                             Constant.OVERLAP_ANALYSIS_EVENT: [], Constant.STEP_EVENT: []}

    @staticmethod
    def _check_trace_data(trace_data):
        if not isinstance(trace_data, list):
            msg = f"Invalid profiling data path, this feature only supports performance data " \
                  f"collected by Ascend PyTorch Profiler."
            raise RuntimeError(msg)

    def run(self) -> dict:
        self._check_trace_path()
        self._parse_trace_events()
        self._parse_kernel_details()
        self._check_result_data()
        return self._result_data

    def _check_trace_path(self):
        if os.path.isfile(self._prof_data_path):
            (split_file_path, split_file_name) = os.path.split(self._prof_data_path)
            (shot_name, extension) = os.path.splitext(split_file_name)
            if extension != ".json":
                msg = f"Invalid profiling path suffix: {self._prof_data_path}. " \
                      f"You should input in a json file path, such as trace_view.json."
                raise RuntimeError(msg)
            self._trace_path = self._prof_data_path
            return
        ascend_output = os.path.join(self._prof_data_path, "ASCEND_PROFILER_OUTPUT")
        profiler_output = ascend_output if os.path.isdir(ascend_output) else self._prof_data_path
        json_path = os.path.join(profiler_output, "trace_view.json")
        if not os.path.isfile(json_path):
            msg = f"Invalid profiling path: {self._prof_data_path}. The data path should be the " \
                  f"folder that ends with the ascend_pt collected by the Ascend PyTorch Profiler."
            raise RuntimeError(msg)
        kernel_path = os.path.join(profiler_output, "kernel_details.csv")
        if os.path.isfile(kernel_path):
            self._kernel_details_path = kernel_path
        self._trace_path = json_path

    def _parse_trace_events(self):
        trace_data = FileReader.read_json_file(self._trace_path)
        self._check_trace_data(trace_data)
        iter_trace_data = [TraceEventBean(data) for data in trace_data]
        for event in iter_trace_data:
            if self._kernel_pid is not None and self._hccl_pid is not None and self._overlap_analysis_pid is not None:
                break
            if not event.is_meta():
                continue
            if event.is_npu_process():
                self._kernel_pid = event.pid
            elif event.is_hccl_process():
                self._hccl_pid = event.pid
            elif event.is_overlap_analysis_process():
                self._overlap_analysis_pid = event.pid
        if self._kernel_pid is None:
            msg = "There is no operator on the NPU side for this data, please check whether the NPU switch is enabled."
            raise RuntimeError(msg)
        for event in iter_trace_data:
            if event.is_optimizer():
                event.event_type = Constant.MODULE_TYPE
                self._result_data[Constant.MODULE_EVENT].append(event)
            elif event.is_cpu_op():
                if event.is_step():
                    self._result_data[Constant.STEP_EVENT].append(event)
                else:
                    event.event_type = Constant.OPERATOR_TYPE
                    self._result_data[Constant.CPU_OP_EVENT].append(event)
            elif event.is_nn_module():
                event.event_type = Constant.MODULE_TYPE
                self._result_data[Constant.MODULE_EVENT].append(event)
            elif event.is_torch_to_npu():
                if event.is_flow_start():
                    self._result_data[Constant.TORCH_TO_NPU_FLOW].setdefault(event.id, {})["start"] = event
                else:
                    self._result_data[Constant.TORCH_TO_NPU_FLOW].setdefault(event.id, {})["end"] = event
            elif event.is_fwd_bwd_flow():
                if event.is_flow_start():
                    self._result_data[Constant.FWD_BWD_FLOW].setdefault(event.id, {})["start"] = event
                else:
                    self._result_data[Constant.FWD_BWD_FLOW].setdefault(event.id, {})["end"] = event
            elif event.is_kernel_event(self._kernel_pid):
                self._result_data[Constant.KERNEL_EVENT].append(event)
            elif event.is_hccl_event(self._hccl_pid):
                self._result_data[Constant.HCCL_EVENT].append(event)
            elif event.is_overlap_analysis_event(self._overlap_analysis_pid):
                self._result_data[Constant.OVERLAP_ANALYSIS_EVENT].append(event)

    def _parse_kernel_details(self):
        if not self._kernel_details_path:
            return
        try:
            all_kernels = FileReader.read_csv_file(self._kernel_details_path, KernelBean)
        except Exception as e:
            logging.error(e)
        kernels = list(filter(lambda x: x.is_computing_op, all_kernels))
        if kernels:
            self._result_data[Constant.KERNEL_EVENT] = kernels

    def _check_result_data(self):
        if not self._result_data.get(Constant.CPU_OP_EVENT):
            msg = "This data does not have any aten operator, please make sure to enable the CPU switch."
            raise RuntimeError(msg)
        if not [event for event in self._result_data.get(Constant.MODULE_EVENT) if event.is_nn_module()]:
            msg = "This data does not collect any modules, please make sure to enable the with_stack or with_modules."
            raise RuntimeError(msg)
