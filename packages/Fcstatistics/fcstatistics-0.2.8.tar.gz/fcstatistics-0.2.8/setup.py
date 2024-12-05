from setuptools import setup, Extension
from Cython.Build import cythonize

# Cython으로 빌드할 확장 모듈 정의
extensions = [
    Extension("Fcstatistics.Fc", ["Fcstatistics/Fc_test.pyx"]),
]

# setup 함수 정의
setup(
    name="Fcstatistics",
    version="0.2.8",
    long_description=open("README.md", encoding="utf-8").read(),
    ext_modules=cythonize(extensions),    # Cython 컴파일 활성화
    package_data={
        "Fcstatistics": ["*.pxd", "*.c", "*.h", "*.pyd"],  # 포함할 파일 확장자 명시
    },
    include_package_data=True,
)
