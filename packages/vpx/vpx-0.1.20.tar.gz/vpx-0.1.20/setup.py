from setuptools import setup, find_packages

setup(
    name="vpx",
    version="0.1.0",
    packages=find_packages(include=['vpx', 'vpx.*']),
    install_requires=[
        "typer>=0.9.0",
        "openai",
        "anthropic",
        "python-dotenv",
        "svgwrite",
        "Pillow>=9.0.0",
        "cairosvg",
    ],
    entry_points={
        "console_scripts": [
            "vpx=vpx.cli:app",
        ],
    },
    python_requires=">=3.7",
)
