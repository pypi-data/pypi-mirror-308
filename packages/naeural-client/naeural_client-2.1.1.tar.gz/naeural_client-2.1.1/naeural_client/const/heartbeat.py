"""
This is the inter-repo portable constant file for heartbeats 
"""

HEARTBEAT_VERSION = 'HEARTBEAT_VERSION'
V1 = 'v1'
V2 = 'v2'

# ALERTS
IS_ALERT_RAM = 'IS_ALERT_RAM'

# End ALERTS

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
TIMESTAMP_FORMAT_SHORT = "%Y-%m-%d %H:%M:%S"

ENCODED_DATA = 'ENCODED_DATA'

INITIATOR_ID = 'INITIATOR_ID'

EE_HB_TIME = 'EE_HB_TIME'
EE_ADDR = 'EE_ADDR'
EE_WHITELIST = 'EE_WHITELIST'
EE_IS_SUPER = 'EE_IS_SUPER'
EE_FORMATTER = 'EE_FORMATTER'

SECURED = 'SECURED'

DEVICE_STATUS = 'DEVICE_STATUS'
MACHINE_IP = 'MACHINE_IP'
MACHINE_MEMORY = 'MACHINE_MEMORY'
AVAILABLE_MEMORY = 'AVAILABLE_MEMORY'
PROCESS_MEMORY = 'PROCESS_MEMORY'
CPU_USED = 'CPU_USED'
GPUS = 'GPUS'
GPU_INFO = 'GPU_INFO'
DEFAULT_CUDA = 'DEFAULT_CUDA'
CPU = 'CPU'
TIMESTAMP = 'TIMESTAMP'
CURRENT_TIME = 'CURRENT_TIME'
RECEIVED_TIME = 'RECEIVED_TIME'
UPTIME = 'UPTIME'
VERSION = 'VERSION'
TOTAL_DISK = 'TOTAL_DISK'
AVAILABLE_DISK = 'AVAILABLE_DISK'
ACTIVE_PLUGINS = 'ACTIVE_PLUGINS'
NR_INFERENCES = 'NR_INFERENCES'
NR_PAYLOADS = 'NR_PAYLOADS'
NR_STREAMS_DATA = 'NR_STREAMS_DATA'
GIT_BRANCH = 'GIT_BRANCH'
CONDA_ENV = 'CONDA_ENV'
SERVING_PIDS = 'SERVING_PIDS'
DCT_STATS = 'DCT_STATS'
COMM_STATS = 'COMM_STATS'

STOP_LOG = 'STOP_LOG'

TIMERS = 'TIMERS'
CONFIG_STREAMS = 'CONFIG_STREAMS'
PIPELINES = CONFIG_STREAMS
LOOPS_TIMINGS = 'LOOPS_TIMINGS'
DEVICE_LOG = 'DEVICE_LOG'
ERROR_LOG = 'ERROR_LOG'

LOGGER_VERSION = 'LOGGER_VERSION'
PY_VER = 'PY_VER'

TEMPERATURE_INFO = 'TEMPERATURE_INFO'


class COMM_INFO:
  IN_KB = 'IN_KB'
  OUT_KB = 'OUT_KB'


class ACTIVE_PLUGINS_INFO:
  STREAM_ID = "STREAM_ID"
  SIGNATURE = "SIGNATURE"
  INSTANCE_ID = "INSTANCE_ID"
  FREQUENCY = "FREQUENCY"
  INIT_TIMESTAMP = "INIT_TIMESTAMP"
  EXEC_TIMESTAMP = "EXEC_TIMESTAMP"
  PROCESS_DELAY = "PROCESS_DELAY"
  LAST_CONFIG_TIMESTAMP = "LAST_CONFIG_TIMESTAMP"
  FIRST_ERROR_TIME = "FIRST_ERROR_TIME"
  LAST_ERROR_TIME = "LAST_ERROR_TIME"
  OUTSIDE_WORKING_HOURS = "OUTSIDE_WORKING_HOURS"
  CURRENT_PROCESS_ITERATION = "CURRENT_PROCESS_ITERATION"
  CURRENT_EXEC_ITERATION = "CURRENT_EXEC_ITERATION"
  LAST_PAYLOAD_TIME = "LAST_PAYLOAD_TIME"
  TOTAL_PAYLOAD_COUNT = "TOTAL_PAYLOAD_COUNT"
  INFO = "INFO"

  ACTIVE_PLUGINS_FIELDS = [
     STREAM_ID,
     SIGNATURE,
     INSTANCE_ID,

     FREQUENCY,
     INIT_TIMESTAMP,
     EXEC_TIMESTAMP,
     LAST_CONFIG_TIMESTAMP,
     FIRST_ERROR_TIME,
     LAST_ERROR_TIME,
     OUTSIDE_WORKING_HOURS,
     CURRENT_PROCESS_ITERATION,
     CURRENT_EXEC_ITERATION,
     LAST_PAYLOAD_TIME,
     TOTAL_PAYLOAD_COUNT,
     INFO,
  ]
