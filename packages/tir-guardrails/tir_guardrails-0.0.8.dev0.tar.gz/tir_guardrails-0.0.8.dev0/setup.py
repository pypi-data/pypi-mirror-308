from setuptools import find_packages, setup

setup(
    name="tir_guardrails",
    version="0.0.8.dev",
    description="TIR Guardrails is a safety framework for monitoring and mitigating harmful or inappropriate outputs in AI systems",
    author='Atharva Pakade',
    author_email='pakade310@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "better_profanity",
        "presidio_analyzer[transformers]",
        "presidio_anonymizer",
        "alt-profanity-check",
        "openai",
        "fuzzysearch",
        "python-dotenv"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='Apache License 2.0'
)
