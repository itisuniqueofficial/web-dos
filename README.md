# web-dos

**web-dos** is a low-bandwidth HTTP DoS (Denial of Service) simulation tool, inspired by Slowloris.  
It allows you to test how your website or server responds to slow HTTP attacks by holding connections open using incomplete requests.

> ⚠️ **DISCLAIMER:**  
> This tool is for **educational** and **authorized** testing **only**. Do **not** use it without **explicit permission**.  
> Unauthorized use may be illegal under cybercrime laws.

---

## 🔧 Features

- Slow HTTP DoS (similar to Slowloris)
- Customizable socket count and timing
- HTTPS support
- SOCKS5 proxy support
- Randomized User-Agent headers
- Reconnects sockets if dropped
- Lightweight and scriptable

---

## 🐍 Requirements

- Python 3.6+
- Optional: `PySocks` for proxy support

```bash
pip install pysocks
````

---

## 📦 Installation

```bash
git clone https://github.com/itisuniqueofficial/web-dos.git
cd web-dos
python3 setup.py install
```

Or use it directly:

```bash
python3 web_dos.py --help
```

---

## 🚀 Usage

```bash
python3 web_dos.py <host> [options]
```

### Example

```bash
python3 web_dos.py example.com -s 200 --https --randuseragents --verbose
```

### Common Options

| Option                         | Description                                       |
| ------------------------------ | ------------------------------------------------- |
| `-s`, `--sockets`              | Number of sockets to use (default: 150)           |
| `--https`                      | Enable HTTPS connections                          |
| `-ua`, `--randuseragents`      | Randomize User-Agent headers                      |
| `--sleeptime`                  | Seconds to wait between each header (default: 15) |
| `-x`, `--useproxy`             | Use SOCKS5 proxy                                  |
| `--proxy-host`, `--proxy-port` | Set proxy host and port                           |
| `-v`, `--verbose`              | Enable detailed output                            |

---

## 📁 File Structure

```
web-dos/
├── web_dos.py        # Main attack script
├── setup.py          # Installation script
└── README.md         # This file
```

---

## 🧑‍💻 Author

**It Is Unique Official**

---

## 📝 License

MIT License – do whatever you want, but **don’t break the law.**
