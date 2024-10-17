# SecureMessage

**SecureMessage** is an easy-to-use application for encrypting and decrypting messages using the Fernet encryption method. With a simple interface, you can securely encrypt your messages and share them with others who have the same application to decrypt them.

## Features

- Encrypt any text-based message.
- Decrypt encrypted messages.
- Copy the results to the clipboard with a single click.
- Clear input and output fields.
- User-friendly and intuitive graphical interface (GUI).
## Requirements

Before running this project, ensure you have the following installed on your system:

### 1. Python 3.x
You can download the latest version of Python from the official website:  
[Python Downloads](https://www.python.org/downloads/)

Make sure Python is correctly installed by running:

```bash
python --version
```

### 2. Required Libraries
This project relies on the following libraries, which can be installed via pip:

 - **cryptography** *(for message encryption and decryption)*
 - **tkinter** *(usually comes bundled with Python, used for the graphical interface)*
   
To install the required libraries, simply run the following command:

```bash
pip install cryptography
```
```bash
pip install tkinter
```

## 3. Download the Executable

If you don't want to install Python or the required libraries, you can simply download the pre-compiled executable from the [Releases](https://github.com/YourUsername/SecureMessage/releases) section. Follow these steps:

1. Go to the [Releases](https://github.com/YourUsername/SecureMessage/releases) page.
2. Download the latest version of the executable (e.g., `SecureMessage.exe` for Windows users).
3. Run the executable file directly.

No need to install Python or additional libraries—just download and start using it!

## Application Walkthrough

1. **Message Field**: Enter any plain text message that you want to encrypt or decrypt.
   
2. **Encrypt Button**: Press this button to encrypt the message. The encrypted result will appear in the result field.
   
3. **Decrypt Button**: Press this button to decrypt an encrypted message. The decrypted result will appear in the result field.

4. **Copy Button**: Easily copy the result (whether encrypted or decrypted) to the clipboard for sharing or saving elsewhere.

5. **Clear Button**: Use this to clear both the input and result fields.

## 3. Contributing

Feel free to contribute to this project! If you have any suggestions, issues, or feature requests, please open an issue or submit a pull request.

### Steps for contributing:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



