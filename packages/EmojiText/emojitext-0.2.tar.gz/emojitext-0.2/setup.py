from setuptools import setup, find_packages

setup(
    name="EmojiText",
    version="0.2",
    author="LacyCat1807",
    description="A library to parse and display custom emojis in text",
    #long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LacyCat/EmojiText",  # GitHub 저장소 URL
    packages=find_packages(),
    include_package_data=True,  # 이미지 파일 포함
    package_data={
        "EmojiText": ["../emojis/*.png","../emojis/*.gif"]  # 이모지 폴더 파일 포함
    },
    install_requires=[
        "Pillow"  # 의존 패키지 (예: 이미지 처리를 위해)
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
