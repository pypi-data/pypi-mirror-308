from setuptools import setup, find_packages

setup(
    name='Blackamerxs',  # اسم المكتبة هنا
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',  # المكتبات التي يعتمد عليها الكود
    ],
    description='A library to send files via Telegram bot',  # وصف المكتبة
    author='Mohammed',  # اسمك
    author_email='wfwefsdfwe@example.com',  # بريدك الإلكتروني
    url='https://github.com/eergwg/Blackamerxs',  # الرابط إلى مستودع GitHub (إذا كان موجودًا)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # يمكنك تعديل الترخيص إذا أردت
        'Operating System :: OS Independent',
    ],
)
