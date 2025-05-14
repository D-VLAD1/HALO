# 🔐 Secure Messenger HALO
**Secure Messenger** is an end-to-end encrypted chat application that allows users to exchange private messages with verified authenticity.

The project combines modern cryptographic techniques to ensure:

🔒 Confidentiality (no one but the recipient can read the message),

- ✅ Authenticity (messages are signed and verified),

- 🛡 Integrity (any tampering is immediately detected).

## ✨ Key Features:
Asymmetric encryption using Elliptic Curve Cryptography (ECC)

Digital signatures using DSA (Digital Signature Algorithm)

WebSocket-based server with FastAPI for real-time communication

Multiple clients: terminal interface & GUI (PyQt6, Tkinter, Kivy)

User presence & key exchange handled through the server

Friendly and lightweight UX

## 🔍 Why ECC + DSA?
Compared to traditional algorithms like RSA, ElGamal, and Rabin, ECC offers faster performance, smaller key sizes, and stronger security per bit.
DSA complements it by adding a layer of identity verification, ensuring that messages cannot be forged.

## 💡 Use Case
Imagine two people communicating over the internet.
Secure Messenger ensures that:

Only the intended recipient can read the message

The sender is who they claim to be

No one can alter the message silently


### Before you start - download all the requested libs.
```
pip install -r requirements.txt
```
### Now run this in your terminal:
```
python client_ui.py
```
or 
```
python3 client_ui.py
```
