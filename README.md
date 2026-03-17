# 🛡️ Cyber AI Shield

An intelligent cybersecurity web application built using **Streamlit** that detects network threats using AI/ML and provides real-time analytics, reports, and visualization dashboards.

---

## 🚀 Features

* 🔐 User Authentication (Login/Register)
* 🔍 Threat Detection using Machine Learning
* 📂 CSV File Upload & Viewer
* 📊 Interactive Dashboard
* 📈 Advanced Analytics (Risk, Severity, Attacks)
* 📄 Downloadable Reports
* ⚙️ Dynamic Settings Panel
* 🔄 Real-time Data Updates after Upload

---

## 🧠 How It Works

1. User uploads a CSV dataset
2. The model processes the data using `detect()` function
3. Predictions are generated:

   * Attack / Normal
   * Risk %
   * Severity Level
4. Results are visualized across Dashboard, Analytics, and Reports

---

## 📁 Project Structure

```
cyber-ai-shield/
│── app.py              # Main Streamlit application
│── predict.py          # ML model logic (detect function)
│── users.json          # User database (auto-created)
│── requirements.txt    # Dependencies
│── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/cyber-ai-shield.git
cd cyber-ai-shield
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Run the Application

```
streamlit run app.py
```

---

## 📊 Dataset Requirements

* CSV file format
* Ideally **41 columns** (for ML model compatibility)
* Corrupted rows are automatically ignored

---

## 🖥️ Application Flow

* Login / Register
* Upload dataset
* Detect threats
* View results in:

  * Dashboard
  * Analytics
  * Reports
  * Settings

---

## 📸 Screens (Optional)

*Add screenshots of your UI here for better presentation*

---

## 🚀 Future Improvements

* 🧠 Advanced attack classification (DoS, Probe, R2L, U2R)
* 🌐 Live network traffic monitoring
* 📡 Real-time alerts system
* ☁️ Cloud deployment (Streamlit Cloud / AWS)

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas & NumPy
* Plotly
* Machine Learning Model

---

## 👨‍💻 Author

Your Name
(Replace with your GitHub profile link)

---

## 📄 License

This project is for educational purposes.

---

## ⭐ Acknowledgment

Inspired by modern AI-based cybersecurity systems.

---

**💡 Tip:** Don’t forget to ⭐ star this repo if you like it!
