from setuptools import setup, find_packages

setup(
    name='arm_rag_testing',
    version='7.7.9',
    packages=find_packages(include=["*"]),
    include_package_data=True,
    package_data={
    '': ['config/default_config.yaml'],
},

    install_requires=[
        'PyYAML==6.0.2',
        'python-docx==1.1.2',
        'Spire.Doc==12.7.1',
        'weaviate-client==4.9.0',
        'sentence-transformers==3.2.1',
        'python-dotenv==1.0.1',
        'tabulate==0.9.0',
        'python-multipart',
        'anthropic==0.37.1',
        'openai==1.52.2',
        'deeplake==3.9.26',
        'pypdf==5.1.0',
        'gmft==0.4.0'
    ],
    python_requires='>=3.6',
)