from setuptools import setup, find_packages

def readme():
        with open('README.rst') as f:
                    return f.read()

setup(
        name='thebe',
        version='0.0.3.4',
        description='Automatically runs and displays python code in browser.',
        author_email='hairyhenry@gmail.com',
        url='https://github.com/hotsoupisgood/Satyrn',
        include_package_data=True,
        packages = ['thebe', 'thebe/templates', 'thebe/static', 'thebe/core', 'thebe/logs'],
        package_data={
            'thebe':['thebe.py'], 'templates': ['*'], 'static': ['*'], 'core': ['*'], 'logs': ['*']
                },
#        packages=find_packages(),
        install_requires=[
            'flask',
            'flask_socketio',
            'pygments',
            'dill'
            ],
        entry_points={
            'console_scripts': [
                'thebe = thebe.thebe:main',
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
        )
