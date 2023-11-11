# Steganography Desktop App

## ❗ Important notes:
- This app's main purpose wasn't *steganography*, rather than just learning more about the process of creating a desktop application.
- Supports  _jpg_  and  _png_  files.
- I plan on making only a few more minor changes.
<br>

## Used packages (that aren't built-in)
- [CustomTkinter](https://customtkinter.tomschimansky.com/) 5.2.0+
- [Pillow](https://pillow.readthedocs.io/en/stable/) 8.2.0+
<br>

## Steganography technique
- For this project I chose to simply hide the given message, or data, in the image's **hex dump**, so there's no pixel/palette processing.

<img src="https://github.com/triskj0/steganography-app/blob/main/screenshots/hex_dump_hidden_message.png" alt="screenshot" width="700"/>

- We only have to append the binary data to the image file.
  - This would be the equialent command in a command line to hide a message:
<br>

  ``` cmd
  $ echo "this is a secret message" >> image.jpg
  ```
<br>

## GUI examples
<img src="https://github.com/triskj0/steganography-app/blob/main/screenshots/main_menu.png" alt="screenshot" width="490"/> <img src="https://github.com/triskj0/steganography-app/blob/main/screenshots/s2.png" alt="screenshot" width="490"/>
<img src="https://github.com/triskj0/steganography-app/blob/main/screenshots/s3.png" alt="screenshot" width="490"/> <img src="https://github.com/triskj0/steganography-app/blob/main/screenshots/s4.png" alt="screenshot" width="490"/>


## App flowchart
- Helpful for understanding and navigating the code

<img src="https://github.com/triskj0/steganography-app/blob/main/screenshots/flowchart.png" alt="flowchart" width="700"/>
