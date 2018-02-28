"""
Data analysis configuration
Mainly key facts, files and directory paths common to all aspects of the analysis
"""
DATA_ROOT_DIR = 'data/'
RAW_DIR = DATA_ROOT_DIR + 'raw/'
DERIVATIVE_DIR = DATA_ROOT_DIR + 'derivative/'
PROCESSED_DIR = DATA_ROOT_DIR + 'processed/'

MODELS_DIR = 'models/'

HEALTHY_DATA = DERIVATIVE_DIR + 'healthy/sub-healthy_all.csv'
CONTROL_DATA = DERIVATIVE_DIR + 'control/sub-control_all.csv'
PATIENT_DATA = DERIVATIVE_DIR + 'patient/sub-patient_all.csv'

HEALTHY_MODELS_PATH = MODELS_DIR + 'db_healthy'
CONTROL_MODELS_PATH = MODELS_DIR + 'db_controls'
PATIENT_MODELS_PATH = MODELS_DIR + 'db_patients'

HEALTHY_OUT_DIR = PROCESSED_DIR + 'healthy/'
CONTROL_OUT_DIR = PROCESSED_DIR + 'control/'
PATIENT_OUT_DIR = PROCESSED_DIR + 'patient/'

CONDITIONS = ['SS', 'CP', 'CS', 'US']