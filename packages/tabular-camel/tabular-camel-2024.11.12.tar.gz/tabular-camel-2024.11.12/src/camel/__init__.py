import warnings


# ================================================================
# =                                                              =
# =                    Warning Information                       =
# =                                                              =
# ================================================================
def color_formatwarning(message, category, filename, lineno, line=''):
    COLOR = '\033[33m'  # Yellow
    RESET = '\033[0m'
    BOLD = '\033[1m'

    return f"{COLOR}{BOLD}{category.__name__}: {filename}:{lineno}: {RESET}{COLOR}{message}{RESET}\n"


warnings.formatwarning = color_formatwarning

# ================================================================
# =                                                              =
# =                    Dataset Information                       =
# =                                                              =
# ================================================================
dataset2openml_id = {
    # Classification
    'qsar-biodeg'               : 1494,
    'vehicle'                   : 54,
    'texture'                   : 40499,
    'steel-plates-fault'        : 1504,
    'MiceProtein'               : 40966,
    'mfeat-fourier'             : 14,
    'adult'                     : 179,
    'one-hundred-plants-texture': 1493,
    'energy-efficiency'         : 1472,
    'collins'                   : 40971,
    'soybean'                   : 42,
    'wilt'                      : 40983,
    'autoUniv-au6-1000'         : 1555,
    'vowel'                     : 307,
    'stock'                     : 841,
    'iris'                      : 61,
    # Regression
    'liver-disorders'   : 8,
    'abalone'           : 42726,
    'california_housing': 43939,
    'house_16H'         : 574,
}

dataset2uci_id = {
    # Classification
    'predict_students_dropout_and_academic_success': 697,
    'aids_clinical_trials_group_study_175'         : 890,
    'support2'                                     : 880,
    'mushroom'                                     : 73,
    'auction_verification'                         : 713,
    'abalone'                                      : 1,
    'statlog_german_credit_data'                   : 144,
}

dataset2path = {
    # Classification
    'lung': '/home/xj265/phd/codebase/Camel/dataset/lung/lung.mat'
}
