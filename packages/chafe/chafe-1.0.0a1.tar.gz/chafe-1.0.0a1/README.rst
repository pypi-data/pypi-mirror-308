Encrypt and Decrypt files
=========================

This Python package provides tools for encrypting and decrypting files
with Dan Bernstein's ChaCha stream cipher, using a key derived from a
pass phrase.

Usage  
----- 
The package provides two entry points named encrypt and decrypt. That
means that if this module is in your Python path then the module can
be used as follows:

To encrypt a file named myfile:

 ``% python3 -m chacha.encrypt myfile``

You will be prompted for a password, and an encrypted file named
myfile.cha will be created.  The password will be visible until the
encryption is finished, then erased.  (So write it down first!)

To decrypt myfile.cha:

  ``% python3 -m chacha.decrypt myfile.cha``

You will be prompted for the password, and a decrypted file named myfile.
will be created.  The password will be visible until the decryption is
finished, then erased.

If you install this module with pip then the commands will simply be:

  ``% chacha-encrypt myfile``

and

  ``% chacha-decrypt myfile.cha``
