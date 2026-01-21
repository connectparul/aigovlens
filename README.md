# 🔍 AIGovLens

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aigovlens.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> **Open source AI governance toolkit — See AI risks clearly**

Evaluate AI use cases against regulatory frameworks (EU AI Act, Colorado AI Act, GDPR) and generate compliance-ready governance reports.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏛️ **Regulatory Analysis** | Automatic mapping to EU AI Act, Colorado AI Act, NYC LL144 |
| ⚖️ **Bias Risk Assessment** | Identifies fairness concerns and affected groups |
| 🔒 **Privacy Evaluation** | GDPR, data handling, and consent analysis |
| 👁️ **Transparency Check** | Explainability and disclosure requirements |
| 📄 **PDF Reports** | Professional governance reports for stakeholders |
| 🤖 **LLM-Powered** | Uses Groq (Llama 3) for intelligent analysis |

---

## 🚀 Quick Start

### Option 1: Use Hosted Version
Visit: **[aigovlens.streamlit.app](https://aigovlens.streamlit.app)**

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/aigovlens.git
cd aigovlens

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 3: Deploy Your Own

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub
4. Select the forked repo
5. Add your `GROQ_API_KEY` in Secrets
6. Deploy!

---

## 🔑 API Setup

AIGovLens uses **Groq** (free tier) for AI analysis.

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Create an API key
4. Add it to the app:
   - **Locally**: Enter in sidebar
   - **Streamlit Cloud**: Add to Secrets as `GROQ_API_KEY`

---

## 📁 Project Structure

```
aigovlens/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Documentation
├── LICENSE             # MIT License
└── .streamlit/
    └── config.toml     # Streamlit theme configuration
```

---

## 🎯 How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   INPUT     │     │   ANALYZE   │     │   ASSESS    │     │   OUTPUT    │
│             │────▶│             │────▶│             │────▶│             │
│ Use Case    │     │ Send to LLM │     │ Risk Scores │     │ PDF Report  │
│ Details     │     │ with Rules  │     │ & Actions   │     │ Dashboard   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

1. **Enter** your AI use case details (name, description, data types, markets)
2. **Analyze** against regulatory frameworks using LLM
3. **Receive** risk scores across 4 dimensions
4. **Export** professional PDF governance report

---

## 📊 Risk Dimensions

| Dimension | What It Checks |
|-----------|----------------|
| 🏛️ **Regulatory** | EU AI Act classification, Colorado AI Act, NYC LL144, sector rules |
| ⚖️ **Bias & Fairness** | Discrimination risk, affected groups, historical domain bias |
| 🔒 **Privacy** | PII handling, GDPR compliance, consent, data retention |
| 👁️ **Transparency** | Explainability, user notification, human oversight needs |

---

## 📸 Screenshots

### Input Form
Enter your AI use case details:
- Name & department
- AI techniques used
- Target markets
- Data types involved
- Detailed description

### Results Dashboard
View comprehensive analysis:
- Overall risk score (0-100)
- Risk level (HIGH/MEDIUM/LOW)
- Four-dimension breakdown
- Prioritized action items

### PDF Report
Export professional report including:
- Executive summary
- Risk assessment matrix
- Recommended actions
- Applicable regulations

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM | Groq (Llama 3.1 70B) |
| PDF Generation | ReportLab |
| Hosting | Streamlit Cloud |

---

## 💰 Cost

**$0** — Completely free to use!

| Service | Cost |
|---------|------|
| Groq API | Free tier |
| Streamlit Cloud | Free |
| GitHub | Free |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions
- [ ] Add more regulatory frameworks (NIST AI RMF, ISO 42001)
- [ ] Batch evaluation of multiple use cases
- [ ] Historical tracking and comparison
- [ ] Custom evaluation criteria
- [ ] Integration with GRC platforms

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

AIGovLens provides **informational guidance only** and does not constitute legal advice. Always consult with qualified legal and compliance professionals for official governance decisions.

---

## 👤 Author

**Parul Khanna**
- [Email](mailto:parulkcyber@gmail.com)

---

## 🌟 Star History

If you find this useful, please ⭐ star the repository!

---

<p align="center">
  <b>Built with ❤️ for the AI governance community</b>
</p>
