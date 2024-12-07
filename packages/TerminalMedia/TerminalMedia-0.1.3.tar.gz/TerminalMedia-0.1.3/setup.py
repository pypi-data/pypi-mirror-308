from setuptools import setup, find_packages

setup(
    name='TerminalMedia',
    version='0.1.3',
    description='A tool to display images and videos in the terminal',
    author='Snape-max',
    author_email='ssnape@qq.com',
    url='https://github.com/Snape-max/TerminalMedia',  # 你的项目主页
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'terminalmedia=tmt.terminalmedia:main',
            'icat=tmt.imgcat:main',
            'vcat=tmt.videocat:main',
        ],
    },
    install_requires=[
        'Pillow',
        'opencv-python'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 选择合适的许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)