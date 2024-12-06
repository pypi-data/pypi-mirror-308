from setuptools import setup, find_packages

setup(
    name="lovadira",  # Nama library
    version="0.1",  # Versi library
    packages=find_packages(),  # Menemukan semua paket yang ada dalam proyek
    install_requires=[],  # Daftar dependensi yang diperlukan, jika ada
    description="A library for generating random quotes from Gus Baha",  # Deskripsi singkat
    long_description=open('README.md').read(),  # Deskripsi panjang dari file README.md
    long_description_content_type='text/markdown',  # Format deskripsi panjang
    author="Khoirul Anam",  # Nama Anda
    author_email="khoirulanaam4567@gmail.com",  # Email Anda
    url="https://github.com/Anammkh/Lovadira",  # URL ke repositori GitHub
    classifiers=[  # Klasifikasi untuk mendeskripsikan tipe proyek Anda
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versi Python yang diperlukan
)

