from distutils.core import setup
from datetime import date


setup(name='NPS Travel Time Cost Surface Model TTCSM',
      version = str(date.today()).replace('-',''),
      description= '''Defines a travel time surface for both motorized
      and foot travel through various landscapes characterized by roads, trails,
      elevation,  water bodies, and vegetational cover.''',
      author='Brent Frakes; National Park Service',
      author_email='brent_frakes@nps.gov',
      url='http://irmaservices.nps.gov/',
      packages=['TTCSM'],
      data_files=[('',['Documentation/TTCSM.pdf']),
                  ('',['TestingData.zip']),
                  ('',['TTCSM_Toolbox.tbx']),
                  ('',['TTCSM_TBOX.py'])
                  ]
    )

