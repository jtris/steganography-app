# Steganography Desktop App

- An easy to use app for image steganography.
- Supports both **png** and **jpg** file formats.

## supported steganography techniques

### 1) data appending
- This option simply hides data, in the image's **hex dump**, so there's no pixel/palette processing. 

<img src="https://github.com/jtris/steganography-app/blob/main/screenshots/hex_dump_hidden_message.png" alt="screenshot" width="500"/>

- This is done by appending the binary data to the image file.
	- This command essentially does the same thing:
<br>

``` cmd
$ echo "this is a secret message" >> image.jpg
```
### 2) metadata
-  Pastes given data into the "**image description**" metadata field. You can read this modified property if you look at the image's properties.

<img src="https://github.com/jtris/steganography-app/blob/main/screenshots/metadata.png" alt="screenshot" width="400"/>

### 3) LSB (least significant bit) matching
- Hides data by modifying the least significant bit of each byte, therefore storing either a 0 or a 1 there.
- If a bit needs to be changed to reflect the data you want to hide, this program randomly chooses between incrementing and decrementing the binary value of the given byte by 1 - this has multiple advantages over simply overwriting the last bit with a "1" or a "0" (commonly referred to as LSB replacement). Most importantly it doesn't create obvious statistical anomalies, therefore isn't as detectable.

### 4) AES combined with LSB matching
- This option firstly encrypts data with AES (a symmetric-key algorithm) and only then hides it with LSB. This serves as an extra layer of security in case LSB gets detected.

### 5) RSA combined with (AES and) LSB matching
- An asymmetric (public-key) cryptography alternative. Data is still first encrypted with AES, except the AES credentials are prepended to the ciphertext. These credentials are then encrypted with RSA and only then is LSB used. It is done this way because RSA can only encrypt data up to the size of its key (2048 bits in this case), so only encrypting data with RSA would be very limiting. Adding AES and only encrypting its credentials is a workaround around this limitation. 

<br>

## GUI examples
<img src="https://github.com/jtris/steganography-app/blob/main/screenshots/main_menu.png" alt="screenshot" width="400"/> <img src="https://github.com/jtris/steganography-app/blob/main/screenshots/s2.png" alt="screenshot" width="400"/>
<img src="https://github.com/jtris/steganography-app/blob/main/screenshots/s3.png" alt="screenshot" width="400"/> <img src="https://github.com/jtris/steganography-app/blob/main/screenshots/s4.png" alt="screenshot" width="400"/>


## app flowchart
- Helpful for understanding and navigating the code

<img src="https://github.com/jtris/steganography-app/blob/main/screenshots/flowchart.png" alt="flowchart" width="700"/>


## how to run
- I assume that python is already installed on your device
		
1. Clone
	``` cmd
	git clone https://github.com/jtris/steganography-app.git

 	cd steganography-app/src
	```

2. Install required packages
	``` cmd
	python3 -m pip install -r requirements.txt
	```

3. Run
	``` cmd
	python3 app.py
	```

