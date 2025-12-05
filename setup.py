from setuptools import setup, find_packages

setup(
    name="roomba-pathfinder",
    version="1.0.0",
    description="A Pathfinding AI Simulator using A*, RRT, and RRT*",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Mustafa BICER",
    author_email="mustafabicer.iletisim@gmail.com",
    url="https://github.com/poqob/roomba-pathfinder",
    
    # src klasörünü bir paket olarak algıla
    packages=find_packages(),
    
    # Gerekli kütüphaneler
    install_requires=[
        "pygame>=2.0.0",
        "pathfinding>=1.0.0"
    ],
    
    # Python sürümü kısıtlaması
    python_requires=">=3.8",
    
    # İşletim sistemi bağımsız olduğunu belirt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    # Paket harici dosyaları (resimler vb.) dahil etme ayarı
    include_package_data=True,
)