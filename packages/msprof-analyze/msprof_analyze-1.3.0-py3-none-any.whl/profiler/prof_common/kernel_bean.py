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
from profiler.prof_common.utils import convert_to_decimal


class KernelBean:
    def __init__(self, data: dict):
        self._name = data.get("Name", "")
        self._op_type = data.get("Type", "")
        self._core_type = data.get("Accelerator Core", "")
        self._input_shape = data.get("Input Shapes", "").replace("\"", "")
        self._input_type = data.get("Input Data Types", "")
        self._input_format = data.get("Input Formats", "")
        self._duration = data.get("Duration(us)", 0)
        self._ts = data.get("Start Time(us)", "")

    @property
    def start_time(self):
        return convert_to_decimal(self._ts)

    @property
    def end_time(self):
        return self.start_time + convert_to_decimal(self.dur)

    @property
    def is_computing_op(self):
        return self._core_type != "HCCL"

    @property
    def dur(self):
        return float(self._duration)

    @property
    def kernel_info(self):
        return [self._name, self._op_type, self._core_type, self._input_shape, self._input_type, self.dur]
