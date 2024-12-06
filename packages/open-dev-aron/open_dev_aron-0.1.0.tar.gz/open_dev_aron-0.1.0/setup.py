from setuptools import setup

setup(
    name='open_dev_aron',
    version='0.1.0',
    author='Seu Nome',
    author_email='felipe.aron@icloud.com',
    description='Uma breve descrição do seu pacote.',
    python_requires='>=3.6, <4',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    scripts=['scripts/hello.py']  # Certifique-se de que o caminho está correto
)
