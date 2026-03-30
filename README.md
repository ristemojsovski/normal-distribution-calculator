# 📊 Normal Distribution Calculator

A modern, interactive calculator for the **normal distribution**, available both as:

* 🖥️ Desktop application (PyInstaller)
* 🌐 Web application (Streamlit)

Designed for students, analysts, and professionals who need quick and intuitive probability calculations.

---

## 🌐 Live Web App

👉 **Use instantly in your browser**
[Open Calculator](https://ndcalculator.streamlit.app)

---

## 📦 Desktop App (Download)

👉 Download the latest version from:
[Releases](https://github.com/ristemojsovski/normal-distribution-calculator/releases)

### macOS Instructions

1. Download `.zip`
2. Unzip the file
3. Right-click → **Open**

If macOS blocks the app:

```bash
xattr -cr NormalDistributionCalculator.app
```

---

## 🚀 Features

* 📈 Normal distribution with default:

  * Mean (μ) = 0
  * Standard deviation (σ) = 1

* 🔄 Two calculation modes:

  * **Input values → calculate probability**
  * **Input probability → calculate values**

* 🎯 Supported probability types:

  * `X ≤ q`
  * `X > q`
  * `q1 < X ≤ q2`
  * `X ≤ q1 OR X > q2`

* 📉 Interactive visualization:

  * Real-time plotted distribution
  * Shaded probability regions

* 🎨 Clean UI:

  * Desktop: CustomTkinter
  * Web: Streamlit

---

## 🧠 Mathematical Background

The application is based on the **normal distribution**:

* Probability Density Function (PDF)
* Cumulative Distribution Function (CDF)
* Percent Point Function (PPF, inverse CDF)

Implemented using:

```python
scipy.stats.norm
```

---

## 🖥️ Run Desktop App (from source)

```bash
git clone https://github.com/ristemojsovski/normal-distribution-calculator.git
cd normal-distribution-calculator

pip install -r requirements.txt
python app.py
```

---

## 🌐 Run Web App (Streamlit locally)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open:

```text
http://localhost:8501
```

---

## 🏗️ Build Desktop App (Mac)

```bash
pip install pyinstaller
pyinstaller --windowed --name "NormalDistributionCalculator" --icon=assets/icon.icns app.py
```

Output:

```text
dist/NormalDistributionCalculator.app
```

---

## 🏗️ Build Desktop App (Windows)

```bash
pyinstaller --onefile --windowed --icon=assets/icon.ico app.py
```

---

## 📁 Project Structure

```text
normal-distribution-calculator/
│
├── app.py                         # Desktop application (Tkinter)
├── streamlit_app.py              # Web application (Streamlit)
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/                       # Icons, images
│   ├── icon.icns
│   ├── icon.ico
│   └── screenshot.png
│
├── dist/                         # Build output (ignored)
├── build/                        # Build temp (ignored)
└── venv/                         # Virtual env (ignored)
```

---

## 📦 Dependencies

* `streamlit`
* `customtkinter`
* `scipy`
* `matplotlib`
* `numpy`

---

## ⚠️ Notes

* `.app` files are macOS bundles → must be zipped before sharing
* macOS may block unsigned apps → use `xattr -cr`
* `dist/`, `build/`, and `venv/` are excluded via `.gitignore`

---

## 🤝 Contributing

Contributions are welcome:

* Add new distributions (t, chi-square, binomial)
* Improve UI/UX
* Optimize performance

---

## 📄 License

MIT License

---

## ⭐ Support

If you find this project useful, please ⭐ the repository!
