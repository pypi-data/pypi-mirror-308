from setuptools import setup, find_packages

setup(
    name='sageattention', 
    version='1.0.4',  
    author='Jintao Zhang, Haofeng Huang',  
    author_email='jt-zhang6@gmail.com', 
    packages=find_packages(),  
    description='Accurate and efficient 8-bit plug-and-play attention.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    url='https://github.com/jt-zhang/SageAttention', 
    license='BSD 3-Clause License', 
    python_requires='>=3.9', 
    classifiers=[  
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',  
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
