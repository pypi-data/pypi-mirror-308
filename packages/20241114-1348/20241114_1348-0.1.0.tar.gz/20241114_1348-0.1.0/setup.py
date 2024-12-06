from setuptools import setup, find_packages

setup(
    name='20241114_1348',  # 包名
    version='0.1.0',    # 版本号
    packages=find_packages(),
    description='A simple utility package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/FriedrichMuelle/20241114_1348',  # 项目主页
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)