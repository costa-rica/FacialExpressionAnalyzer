import os
from fea_config import ConfigWorkstation, ConfigDev, ConfigProd

match os.environ.get('fea_config_TYPE'):
    case 'dev':
        config = ConfigDev()
        print('- FacialExpressionAnalyzer/app_pacakge/config: Development')
    case 'prod':
        config = ConfigProd()
        print('- FacialExpressionAnalyzer/app_pacakge/config: Production')
    case _:
        config = ConfigWorkstation()
        print('- FacialExpressionAnalyzer/app_pacakge/config: Local')