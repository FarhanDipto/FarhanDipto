<picture>
  <source media="(max-width: 600px)" srcset="assets/hero-mobile.svg">
  <img src="assets/hero.svg" width="100%" alt="Farhan Abid Ahmed. AI Engineer at Gakk Media, Dhaka. Systems that turn a sentence into something real.">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/farhan-abid-ahmed/"><img src="https://img.shields.io/badge/LinkedIn-271F4D?style=for-the-badge&logo=linkedin&logoColor=4DD0E1" alt="LinkedIn"/></a>&nbsp;
  <a href="mailto:f.dipto5@gmail.com"><img src="https://img.shields.io/badge/Email-271F4D?style=for-the-badge&logo=gmail&logoColor=4DD0E1" alt="Email"/></a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&size=17&duration=3200&pause=1100&color=C9B8FF&center=true&vCenter=true&width=760&height=36&lines=AI+Engineer+%40+Gakk+Media+(BD)+Limited;Building+OneAI%2C+a+self-hosted+multi-LLM+hub;Turning+prompts+into+magic;Federated+learning+and+privacy-preserving+AI;OCR+that+reads+Bengali%2C+Arabic%2C+Devanagari%2C+CJK+and+Latin" alt="Typing SVG"/>
</p>

<br/>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/heading-about-dark-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/heading-about-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/heading-about-light-mobile.svg">
  <img src="assets/heading-about-light.svg" width="100%" alt="About">
</picture>

<img align="right" width="464" src="assets/profile-card.svg" alt="profile.json: role AI Engineer, team Gakk Media (BD) Limited, base Dhaka, degree CSE at AUST, previously federated learning at AISIP Lab, builds OneAI, deckforge and xlsx_gen"/>

AI Engineer at **Gakk Media (BD) Limited** in Dhaka. Building **OneAI**, a self-hosted multi-LLM platform that puts GPT, Claude, Gemini, Grok, DeepSeek and open-source models behind one API, at a fraction of the cost of paying for each one separately.

Before that, I was making AI system, ML models, federated learning and edge-fog-cloud systems at **AISIP Lab**, with a detour building OTT streaming backends. CSE graduate of **Ahsanullah University of Science & Technology**.

I mostly write systems that turn a sentence into something real: a slide deck, a spreadsheet, a document, a retrieved answer! Then I spend an unreasonable amount of time making sure the output doesn't quietly lie to the renderer.

<br clear="right"/>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/heading-building-dark-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/heading-building-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/heading-building-light-mobile.svg">
  <img src="assets/heading-building-light.svg" width="100%" alt="What I'm building">
</picture>

<table>
<tr>
<td width="50%" valign="top">

### 🧠 OneAI &nbsp;<sup><code>ai-hub-api</code></sup>

Bangladesh's first self-hosted multi-LLM hub. Search-augmented chat over SSE, tiered scraping, and a Redis-backed context system that auto-summarizes at 65% of the token budget before hard-truncating at 88%.

<img src="https://img.shields.io/badge/Redis-0B0E23?style=flat-square&logo=redis&logoColor=4DD0E1" alt="Redis"/> <img src="https://img.shields.io/badge/SSE-0B0E23?style=flat-square" alt="SSE"/> <img src="https://img.shields.io/badge/Multi--LLM%20routing-0B0E23?style=flat-square" alt="Multi-LLM routing"/>

</td>
<td width="50%" valign="top">

### 🔍 oneai-search

A production-grade AI search and scraping service built on SearXNG, rotating proxy pools, and tiered extraction (Trafilatura + Crawl4AI). Decoupled into its own vertical-slice service with Postgres-backed caching and isolated browser workers.

<img src="https://img.shields.io/badge/SearXNG-0B0E23?style=flat-square&logo=searxng&logoColor=4DD0E1" alt="SearXNG"/> <img src="https://img.shields.io/badge/Postgres-0B0E23?style=flat-square&logo=postgresql&logoColor=4DD0E1" alt="Postgres"/> <img src="https://img.shields.io/badge/Crawl4AI-0B0E23?style=flat-square" alt="Crawl4AI"/>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📽️ deckforge &nbsp;<sup><code>pptx_gen</code></sup>

A spec-driven PowerPoint engine. An LLM emits a content-only `DeckSpec`, and everything about how the deck _looks_ (palette, typography, composition, icons) is decided downstream by code, not the model.

<img src="https://img.shields.io/badge/DeckSpec-0B0E23?style=flat-square" alt="DeckSpec"/> <img src="https://img.shields.io/badge/TTF%20metrics-0B0E23?style=flat-square" alt="TTF metrics"/> <img src="https://img.shields.io/badge/Delta--E%20checks-0B0E23?style=flat-square" alt="Delta-E checks"/>

</td>
<td width="50%" valign="top">

### 📊 xlsx_gen

The same architecture for spreadsheets. Natural language becomes a `WorkbookSpec` JSON, resolved by a deterministic `openpyxl` renderer into live formulas and native charts.

<img src="https://img.shields.io/badge/WorkbookSpec-0B0E23?style=flat-square" alt="WorkbookSpec"/> <img src="https://img.shields.io/badge/openpyxl-0B0E23?style=flat-square" alt="openpyxl"/> <img src="https://img.shields.io/badge/Live%20formulas-0B0E23?style=flat-square" alt="Live formulas"/>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🗂️ Document extraction registry

A unified extraction layer for RAG (PDF / DOCX / XLSX / Images), with automatic script detection routing pages to the right OCR model: Bengali, Arabic, Devanagari, CJK, Latin.

<img src="https://img.shields.io/badge/Multi--script%20OCR-0B0E23?style=flat-square" alt="Multi-script OCR"/> <img src="https://img.shields.io/badge/PDF%20%2F%20DOCX%20%2F%20XLSX-0B0E23?style=flat-square" alt="PDF / DOCX / XLSX"/>

</td>
<td width="50%" valign="top">

### 📰 Bangladesh news RAG

A news retrieval pipeline built on BGE-M3 embeddings and Qdrant hybrid dense+sparse retrieval with RRF fusion, validated end-to-end with RAGAS.

<img src="https://img.shields.io/badge/Qdrant-0B0E23?style=flat-square&logo=qdrant&logoColor=4DD0E1" alt="Qdrant"/> <img src="https://img.shields.io/badge/BGE--M3-0B0E23?style=flat-square" alt="BGE-M3"/> <img src="https://img.shields.io/badge/RAGAS-0B0E23?style=flat-square" alt="RAGAS"/>

</td>
</tr>
</table>

<br/>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/heading-stack-dark-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/heading-stack-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/heading-stack-light-mobile.svg">
  <img src="assets/heading-stack-light.svg" width="100%" alt="Tech stack">
</picture>

<table>
<tr>
<td align="right" width="190"><b>AI / ML</b></td>
<td><img src="https://skillicons.dev/icons?i=pytorch,tensorflow,opencv&theme=dark" alt="PyTorch, TensorFlow, OpenCV"/></td>
</tr>
<tr>
<td align="right"><b>Infrastructure</b></td>
<td><img src="https://skillicons.dev/icons?i=docker,kubernetes,kafka,nginx,linux&theme=dark" alt="Docker, Kubernetes, Kafka, Nginx, Linux"/></td>
</tr>
<tr>
<td align="right"><b>Data &amp; storage</b></td>
<td><img src="https://skillicons.dev/icons?i=postgres,mongodb,mysql,redis,elasticsearch&theme=dark" alt="Postgres, MongoDB, MySQL, Redis, Elasticsearch"/></td>
</tr>
<tr>
<td align="right"><b>Full-stack</b></td>
<td><img src="https://skillicons.dev/icons?i=react,nodejs,express,flask,fastapi&theme=dark" alt="React, Node.js, Express, Flask, FastAPI"/></td>
</tr>
<tr>
<td align="right"><b>Languages</b></td>
<td><img src="https://skillicons.dev/icons?i=python,js,java,cpp,php&theme=dark" alt="Python, JavaScript, Java, C++, PHP"/></td>
</tr>
<tr>
<td align="right" valign="top"><b>LLM &amp; agents</b></td>
<td>
<img src="https://img.shields.io/badge/LangChain-0B0E23?style=flat-square&logo=langchain&logoColor=4DD0E1" alt="LangChain"/>
<img src="https://img.shields.io/badge/LangGraph-0B0E23?style=flat-square&logo=langgraph&logoColor=4DD0E1" alt="LangGraph"/>
<img src="https://img.shields.io/badge/vLLM-0B0E23?style=flat-square&logo=vllm&logoColor=4DD0E1" alt="vLLM"/>
<img src="https://img.shields.io/badge/LiteLLM-0B0E23?style=flat-square" alt="LiteLLM"/>
<img src="https://img.shields.io/badge/Hugging%20Face-0B0E23?style=flat-square&logo=huggingface&logoColor=4DD0E1" alt="Hugging Face"/>
<img src="https://img.shields.io/badge/Ollama-0B0E23?style=flat-square&logo=ollama&logoColor=4DD0E1" alt="Ollama"/>
<img src="https://img.shields.io/badge/Model%20Context%20Protocol-0B0E23?style=flat-square&logo=modelcontextprotocol&logoColor=4DD0E1" alt="Model Context Protocol"/>
<img src="https://img.shields.io/badge/Federated%20Learning%20(FLWR)-0B0E23?style=flat-square&logo=flower&logoColor=4DD0E1" alt="Federated Learning (FLWR)"/>
<img src="https://img.shields.io/badge/Qdrant-0B0E23?style=flat-square&logo=qdrant&logoColor=4DD0E1" alt="Qdrant"/>
<img src="https://img.shields.io/badge/FAISS-0B0E23?style=flat-square" alt="FAISS"/>
<img src="https://img.shields.io/badge/DeepSeek%20API-0B0E23?style=flat-square&logo=deepseek&logoColor=4DD0E1" alt="DeepSeek API"/>
<img src="https://img.shields.io/badge/OpenAI%20API-0B0E23?style=flat-square" alt="OpenAI API"/>
<img src="https://img.shields.io/badge/Anthropic%20API-0B0E23?style=flat-square&logo=anthropic&logoColor=4DD0E1" alt="Anthropic API"/>
<img src="https://img.shields.io/badge/Gemini%20API-0B0E23?style=flat-square&logo=googlegemini&logoColor=4DD0E1" alt="Gemini API"/>
</td>
</tr>
</table>

<br/>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/heading-stats-dark-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/heading-stats-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/heading-stats-light-mobile.svg">
  <img src="assets/heading-stats-light.svg" width="100%" alt="GitHub stats">
</picture>

<p align="center">
  <img height="170" src="https://github-readme-stats.vercel.app/api?username=FarhanDipto&show_icons=true&hide_border=true&border_radius=14&bg_color=35,0B0E23,171540&title_color=4DD0E1&icon_color=9B5DE5&text_color=E8E8F0&ring_color=9B5DE5" alt="GitHub stats"/>
  <img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=FarhanDipto&layout=compact&hide_border=true&border_radius=14&bg_color=35,0B0E23,171540&title_color=4DD0E1&text_color=E8E8F0&langs_count=8" alt="Top languages"/>
</p>

<p align="center">
  <img src="https://streak-stats.demolab.com?user=FarhanDipto&hide_border=true&border_radius=14&background=35,0B0E23,171540&ring=4DD0E1&fire=9B5DE5&currStreakLabel=4DD0E1&sideLabels=E8E8F0&dates=8E8EAB&currStreakNum=E8E8F0&sideNums=E8E8F0" alt="Contribution streak"/>
</p>

<br/>

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/heading-activity-dark-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/heading-activity-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/heading-activity-light-mobile.svg">
  <img src="assets/heading-activity-light.svg" width="100%" alt="Contribution graph">
</picture>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=FarhanDipto&bg_color=0B0E23&color=C9B8FF&line=9B5DE5&point=4DD0E1&area=true&area_color=271F4D&hide_border=true&radius=14&custom_title=Contributions%2C%20last%2031%20days" width="100%" alt="Contribution activity, last 31 days"/>
</p>

<p align="center">
  <img src="./profile-3d-contrib/profile-nebula.svg" width="100%" alt="Isometric 3D contribution calendar"/>
</p>

<br/>

<!-- <picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/heading-connect-dark-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/heading-connect-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/heading-connect-light-mobile.svg">
  <img src="assets/heading-connect-light.svg" width="100%" alt="Connect">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/farhan-abid-ahmed/"><img src="https://img.shields.io/badge/Let's_connect-LinkedIn-0B0E23?style=for-the-badge&labelColor=271F4D&logo=linkedin&logoColor=4DD0E1" alt="Connect on LinkedIn"/></a>&nbsp;
  <a href="mailto:f.dipto5@gmail.com"><img src="https://img.shields.io/badge/Say_hi-Email-0B0E23?style=for-the-badge&labelColor=271F4D&logo=gmail&logoColor=4DD0E1" alt="Send an email"/></a>
</p>

<br/> -->

<picture>
  <source media="(max-width: 600px)" srcset="assets/footer-mobile.svg">
  <img src="assets/footer.svg" width="100%" alt="Thanks for stopping by.">
</picture>
