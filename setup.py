import setuptools

setuptools.setup(
    name='line_pay',
    version='0.1.0',
    author='Pochang Lee',
    author_email='stupidgod08@yahoo.com.tw',
    description='Line pay sdk for python',
    long_description='Line pay sdk for python ',
    long_description_content_type='text/markdown',
    url='https://github.com/pochangl/line-pay',
    install_requires=[
        'requests',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
    ],
)
