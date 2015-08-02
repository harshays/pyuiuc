from setuptools import setup

requirements = ['requests', 'responses']
test_requirements = ['nose']

setup(
    name='PyUIUC',
    version='0.1',
    description="UIUC CISAPI Python API Wrapper",
    author="Harshay Shah",
    author_email='harshay.rshah@gmail.com',
    url='https://github.com/harshays/PyUIUC',
    packages=['pyuiuc',],
    package_dir={'pyuiuc': 'pyuiuc'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    test_suite='tests',
    tests_require=test_requirements
)
