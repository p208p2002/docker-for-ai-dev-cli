import setuptools


with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()
    
# with open('requirements.txt','r',encoding = 'utf-8') as f:
    # requirements = f.read().split("\n")

setuptools.setup(
    name="docker_for_ai_dev_cli", # 
    version='0.0.1',
    author="Philip Huang",
    author_email="p208p2002@gmail.com",
    description="docker-for-ai-dev-cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    # install_requires = requirements
)