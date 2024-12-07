from setuptools import setup, find_packages

setup(
    name="song_organizer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package to organize music files by metadata.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/your-repo/song_organizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["mutagen"],
    entry_points={
        'console_scripts': [
            'song-organizer=song_organizer.__main__:main',
        ],
    },
)
