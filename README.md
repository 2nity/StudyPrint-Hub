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
    ├── promo.mp4       # Group promotional video slot
    └── poster.jpg      # Video player poster thumbnail
```

---

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

---

## 📽️ Configuring the Promotional Video

The promotional video is embedded **exclusively on the Home / Landing Page**.

To add your group's commercial:
1. Place your MP4 video file inside the `assets/` directory.
2. Name the file `promo.mp4` (Target path: `assets/promo.mp4`).
3. Reload `index.html`. The video player will load `assets/promo.mp4` with `assets/poster.jpg` as thumbnail.

---

## 💻 How to Run locally in VS Code

You can host the project locally using Python's built-in HTTP server:

1. Open VS Code in the `StudyPrint-Hub` root folder.
2. Open the integrated terminal and run:
   ```bash
   python -m http.server 8000
   ```
3. Open your browser and navigate to:
   ```text
   http://localhost:8000
   ```

---

## 🌐 Deploying to GitHub Pages

1. Commit and push all files (`index.html`, `style.css`, `main.py`, `README.md`, `.gitignore`, `assets/`) to your GitHub repository.
2. Navigate to **Settings** > **Pages** in your repository.
3. Under **Branch**, select `main` (or `master`) and folder `/ (root)`.
4. Click **Save**. GitHub Pages will publish the static PyScript website at your repository URL.

---

*EVD & Business Analytics Final Exam Project 2026 — StudyPrint Hub*
