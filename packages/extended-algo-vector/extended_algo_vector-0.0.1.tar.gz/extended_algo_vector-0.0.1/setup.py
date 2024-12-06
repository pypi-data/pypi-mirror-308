import time

from setuptools import setup
import shutil

try:
    print('Removing cache data before install...')
    shutil.rmtree('./build/')
    shutil.rmtree('./dist/')
    shutil.rmtree('./extended_algo.egg-info/')
    shutil.rmtree('./.pytest_cache/')
    time.sleep(1)
except:
    ...

setup(name='extended-algo-vector',
      version='0.0.1',
      description='wrapper for vector algo that supports the extended-chart and strategy discovery',
      url='https://github.com/karunkrishna/extended_algo_vector',
      author='Karun Krishna',
      author_email='karun.krishna@gmail.com',
      license='MIT',
      packages=['extended_algo_vector', 'extended_algo_vector.engine', 'extended_algo_vector.market', 'extended_algo_vector.report',
                'extended_algo_vector.report.calculate', 'extended_algo_vector.report.utils',
                'extended_algo_vector.market.bars', 'extended_algo_vector.market.utils'],

      # TODO: I may want to hard code the version numbers being used here:
      install_requires=['pandas', 'python-dotenv', 'pandas-ta', 'extended-chart', 'tqdm', 'pyarrow', 'SQLAlchemy',
                        'mysqlclient'],
      zip_safe=False
      )
