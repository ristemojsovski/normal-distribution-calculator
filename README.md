# 📊 Normal Distribution Calculator

A modern desktop application for calculating probabilities and values of the normal distribution.

Built with **Python**, featuring an intuitive UI and interactive visualization.

## 📦 Download App

👉 [Download latest version](https://github.com/ristemojsovski/normal-distribution-calculator/releases)

---

## 🚀 Features

* 📈 Standard normal distribution (default: μ = 0, σ = 1)
* 🔄 Supports two calculation modes:

  * Input values → calculate probability
  * Input probability → calculate values
* 🎯 Four probability types:

  * `X ≤ q`
  * `X > q`
  * `q1 < X ≤ q2`
  * `X ≤ q1 OR X > q2`
* 📉 Interactive graph with shaded probability area
* 🎨 Clean and modern UI (CustomTkinter)

---

## 🖼️ Preview

![App Screenshot](assets/screenshot.png)

---

## 🛠️ Installation (Run from Source)

### 1. Clone the repository

```bash
git clone https://github.com/ristemojsovski/normal-distribution-calculator.git
cd normal-distribution-calculator
```

### 2. (Optional) Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

---

## 📦 Build Desktop App (Mac)

### Install PyInstaller

```bash
pip install pyinstaller
```

### Build the app

```bash
pyinstaller --windowed --name "NormalDistributionCalculator" --icon=assets/icon.icns app.py
```

### Output

The built application will be located in:

```text
dist/NormalDistributionCalculator.app
```

---

## 📦 Build Desktop App (Windows)

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico app.py
```

Output:

```text
dist/app.exe
```

---

## 📁 Project Structure

```text
normal-distribution-calculator/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   ├── icon.icns
│   ├── icon.ico
│   └── screenshot.png
│
├── dist/        (generated)
├── build/       (generated)
```

---

## 📚 Dependencies

* `customtkinter`
* `scipy`
* `matplotlib`
* `numpy`

---

## 🧠 How It Works

The app uses the normal distribution:

* PDF (probability density function)
* CDF (cumulative distribution function)
* PPF (inverse CDF)

From:

* `scipy.stats.norm`

---

## 🎯 Use Cases

* Students learning statistics
* Data analysts
* Quick probability calculations
* Teaching and demonstrations

---

## 📌 Notes

* macOS may block first launch → Right click → Open
* Or run:

```bash
xattr -cr dist/NormalDistributionCalculator.app
```

---

## 🤝 Contributing

Feel free to:

* fork the repo
* suggest improvements
* add new distributions (t, chi-square, etc.)

---

## 📄 License

MIT License

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
