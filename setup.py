from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='covidcapitalist',
    version='0.1.0',
    description='Tycoon game based on the COVID-19 pandemic',
    long_description=readme(),
    url='',
    author='Svein-Kåre Bjørnsen',
    author_email='sveinkare@gmail.com',
    test_suite="nose.collector",
    tests_require=["nose"],
    license='MIT',
    entry_points = {
        "console_scripts" : [
            "covidcapitalist=covidcapitalist.cmd:main",
        ],
    },
    packages=find_packages(include=['covidcapitalist', 'covidcapitalist.*']),
    include_package_data=True,
    install_requires=[
        "pygame>=1.9.6",
    ],
    zip_safe=False
)