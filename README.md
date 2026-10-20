# StudyPrint Hub — Professional Interactive Business Website
### EVD and Business Analytics Final Exam Project 2026

StudyPrint Hub is a modern, student-focused document and printing services web application. It features working **PyScript** client-side event execution, live price estimation, real-time service searching and category filtering, and interactive demonstration receipt generation.

---

## 📁 Project Structure

```text
StudyPrint-Hub/
├── index.html          # Semantic HTML structure & PyScript configuration
├── style.css           # Modular CSS stylesheet (Colors, Typography, Layouts)
├── main.py             # Python logic (Calculations, Filtering, Validation)
├── README.md           # Documentation & instructions
├── .gitignore          # Version control exclusion rules
└── assets/
    ├── logo.svg        # Original vector brand logo (Printer + Wordmark)
    ├── adverisement.mp4# Group advertisement video slot
    └── poster.jpg      # Video player poster thumbnail
```


## 🛠️ How HTML, CSS, and PyScript Work Together

1. **`index.html`**:
   - Contains clean semantic sections: Navigation Header, Hero/Home, Services, Price Calculator, Order Request, About Us, Contact, and Footer.
   - Links `style.css` in the `<head>` tag.
   - Loads PyScript 2024.1 engine and imports `main.py` asynchronously via `<script type="py" src="main.py" async></script>`.
   - Uses `py-click="function_name()"` attributes to connect UI buttons directly to Python functions.

2. **`style.css`**:
   - Stores custom CSS variables (`--brand-navy`, `--brand-blue`, `--brand-yellow`, `--brand-bg`), typography, card hover animations, glassmorphism header, video container styles, and responsive breakpoints.

3. **`main.py`**:
   - Maintains the centralized `SERVICES_DATA` dictionary.
   - Implements `@when` decorators and global Python functions for live search filtering, service selection, quantity stepping, price calculation, validation, form handling, and modal receipt generation.

*EVD & Business Analytics Final Exam Project 2026 — StudyPrint Hub*
