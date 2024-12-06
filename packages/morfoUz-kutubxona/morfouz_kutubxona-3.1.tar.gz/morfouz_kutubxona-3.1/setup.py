import setuptools

setuptools.setup(
   name='morfoUz_kutubxona',
   version='3.1',
   author='Alisher Ismailov Shakirovich',
   author_email='alisherismailov1991@gmail.com',
   description='''ushbu kutubxona o`zbek tili uchun qo`llaniladi. 
   Kutubxonadan foydalangan holda tadqiqotchi o`zbek morfologik tahlilni amalga oshirish mumkin. 
   Kutubxona foydalanuvchidan gap/matn kiritishni so`raydi va 
   kiritilgan matnni morfologik tahlil qilingan holatda natijasini ko`rsatadi''',
   packages=setuptools.find_packages(),
   license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)