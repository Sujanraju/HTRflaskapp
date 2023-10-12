from setuptools import setup, find_namespace_packages

setup(
    name='htr-pipeline',
    version='1.0.0',
    description='Handwritten text recognition pipeline.',
    author='SUJAN',
    packages=find_namespace_packages(),
    install_requires=['numpy==1.21.0',
                      'tensorflow==2.11.0',
                      'opencv-python',
                      'scikit-learn',
                      'editdistance',
                      'path'],
    python_requires='>=3.8',
    package_data={'htr_pipeline.reader.stored_model': ['*']}
)
