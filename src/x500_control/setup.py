from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'x500_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),
        (
            os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.sdf')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='siva',
    maintainer_email='sivasai1232006@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "x500_cmd = x500_control.x500_twist_pub:main",
            "keyboard = x500_control.keyboard_node:main",
        ],
    },
)
