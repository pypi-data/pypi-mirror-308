============
SNAP BCA API
============
:Author: Oji Setyawan <ojiset22@outlook.com>
:Company: PT Tenten Digital Indonesia
:Version: $Version: 1.0.0 $
:License: GNU GPL v3

.. role:: python(code)
   :language: python

.. contents:: Table of content

Introduction
============

python module to access SNAP BCA API. 

Feature :

- check balance.
- account statement (history).

How to install
==============

1. Clone or download this repo https://github.com/tentendigital-id/Snap-BCA-API.git.
2. Move this entire project to your project's directory.

How to use
==========

1. Import library to your project :python:`from snap_bca_api.bca import BCA_SNAP`.
2. Initiate config your BCA API

.. code-block:: python

    bca = BCA_SNAP(
        client_id=client_id,
        client_secret=client_secret,
        private_key=private_key,
        channel_id=channel_id,
        partner_id=partner_id,
        host=host,
        debug=False
    )

3. Call :python:`BCA_SNAP` function.

Get balance
-----------

.. code-block:: python

    get_balance = bca.getBalance(
        account_number=ACCOUNT_NUMBER,
        partnerReferenceNo=PARTNER_REFERENCE_NO,
    )
    print(get_balance)

Get statement
-------------

.. code-block:: python

    get_statement = bca.getStatement(
        account_number=ACCOUNT_NUMBER,
        partnerReferenceNo=PARTNER_REFERENCE_NO,
        fromDateTime=FROM_DATE,
        toDateTime=TO_DATE
    )
    print(get_statement)

Note:

1. :code:`FROM_DATE` and :code:`TO_DATE` use :code:`yyyy-MM-ddT00:00:00+07:00` format.
2. Maximum date to get from start to end is 31 day.


Resource
=================

- https://stackoverflow.com/questions/32505722/signing-data-using-openssl-with-python
- https://github.com/otnansirk/php-snap-bi
- https://github.com/zahris85/Python-API-BCA/tree/master
- https://github.com/TheArKaID/snap-bi-signer-js
- https://github.com/3mp3ri0r/cpybca
