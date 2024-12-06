#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# Copyright (C) 2023-2024. Huawei Technologies Co., Ltd. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
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
"""


class Constant(object):
    GPU = "GPU"
    NPU = "NPU"
    NA = 'N/A'
    LIMIT_KERNEL = 3
    MAX_PATH_LENGTH = 4096
    MAX_FLOW_CAT_LEN = 20
    MAX_OP_NAME_LEN = 200
    MAX_FILE_SIZE = 1024 * 1024 * 1024 * 5
    MAX_JSON_SIZE = 1024 * 1024 * 1024 * 10
    BYTE_TO_KB = 1024
    YELLOW_COLOR = "FFFF00"
    GREEN_COLOR = "00FF00"
    RED_COLOR = "FF0000"
    BLUE_COLOR = "00BFFF"
    LIGHT_BLUE_COLOR = "87CEFA"
    US_TO_MS = 1000
    KB_TO_MB = 1024
    INVALID_VALUE = -1
    MILLISECONDS_TO_SECONDS = 10 ** 3
    MICROSECONDS_TO_SECONDS = 10 ** 6

    # epsilon
    EPS = 1e-15

    # autority
    FILE_AUTHORITY = 0o640
    DIR_AUTHORITY = 0o750

    PROFILING_TYPE = "profiling type"

    # path
    PROFILING_PATH = "profiling_path"
    TRACE_PATH = "trace_path"
    MEMORY_DATA_PATH = "memory_data_path"
    ASCEND_OUTPUT_PATH = "ascend_output"
    INFO_JSON_PATH = "info_path"

    # excel headers
    BASE_PROFILING = 'Base Profiling: '
    COMPARISON_PROFILING = 'Comparison Profiling: '
    WAIT_TIME = "wait"
    TRANSMIT_TIME = "transmit"

    # compare type
    OPERATOR_COMPARE = "OperatorCompare"
    MEMORY_COMPARE = "MemoryCompare"
    API_COMPARE = "ApiCompare"
    KERNEL_COMPARE = "KernelCompare"

    # sheet name
    OPERATOR_SHEET = "OperatorCompare"
    MEMORY_SHEET = "MemoryCompare"
    OPERATOR_TOP_SHEET = "OperatorCompareStatistic"
    MEMORY_TOP_SHEET = "MemoryCompareStatistic"
    COMMUNICATION_SHEET = "CommunicationCompare"
    API_SHEET = "ApiCompare"
    KERNEL_SHEET = "KernelCompare"

    # table name
    OPERATOR_TABLE = "OperatorCompare"
    MEMORY_TABLE = "MemoryCompare"
    OPERATOR_TOP_TABLE = "OperatorCompareStatistic"
    MEMORY_TOP_TABLE = "MemoryCompareStatistic"
    COMMUNICATION_TABLE = "CommunicationCompare"
    PERFORMANCE_TABLE = "Model Profiling Time Distribution"
    MODULE_TABLE = "ModuleCompare"
    MODULE_TOP_TABLE = "ModuleCompareStatistic"
    OVERALL_METRICS_TABLE = "OverallMetrics"
    API_TABLE = "ApiCompare"
    KERNEL_TABLE = "KernelCompare"

    # memory
    SIZE = "Size(KB)"
    TS = "ts"
    ALLOCATION_TIME = "Allocation Time(us)"
    RELEASE_TIME = "Release Time(us)"
    NAME = "Name"

    OP_KEY = "op_name"
    DEVICE_DUR = "dur"

    BASE_DATA = "base_data"
    COMPARISON_DATA = "comparison_data"
    OVERALL_METRICS = "overall_metrics"
    TORCH_OP = "torch_op"
    KERNEL_DICT = "kernel_dict"
    MEMORY_LIST = "memory_list"
    COMMUNICATION_DICT = "comm_dict"

    # compare type
    OVERALL_COMPARE = "overall"

    BWD_LIST = ["bwd", "backward", "back", "grad"]

    CPU_OP_FA_MASK = (
        "flash_attention", "fusion_attention", "flashattn", "xformers_flash", "efficient_attention", "flash2attn"
    )
    CPU_OP_CONV = "aten::conv"
    CPU_OP_MATMUL_MASK = ("aten::addmm", "aten::bmm", "aten::mm", "aten::matmul")
    KERNEL_CUBE_MASK = ("gemm", "conv", "cutlass", "wgrad", "gemvx")
    KERNEL_TRANS_MASK = ("cast", "transdata", "transpose")

    IS_BWD = "is_bwd"
    OPS = "ops"

    VOID_STEP = -1
