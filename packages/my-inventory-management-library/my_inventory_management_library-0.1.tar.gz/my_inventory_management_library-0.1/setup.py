from setuptools import setup, find_packages

setup(
    name="my_inventory_management_library",
    version="0.1",
    packages=find_packages(),
    description="Library to manage different inventories",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ane Vázquez, Ainhize Barredo, Naroa Etxebarria and Lucia Saiz",
    author_email="ane.vazquez@ikasleak.salesianosdeusto.com",
    url="https://github.com/naroaetxebarria/inventory-management.git",
    keywords = ['Inventory', 'Product', 'Shop'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
    python_requires='>=3.6',
)
