# MindDish.ai - Multimodal AI Cooking Assistant

**Ironhack Final Project - Building a Multimodal AI ChatBot for YouTube Video QA**

![MindDish.ai](https://img.shields.io/badge/MindDish.ai-Cooking%20Assistant-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-green)
![Accuracy](https://img.shields.io/badge/Accuracy-92.9%25-success)

##  Project Overview

MindDish.ai is an AI-powered cooking assistant that transforms how people interact with YouTube cooking videos. Instead of constantly pausing and rewinding, users can simply ask questions and get instant, accurate answers from a curated database of 28 cooking videos across 7 global cuisines.

**Live Demo:** [minddish.ai](https://minddish.ai)  
**API Endpoint:** [api.minddish.ai](https://api.minddish.ai)

---

##  Business Case

- **Accessibility:** Makes cooking content accessible to users with hearing impairments and language barriers
- **Efficiency:** Enables quick information retrieval from hours of video content
- **Educational Value:** Enhances learning with interactive Q&A and step-by-step guidance
- **Global Reach:** Multilingual support (English, Portuguese, Spanish, French, Nigerian languages)
- **User Engagement:** Natural conversation flow with context-aware responses

---

##  Key Features

###  Multi-Tool Agent System
17 specialized tools including:
- **Video QA** - Search and retrieve from 28 indexed cooking videos
- **Ingredient Extraction** - Parse recipe components
- **Cooking Time Estimation** - Calculate preparation and cooking times
- **Web Search** - Permission-based external recipe lookup
- **Recipe Comparison** - Cross-cuisine analysis

###  3-Layer Safety System
For ingredient substitutions:
- Allergen detection
- Dietary restriction validation
- Nutritional compatibility checks

###  Multilingual Support
- English, Portuguese, Spanish, French, Nigerian languages

###  Source Attribution
Every answer cites its source with video title and timestamp

###  Privacy-First Design
Permission-based web search puts users in control

---

##  Technical Architecture

### Data Layer
- **28 YouTube videos** across 7 cuisines (African, French, Portuguese, Jamaican, Syrian, Italian, Indian)
- **240 text chunks** extracted from transcripts
- **ChromaDB** vector database for semantic search
- **OpenAI text-embedding-3-small** for embeddings

### AI Layer
- **GPT-3.5-turbo** language model
- **LangChain** for agent orchestration
- **17 specialized tools** for diverse cooking queries
- **Session-based memory** for natural conversations

### Application Layer
- **FastAPI** backend (deployed on Render)
- **Next.js** frontend (deployed on Vercel)
- **Tavily API** for web search integration

---

##  Evaluation Results

| Metric | Result |
|--------|--------|
| **Accuracy** | 92.9% (improved from 90.9%) |
| **Test Pass Rate** | 100% |
| **Avg Response Time** | 1.77 seconds |
| **Cosine Similarity** | 0.7743 |
| **Total Chunks** | 240 |
| **Total Videos** | 28 |
| **Tools Available** | 17 |

---

##  Getting Started

### Prerequisites
```bash
Python 3.12+
OpenAI API Key
Tavily API Key (optional, for web search)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Affiwhizz/multimodal-youtube-qa-bot-project.git
cd multimodal-youtube-qa-bot-project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here (optional)
```

4. **Run the notebook**
```bash
jupyter notebook notebooks/MindDish_Development.ipynb
```

---

## 📁 Project Structure
```
multimodal-youtube-qa-bot-project/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── notebooks/
│   └── MindDish_Development.ipynb    # Main development notebook
├── data/
│   ├── curated_index.json            # Video metadata (28 videos)
│   └── transcripts/                  # Video transcripts (not in repo)
├── docs/
│   └── MindDish_Presentation.pptx    # Project presentation
├── evaluation/
│   └── evaluation_results.json       # Test results and metrics
└── src/
    ├── __init__.py
    ├── tools.py                       # Tool definitions
    ├── agent.py                       # Agent configuration
    └── config.py                      # Configuration settings
```

---

##  Technologies Used

- **Python 3.12** - Core programming language
- **LangChain** - Agent orchestration and tool management
- **OpenAI GPT-3.5-turbo** - Language model
- **ChromaDB** - Vector database
- **YouTube Transcript API** - Video transcript extraction
- **FastAPI** - Backend API framework
- **Next.js** - Frontend framework
- **Tavily API** - Web search integration

---

## 🎓 Key Learnings

1. **Real-world API constraints** - Adapted from yt-dlp to YouTube Transcript API due to anti-bot protections
2. **Security best practices** - Implemented environment variables, .gitignore, GitHub secret scanning
3. **Evaluation-driven improvement** - Systematic testing improved accuracy from 90.9% to 92.9%
4. **User experience matters** - Permission-based features, source attribution, safety systems
5. **Production deployment challenges** - ChromaDB persistence, environment configuration, API key management

---

## Future Enhancements

- [ ] Voice input/output for hands-free cooking
- [ ] Mobile app development
- [ ] Meal planning and shopping list generation
- [ ] More cuisines and video content
- [ ] Video timestamp linking
- [ ] Image recognition ("what ingredient is this?")
- [ ] Community recipe sharing
- [ ] Upgrade to GPT-4 for better accuracy

---

##  Project Deliverables

 **Source Code** - Complete implementation with LangChain integration  
 **Documentation** - Comprehensive README and inline comments  
 **Presentation** - PowerPoint slides in `/docs`  
 **Deployment** - Live web app at minddish.ai  
 **Evaluation** - Test results in `/evaluation`  
 **Agents & Tools** - 17 specialized tools with memory  
 **Vector Database** - ChromaDB with 240 chunks  

---

##  Author

**Affy** - AI Engineering Student, Ironhack Bootcamp  
- GitHub: [@Affiwhizz](https://github.com/Affiwhizz)
- Project: [minddish.ai](https://minddish.ai)

---

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

---

##  Acknowledgments

- **Ironhack** - For the project framework and guidance
