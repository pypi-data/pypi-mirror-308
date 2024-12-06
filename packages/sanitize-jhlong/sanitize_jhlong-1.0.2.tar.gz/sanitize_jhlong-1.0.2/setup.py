from setuptools import setup

setup(
    name='sanitize_jhlong',
    version='1.0.2',
    description='处理计时数据的一个函数',
    long_description=open("README.md", encoding="utf-8").read(), # 从 README.md 文件读取长描述
    long_description_content_type="text/markdown",  # 指定描述文件的格式
    py_modules=['sanitize_jhlong'],
    author='jhlong',
    author_email='jhlong2024@163.com',
)

