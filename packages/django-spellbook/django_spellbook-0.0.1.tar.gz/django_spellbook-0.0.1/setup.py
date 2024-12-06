from setuptools import setup, find_packages

setup(
    name='django-spellbook',
    version='0.0.1',
    author='Mathew Storm',
    author_email='mathewstormdev@gmail.com',
    description='A collection of tools for creating beautiful, interactive content with Django. Markdown Processor includes special Django-like tags, and a block system allowing for re-usable components controlled directly through markdown.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/django-spellbook',
    # Excludes tests and example folders
    packages=find_packages(exclude=['tests*', 'examples*']),
    include_package_data=True,
    install_requires=[
        'django>=5.0',
        'markdown>=3.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',  # For bloggers
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',  # For blog content
    ],
    python_requires='>=3.10',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/django-spellbook/issues',
        'Source': 'https://github.com/yourusername/django-spellbook',
    },
)
