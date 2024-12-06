# Copyright (c) 2024, Huawei Technologies Co., Ltd.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0  (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
class Constant(object):
    COLLECTION_PATH = "collection_path"
    ANALYSIS_MODE = "analysis_mode"
    CONTEXT_SETTINGS = dict(help_option_names=['-H', '-h', '--help'])

    MAX_FILE_SIZE_5_GB = 1024 * 1024 * 1024 * 5

    MODULE_EVENT = "module_event"
    CPU_OP_EVENT = "op_event"
    STEP_EVENT = "step_event"
    TORCH_TO_NPU_FLOW = "torch_to_device"
    KERNEL_EVENT = "kernel_event"
    HCCL_EVENT = "hccl_event"
    OVERLAP_ANALYSIS_EVENT = "overlap_event"
    FWD_BWD_FLOW = "fwd_to_bwd"
    NPU_ROOT_ID = "NPU"
    BACKWARD_MODULE = "nn.Module: BACKWARD"

    FWD_OR_OPT = 0
    BACKWARD = 1
    INVALID_RETURN = -1

    # node type
    MODULE_TYPE = 0
    OPERATOR_TYPE = 1
    VIRTUAL_TYPE = 9

    # trace bar
    NPU_BAR = "Ascend Hardware"
    HCCL_BAR = "HCCL"
    OVERLAP_BAR = "Overlap Analysis"

    # overlap_analysis event
    COMPUTING_EVENT = "Computing"
    FREE_EVENT = "Free"
    UNCOVERED_COMMUNICATION_EVENT = "Communication(Not Overlapped)"
