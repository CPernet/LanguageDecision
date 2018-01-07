PROJECT_DIR = '/lang_dec/'
MODELS_DIR = PROJECT_DIR + 'language_decision/models/'
DATA_DIR = PROJECT_DIR + 'data/'
DB_TYPE = 'txt'

PILOT_DATA = DATA_DIR + 'pilot_clean.csv'
CONTROLS_DATA = DATA_DIR + 'controls_clean.csv'
PATIENT_DATA = DATA_DIR + 'patients_clean.csv'

_pilot_models = {
    'lumped': 'pilot_lumped',
    'norm': 'pilot',
}
_controls_models = {
    'lumped': 'controls_lumped',
    'norm': 'controls',
}
_patients_models = {
    'lumped': 'patients_lumped',
    'norm': 'patients',
}

PILOT_MODELS = {k: MODELS_DIR + v for k, v in _pilot_models.items()}
CONTROLS_MODELS = {k: MODELS_DIR + v for k, v in _controls_models.items()}
PATIENTS_MODELS = {k: MODELS_DIR + v for k, v in _patients_models.items()}
