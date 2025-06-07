from distutils.core import setup

setup(
    name="web-dos",
    py_modules=["web_dos"],
    entry_points={"console_scripts": ["web-dos=web_dos:main"]},
    version="1.0.0",
    description="Slow HTTP DoS (Denial of Service) testing tool written in Python.",
    author="It Is Unique Official",
    author_email="itisuniqueofficial@gmail.com",
    url="https://github.com/itisuniqueofficial/web-dos",
    keywords=["dos", "http", "slowloris", "web-dos", "stress-test"],
    license="MIT",
)
