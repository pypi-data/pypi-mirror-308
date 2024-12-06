from setuptools import setup, find_packages
setup(
    name = "qinglan",
    version = "0.0.3",
    packages = find_packages(),
    author = "thekingofhero",
    author_email = "thekingofhero@live.com",
    description = "This is a scaffold for nicegui,just like ruby on rails",
    license = "MIT",
    entry_points = {
        'console_scripts': ['qinglan=qinglan.cmd:main'],
    }
    #url = "http://example.com/HelloWorld/"  
)
