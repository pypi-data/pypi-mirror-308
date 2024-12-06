from setuptools import setup, find_packages

setup(
    name="FaceGuard",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "face_recognition",
        "numpy"
    ],
    description="A face recognition package for login systems and other",
    author="Paul H.",
    author_email="paulhoflich@gmail.com",
    url="https://github.com/baulum/FaceGuard",
)
