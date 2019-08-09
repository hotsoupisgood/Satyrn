from setuptools import setup, find_packages

def readme():
        with open('README.rst') as f:
                    return f.read()

setup(
        name='python_live',
        version='0.1',
        description='Automatically runs and displays python code in browser.',
        long_description=readme(),
#        include_package_data=True,
        package_data={
                'python_live': [ '../README.rst', 'templates/*','static/*','util.py']
                },
        packages=find_packages(),
#        ['python_live', 'python_live/util', 'python_live/static', 'python_live/templates'],
#        install_requires=[
#            'flask',
#            'flask_socketio',
#            'pygments'
#            ],
        zip_safe=False,
        entry_points={
            'console_scripts': [
                'livepy = python_live.livepy:main',
                ]
            }
#        scripts=['bin/livepy'],
        )
