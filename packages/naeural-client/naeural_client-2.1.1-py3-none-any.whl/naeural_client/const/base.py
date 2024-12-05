EE_ID = 'EE_ID'
SB_ID = 'SB_ID'  # change to SB_ID = EE_ID post mod from sb to ee


class CONFIG_STREAM:
  K_URL = 'URL'
  K_TYPE = 'TYPE'
  K_RECONNECTABLE = 'RECONNECTABLE'
  K_NAME = 'NAME'
  K_LIVE_FEED = 'LIVE_FEED'
  K_PLUGINS = 'PLUGINS'
  K_INSTANCES = 'INSTANCES'

  K_MODIFIED_BY_ADDR = 'MODIFIED_BY_ADDR'
  K_MODIFIED_BY_ID = 'MODIFIED_BY_ID'

  K_INITIATOR_ID = 'INITIATOR_ID'
  K_INITIATOR_ADDR = 'INITIATOR_ADDR'
  K_SESSION_ID = 'SESSION_ID'
  K_ALLOWED_PLUGINS = 'ALLOWED_PLUGINS'

  K_PIPELINE_COMMAND = 'PIPELINE_COMMAND'
  K_USE_LOCAL_COMMS_ONLY = 'USE_LOCAL_COMMS_ONLY'

  METASTREAM = 'MetaStream'

  INITIATOR_ID = K_INITIATOR_ID
  SESSION_ID = K_SESSION_ID
  COLLECTED_STREAMS = 'COLLECTED_STREAMS'
  STREAM_CONFIG_METADATA = 'STREAM_CONFIG_METADATA'
  CAP_RESOLUTION = 'CAP_RESOLUTION'

  LAST_UPDATE_TIME = 'LAST_UPDATE_TIME'

  URL = K_URL
  TYPE = K_TYPE
  RECONNECTABLE = K_RECONNECTABLE
  NAME = K_NAME
  LIVE_FEED = K_LIVE_FEED
  PLUGINS = K_PLUGINS
  INSTANCES = K_INSTANCES
  PIPELINE_COMMAND = K_PIPELINE_COMMAND
  LAST_PIPELINE_COMMAND = 'LAST_' + PIPELINE_COMMAND

  DEFAULT_PLUGINS = 'DEFAULT_PLUGINS'
  OVERWRITE_DEFAULT_PLUGIN_CONFIG = 'OVERWRITE_DEFAULT_PLUGIN_CONFIG'

  DEFAULT_PLUGIN = 'DEFAULT_PLUGIN'
  DEFAULT_PLUGIN_SIGNATURE = 'REST_CUSTOM_EXEC_01'
  DEFAULT_PLUGIN_CONFIG = 'DEFAULT_PLUGIN_CONFIG'

  ALLOWED_PLUGINS = K_ALLOWED_PLUGINS

  MANDATORY = [K_NAME, K_TYPE]

  VOID_STREAM = 'VOID'

  NO_DATA_STREAMS = [VOID_STREAM]


class BIZ_PLUGIN_DATA:
  INSTANCE_ID = 'INSTANCE_ID'
  MAX_INPUTS_QUEUE_SIZE = 'MAX_INPUTS_QUEUE_SIZE'
  COORDS = 'COORDS'
  POINTS = 'POINTS'
  INSTANCES = 'INSTANCES'
  SIGNATURE = 'SIGNATURE'
  PROCESS_DELAY = 'PROCESS_DELAY'
  ALLOW_EMPTY_INPUTS = 'ALLOW_EMPTY_INPUTS'
  RUN_WITHOUT_IMAGE = 'RUN_WITHOUT_IMAGE'


class PLUGIN_INFO:
  STREAM_ID = 'STREAM_ID'
  INSTANCE_ID = BIZ_PLUGIN_DATA.INSTANCE_ID
  SIGNATURE = BIZ_PLUGIN_DATA.SIGNATURE
  FREQUENCY = 'FREQUENCY'
  EXEC_TIMESTAMP = 'EXEC_TIMESTAMP'
  INIT_TIMESTAMP = 'INIT_TIMESTAMP'
  LAST_CONFIG_TIMESTAMP = 'LAST_CONFIG_TIMESTAMP'
  FIRST_ERROR_TIME = 'FIRST_ERROR_TIME'
  LAST_ERROR_TIME = 'LAST_ERROR_TIME'
  PROC_ITER = 'PROC_ITER'
  EXEC_ITER = 'EXEC_ITER'
  OUTSIDE_WORKING_HOURS = 'OUTSIDE_WORKING_HOURS'
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
  ]


EE_DATE_TIME_FORMAT = "%Y.%m.%d_%H:%M:%S"
