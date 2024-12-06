from setuptools import setup, find_packages

setup(
   name='MeuPrimeiroPypi',
   version='1.0',
   packages=find_packages(),
   install_requires=[],
   author='LRZCalmon / Curso FIAP-PosIA',
   author_email='ricardocalmon@gmail.com',
   description='Um Hello World para aprender a subir no twine.',
   url='',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)

