from setuptools import setup, find_packages

setup(
    name="DoomiPyApi",
    version="1.0.0",
    keywords=("Doomisoft", "Python AI"),
    description="The HTML Report for Python unit testing Base on HTMLTestRunner",
    long_description="The HTML Report for Python unit testing Base on HTMLTestRunner",
    license="MIT",
    url="https://github.com/five3/Doomisoft",
    author="StephenShen",
    author_email="28728660@qq.com",

    package_dir={'doomiapi': 'doomiapi'},         # 指定哪些包的文件被映射到哪个源码包
    packages=['doomiapi'],       # 需要打包的目录。如果多个的话，可以使用find_packages()自动发现
    include_package_data=True,
    py_modules=[],          # 需要打包的python文件列表
    # data_files=['pytestreport/templates/default.html', 'pytestreport/static/css/default.css', 'pytestreport/static/js/default.js'],          # 打包时需要打包的数据文件
    platforms="any",
    install_requires=[      # 需要安装的依赖包
        # 'Flask>=1.0.2'
    ],
    scripts=[],             # 安装时复制到PATH路径的脚本文件
    entry_points={
        'console_scripts': [    # 配置生成命令行工具及入口
            # 'PyTestReport.shell = pytestreport:shell',
            # 'PyTestReport.web = pytestreport:web'
        ]
    },
    classifiers=[           # 程序的所属分类列表
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)