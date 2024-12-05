# pyapktool

pyapktool is a Python command line utility that can help speed up common actions usually performed when reverse engineering 
Android apps:

* It can unpack Android app's apk file and extract all of its content (Smali code, libs, layouts XMLs etc.)
* It can pack an unpacked Android app's directory, back to an apk file (which usually happens after you create
any modification/patching to the app)
* It can sign a packed apk(by default-with debug keys. This is a required step in order to install your modified 
apk to any Android device)
* **No other prerequisite libraries installation/tools are needed to use this tool.** 
It will download/update any required tool ([apktool](https://github.com/iBotPeaches/Apktool), [apk-signer](https://github.com/patrickfav/uber-apk-signer)) automatically if needed.


### pyapktool is available on PyPI:

```
$ python -m pip install pyapktool
```

### How to use

Unpack an apk file (output will be located in a directory named 'myapp') :
```
$ pyapktool myapp.apk
```

Pack an unpacked Android app's directory, back to an apk file, and sign it with debug keys (output will be 'myapp-signed.apk'):
```
$ pyapktool myapp
```


