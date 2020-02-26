from setuptools import setup, find_packages
import sys

TELLURIUM = "tellurium"
INSTALL_FULL = [
    "matplotlib",
    "networkx",
    "nose",
    "numpy",
    "pandas",
    "python-libsbml",
    "pyyaml",
    "scipy",
    "urllib3",
    "xlrd",
    "tellurium",
    ]

def sbmllint_setup(install_requires):
  setup(
      name='SBMLLint',
      version='1.0.6',
      author='Woosub Shin, Joseph L. Hellerstein',
      author_email='jlheller@uw.edu',
      packages=find_packages(exclude=['tests', 'analysis',
          'notebook', 'docs']),
      scripts=[
          'SBMLLint/tools/games',
          'SBMLLint/tools/games.bat',
          'SBMLLint/tools/moiety_analysis',
          'SBMLLint/tools/lp_analysis',
          'SBMLLint/tools/make_moiety_structure',
          'SBMLLint/tools/print_reactions',
          ],
      url='https://github.com/ModelEngineering/SBMLLint',
      description='Linter for SBML models.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      package_dir={'SBMLLint': 'SBMLLint'},
      install_requires=install_requires,
      include_package_data=True,
      data_files=[('data/biomodels',
          ['data/biomodels/biomodels.zip'])],
      #extras_require={ "Antimony":  [TELLURIUM]},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',      # Define that your audience are developers
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',   # Again, pick a license
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
        ],
      )

sbmllint_setup(INSTALL_FULL)
