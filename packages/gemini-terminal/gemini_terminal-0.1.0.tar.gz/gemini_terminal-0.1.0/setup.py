from setuptools import setup, find_packages

setup(
    name="gemini-terminal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
    ],
    entry_points={
        'console_scripts': [
            'gemini-chat=gemini_terminal.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A terminal-based chat interface for Google's Gemini AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
) 