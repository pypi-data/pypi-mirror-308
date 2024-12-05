==================================
 RsCmwBluetoothSig
==================================

.. image:: https://img.shields.io/pypi/v/RsCmwBluetoothSig.svg
   :target: https://pypi.org/project/ RsCmwBluetoothSig/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsCmwBluetoothSig.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsCmwBluetoothSig.svg
   :target: https://pypi.python.org/pypi/RsCmwBluetoothSig/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsCmwBluetoothSig.svg
   :target: https://pypi.python.org/pypi/RsCmwBluetoothSig/

Rohde & Schwarz CMW Bluetooth Signaling RsCmwBluetoothSig instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsCmwBluetoothSig import *

    instr = RsCmwBluetoothSig('TCPIP::192.168.2.101::hislip0')
    idn = instr.query('*IDN?')
    print('Hello, I am: ' + idn)

Supported instruments: CMW500, CMW270

The package is hosted here: https://pypi.org/project/RsCmwBluetoothSig/

Documentation: https://RsCmwBluetoothSig.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/


Version history
----------------

Release Notes:

Latest release notes summary: Update for FW version 4.0.230

	Version 4.0.230
		- Update for FW version 4.0.230

	Version 3.8.xx2
		- Fixed several misspelled arguments and command headers

	Version 1.0.0.0
		- First released version