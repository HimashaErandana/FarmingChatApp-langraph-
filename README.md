# AgroGo – AI Chat & Farming Assistant for Sri Lankan Rice Farmers 🌾🤖

**AgroGo** is an AI-powered platform designed to help rice farmers access actionable insights about farming, including **weather, soil conditions, pesticide usage, and disease detection**. The system combines **machine learning, natural language processing, and knowledge graphs** to provide real-time guidance and decision support.

---

## 🚀 Features

- **Chat Interface:** Farmers can ask questions and receive instant responses related to farming practices.  
- **RAG-based Document Retrieval:** Answers are retrieved from agriculture documents supplied by the government using a **Retrieval-Augmented Generation (RAG)** pipeline.  
- **Rice Leaf Disease Detection:** Integrated **CNN (EfficientNet)** model for early detection of diseases from uploaded images.  
- **Real-time Weather Updates:** Fetches weather information using **OpenWeather API**.  
- **Knowledge Graph Integration:** **LangGraph** structures agricultural knowledge for accurate and actionable responses.  
- **Secure Authentication:** Users are managed securely using **JWT**.  
- **Vector Search:** **Chroma VectorDB** and **Sentence Transformers** enable semantic search of agriculture documents.  

---

## 🛠️ Tech Stack

- **Frontend:** React (Interactive Chat UI)  
- **Backend:** FastAPI (API & Model Serving)  
- **Authentication:** JWT  
- **AI / ML:** **OLLAMA (Local LLM Hosting)**, EfficientNet CNN, Sentence Transformers  
- **Knowledge Graph & Orchestration:** LangGraph, LangChain (RAG & workflow)  
- **Databases:** MongoDB (**hosted locally in Docker**), Chroma VectorDB  

---

## 📁 Project Structure


---

## 📈 How It Works

1. **User Query:** A farmer types a question into the chat interface.  
2. **RAG Pipeline:** The system retrieves relevant documents from **Chroma VectorDB** using **Sentence Transformers embeddings**.  
3. **LLM Response:** **OLLAMA hosts a local LLM** that generates contextual answers from retrieved documents.  
4. **Knowledge Graph:** **LangGraph** structures the data to ensure accurate and actionable responses.  
5. **Disease Detection:** If an image is uploaded, **EfficientNet CNN** predicts disease presence.  
6. **Weather Info:** The app fetches real-time weather data from **OpenWeather API**.  
7. **Data Storage:** User data, chat logs, and agricultural information are stored in **MongoDB running locally in a Docker container**.  

---

## 📊 Outcomes / Impact

- Farmers can make **informed decisions** about crop care and pesticide usage.  
- **Early detection** of rice leaf diseases helps prevent crop loss.  
- Provides **centralized, real-time agricultural knowledge** to improve productivity.  

---

