from setuptools import setup, find_packages

setup(
    name='mypackage_test_t',                     # 包名
    version='0.1.0',                      # 包的版本号
    packages=find_packages(),             # 自动发现包
    install_requires=[                    # 依赖的第三方库
        'pytest',                          # 如果有需要的依赖，列出它们
    ],
    author='szy123',                   # 作者
    author_email='15735709004@163.com',   # 作者邮箱
    description='test_upload_package', # 包的简短描述
    long_description=open('README.md').read(),  # 详细描述
    long_description_content_type='text/markdown',
    url='https://github.com/szy123/mypackage_test_t',  # 项目的URL
    classifiers=[                          # Python 包的分类信息
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)
