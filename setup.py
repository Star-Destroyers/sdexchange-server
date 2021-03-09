from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='sdexchange-server',
    version='0.0.1',
    description='Start Destroyers Exchange API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Star-Destroyers/sdexchange-server',
    author='Austin Riba',
    author_email='austin@m51.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GPLV3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='Star destroyers,astronomy,alerts,',
    packages=find_packages(),
    python_requires='>=3.8, <4',
    install_requires=[
        'fastapi',
        'uvicorn[standard]'
    ],
    extras_require={
        'dev': [
            'requests',
            'pytest'
        ]
    },
    project_urls={
        'Bug Reports': 'https://github.com/Star-Destroyers/sdexchange-server/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/Star-Destroyers/sdexchange-server/'
    },
)
