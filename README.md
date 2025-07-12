Problem Statement 2:-   
StackIt – A Minimal Q&A Forum Platform

team detauls :
team leader : Manoj Konireddy
team member-1 : Lakshmi Rupa Kalasapati
team member-2 : Rama Thulasi
team member-3 : Manoj Meka

# 🧠 StackIt – A Minimal Q&A Forum Platform

StackIt is a simple and clean Q&A platform inspired by Stack Overflow. Built for the Odoo Hackathon 2025, it allows users to ask and answer questions, vote on answers, and engage in community knowledge sharing.

## 🚀 Features

- 🔐 User Authentication (Register/Login)
- 📝 Ask Questions with:
  - Title
  - Rich Text Editor Description
  - Tags
- 💬 Answer Questions with rich formatting
- 👍 Voting System (Upvote/Downvote answers)
- 🏷️ Tagging System (Filter and categorize)
- 🛎️ Notifications (answers, mentions, comments)
- 📱 Mobile-Friendly Responsive UI
- 🔐 Role-Based Access: Guest, User, Admin

---

## 📁 Project Structure

```bash
stackit/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── utils.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── questions.py
│   │   │   ├── answers.py
│   │   │   ├── votes.py
│   ├── config.py
│   ├── run.py
│   └── .env
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── question.html
│   ├── ask-question.html
│   └── js/
│       ├── main.js
│       ├── auth.js
│       ├── question.js


