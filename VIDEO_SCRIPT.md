# MAT496 Capstone Video Script (SIMPLIFIED)
## AI-Powered Stock Analysis Agent
### Duration: 3 minutes (Face-to-camera only, no screen share)

---

## 🎬 Simple Script - Just You Talking

**[Your face visible on camera the entire time. Sit comfortably, smile, be natural]**

---

### INTRO (20 seconds)

"Hi, I'm [Your Name], and this is my MAT496 capstone project. I built an AI-powered stock analysis agent that helps individual investors make better investment decisions by generating professional-grade analysis using LLMs and retrieval augmented generation."

---

### WHAT IT DOES (30 seconds)

"So what does this agent do? It takes two simple inputs - a stock ticker symbol like AAPL or TSLA, and a time period like one year. Then it outputs a complete investment analysis with a BUY, HOLD, or SELL recommendation, risk assessment, price targets, and detailed fundamental analysis - basically what you'd get from a Goldman Sachs analyst."

---

### HOW IT WORKS (50 seconds)

"Here's how it works under the hood. It's built as a RAG pipeline with three phases.

First, the Retrieval phase - the agent calls four different APIs as tools: Yahoo Finance for real-time stock data, Alpha Vantage for financial fundamentals, NewsAPI for recent company news using semantic search, and the Federal Reserve API for economic indicators like Treasury rates.

Second, the Augmentation phase - all that retrieved data gets combined into one comprehensive context. Think P/E ratios, profit margins, debt levels, recent news headlines - everything gets structured into a prompt.

Third, the Generation phase - that augmented context goes to Groq's Llama 3.3 model with a carefully engineered prompt that acts like a senior equity analyst and generates a structured five-section investment memo."

---

### MAT496 CONCEPTS (50 seconds)

"This project demonstrates every major concept we learned in MAT496.

Prompting - I crafted institutional-grade prompts that make the LLM behave like a senior analyst.

Structured Output - the investment memos follow a consistent five-section format every time.

Semantic Search - the NewsAPI integration retrieves contextually relevant articles, not just keyword matching.

RAG - the entire pipeline retrieves from multiple sources then augments the LLM's context before generation.

Tool Calling - those four APIs act as tools the agent invokes dynamically based on what stock you analyze.

And Langgraph concepts - there's explicit state management using session state, modular processing nodes for each component, and a clear graph flow from data fetching through processing to analysis and display."

---

### WHY THIS PROJECT (30 seconds)

"I chose this project because financial markets generate massive amounts of unstructured data that most people can't process effectively. This is exactly the kind of problem LLMs and RAG were designed to solve. Plus, it let me demonstrate every MAT496 concept in a real-world application that actually provides value - it's not just a demo, I actually use this for my own investment research."

---

### EXAMPLE OUTPUT (20 seconds)

"To give you an idea of the output - when you analyze a stock, you get an executive summary with the investment thesis, fundamental analysis covering profitability and valuation, strategic analysis of competitive position, a detailed risk assessment with three bull case and three bear case factors, and finally a clear recommendation with price target and key catalysts to watch."

---

### CLOSING (20 seconds)

"This project shows how the concepts from MAT496 - RAG, tool calling, semantic search, structured prompting - can transform complex domains like financial analysis. The tools we learned are incredibly powerful when applied to real problems. Thanks for watching!"

**[Smile and wave]**

---

## 📝 Total Speaking Time Breakdown
- Intro: 20 seconds
- What it does: 30 seconds  
- How it works: 50 seconds
- MAT496 concepts: 50 seconds
- Why this project: 30 seconds
- Example output: 20 seconds
- Closing: 20 seconds
**Total: 3 minutes 20 seconds** (perfect for 3-5 min requirement)

---

## 💡 Tips for Recording

- **Just be yourself** - You're explaining your project, not giving a formal presentation
- **Smile and show enthusiasm** - You built something cool!
- **Don't memorize word-for-word** - Use this as a guide, speak naturally
- **Pause between sections** - Take a breath, it's okay
- **If you mess up** - Just restart, it's only 3 minutes
- **Look at the camera** - Not at yourself on screen
- **Speak clearly** - Slightly slower than normal conversation

---

## 🎯 Key Points to Emphasize

**Must mention these:**
1. Stock ticker input → Investment analysis output
2. Four APIs as tools (Yahoo, Alpha Vantage, News, FRED)
3. RAG pipeline: Retrieve → Augment → Generate
4. All MAT496 concepts covered
5. Real-world problem solved

---

## 📋 Quick Setup Checklist

- [ ] Good lighting on your face
- [ ] Quiet room (no background noise)
- [ ] Camera at eye level
- [ ] Sit comfortably
- [ ] Read through script once
- [ ] Record using screenrec.com or phone camera
- [ ] Watch recording once before uploading

---

## 📤 After Recording

1. Upload to YouTube as "Unlisted" OR Google Drive
2. Get shareable link
3. Add link to MAT496_README.md (line 213)
4. Done! ✅

---

**You've got this! Just talk naturally about your project for 3 minutes. It's that simple.** 🚀
