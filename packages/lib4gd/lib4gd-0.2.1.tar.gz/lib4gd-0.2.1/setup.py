from setuptools import setup, find_packages

setup(
    name='lib4gd',
    version='0.2.1',
    description='A comprehensive library for image handling and Google Drive file downloading.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tejas R Simha',
    author_email='tejas@4gd.ai',
    url='https://github.com/4dg-ai/lib4gd',
    license='MIT',
    packages=find_packages(include=["lib4gd", "lib4gd.*"]),  # Ensure all subpackages are included
    install_requires=[
        'aiofiles>=0.8.0',
        'google-auth>=2.0.0',
        'google-auth-oauthlib>=0.4.0',
        'google-auth-httplib2>=0.1.0',
        'google-api-python-client>=2.0.0',
        'numpy>=1.19.0',
        'opencv-python>=4.5.0',
        'Pillow>=8.0.0',
        'asyncssh>=2.0.0',  # For SFTP downloading
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
