# setup.py

from setuptools import setup, find_packages

setup(
    name="llm_structured_output_Detect_repairs",
    version="0.1.0",
    author="jiayanfeng",
    author_email="jyf_bit@163.com",
    description="A Python package for interacting with large language models (LLMs) to extract, detect, and fix structured data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/lfl_llm_agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'langchain',
        'openai',
    ],
)