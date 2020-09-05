import setuptools

setuptools.setup(
    name="docker_for_ai_dev_cli", # 
    version='0.0.1',
    author="Philip Huang",
    author_email="p208p2002@gmail.com",
    description="docker-for-ai-dev-cli",
    url="https://github.com/p208p2002/docker-for-ai-dev-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['dfad=docker_for_ai_dev_cli:main'],
    },
    python_requires='>=3.5',
    install_requires = ['requests']
)