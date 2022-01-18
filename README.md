# Implementation of encryption algorithms
There are too many comments in Russian in the code, but this is to get a good grade.

The further - the more difficult the tasks and the better the code)
## Structure
- [Cesarean code](#cesar)
- [Substitution cipher](#substitution-cipher)
- [Frequency analysis](#frequency-analysis)


- [Miller–Rabin primality test](#miller-rabin)
- [RSA client-server socket app](#rsa)

<a name="cesar"></a>
### Cesarean code
![](./z-pictures/ceaserCipher.png)
PATH: /cesar
The console application can work in several modes:
- encryption with step d
- decryption
- brute force

<a name="substitution-cipher"></a>
### Substitution cipher
![](./z-pictures/substitution-cipher.png)
PATH: /substitution_cipher
The console application can work in several modes:
- random encryption table generation
- text encryption
- text decryption

<a name="frequency-analysis"></a>
### Frequency analysis
![](./z-pictures/freq.png)
PATH: /frequency_analysis
The console application can work in several modes:
- random encryption table generation
- text encryption
- scenario to evaluate the effectiveness of frequency analysis
- scenario to crack the substitution cipher manually

<a name="miller-rabin"></a>
### Miller–Rabin primality test
![](./z-pictures/miller.jpg)
PATH: /miller-rabin_primary_test
The console application can work in several modes:
- check numbers from file
- check nubers from console input
- check number with client-server console app on sockets
  - first start server(main.py) then client(client.py)

<a name="rsa"></a>
### RSA client-server socket app
![](./z-pictures/how-rsa-works.png)
PATH: /rsa
The console application can work in several modes:
- chipher functions on encryption.py
- rsa chat with client-server console app on sockets
  - first start server(main.py) then client(client.py) then client1.py