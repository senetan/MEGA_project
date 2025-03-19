from setuptools import find_packages, setup

with open('requirements.txt') as f:
    content = f.readlines()

requirements = [x.strip() for x in content if "git+" not in x]
extra_files = [
    'Dockerfile',
    'Makefile',
    'README.md',
    'requirements.txt',
    'models/MEGA_model.h5',
    'models/MEGA_model.pkl',
    'notebook/mvp_draft.ipynb',
    'raw_data/df_de_merged.csv'
]
setup(
    name='MEGA_project_folder',
    version="0.0.1",
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mega_api=MEGA_project_folder.api_file:main',
        ],
    },
)
