from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
readme_path = Path(__file__).parent / 'README.md'
long_description = readme_path.read_text(encoding='utf-8')


def main():
    setup(
        name='printmoji',
        version='1.0.0',
        packages=find_packages(),
        include_package_data=True,
        author='Kyle Williams',
        description='Printing with emojis',
        python_requires='>=3',
        classifiers=[
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 3'
        ],
        long_description=long_description,
        long_description_content_type="text/markdown"
    )


if __name__ == '__main__':
    main()
