from setuptools import setup, find_packages

setup(
    name='tlgfwk',
    version='1.0.5',
    description='A Telegram Bot Framework for monitoring remote hosts',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/tlgfwk',  # Replace with your repository URL
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'python-telegram-bot>=20.0a4',
        'python-dotenv>=0.21.0',
        'httpx>=0.23.0',
        'cryptography>=3.4.7',
        'flask',
        'paypalrestsdk'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)