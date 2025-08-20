
# GoogleGemini-ImageClassifier

🚀 A Flask-based project that integrates **Google Gemini AI** and **MediaPipe** to classify images into meaningful hashtags. It detects faces, evaluates confidence, checks activity type, and saves results into an **Excel file** for further use.

---

## 📌 Features

* ✅ Upload Excel files containing image URLs
* ✅ Downloads and processes each image
* ✅ Detects faces using **MediaPipe**
* ✅ Classifies images into hashtags using **Google Gemini AI** based on **custom rules**
* ✅ Supports indoor/outdoor detection, sitting/standing posture, and activity type
* ✅ Automatically updates results in `updated_file.xlsx`
* ✅ Skips already processed URLs to save time
* ✅ Alerts when low confidence face detection requires manual review

---

## 🏷️ Custom Hashtags & Rules

This project defines **specific hashtags** and rules inside the classification prompt. Images are categorized based on  **visibility of humans, activity type, and context** .

Some examples:

* **🌱 earthivist** → Human must be visible and activity should be related to the environment (e.g., watering plants, growing plants, using dustbins).
* **🐾 chiefanimalofficer** → Human must be visible and engaged in animal welfare activities (e.g., feeding strays, caring for pets).
* **💪 wellnesschamp** → Human must be visible and performing physical or mental wellness activities (e.g., sports like chess/cricket, yoga, meditation).
* **🎨 artist** → Human must be visible and engaged in artistic activities (e.g., painting, drawing, artwork).
* **🙌 promotivator** → If an image does not fit into any category OR meets conditions without showing a visible human (e.g., only a hand watering plants, no face visible).
* **⚠️ inappropriate** → Spam, violence, nudity, or harmful content.

👉 All hashtags and their conditions are explicitly defined in the **prompt** used for Gemini AI.

---

## 🛠️ Tech Stack

* **Flask** – REST API framework
* **Google Generative AI (Gemini)** – Image classification
* **MediaPipe** – Face detection
* **OpenCV** – Image processing
* **Numpy** – Numerical operations
* **Pandas** – Excel file management

---

## 📂 Folder Structure

<pre class="overflow-visible!" data-start="3027" data-end="3378"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>GoogleGemini-ImageClassifier/
│── app.py                </span><span># Main Flask application</span><span>
│── requirements.txt      </span><span># Python dependencies</span><span>
│── .gitignore            </span><span># Ignore unnecessary files</span><span>
│── updated_file.xlsx     </span><span># Auto-generated results file</span><span>
│── images/               </span><span># Temporary downloaded images</span><span>
│── README.md             </span><span># Project documentation</span><span>
</span></span></code></div></div></pre>

---

## ⚡ Installation

1. Clone the repository:
   <pre class="overflow-visible!" data-start="3435" data-end="3565"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/your-username/GoogleGemini-ImageClassifier.git
   </span><span>cd</span><span> GoogleGemini-ImageClassifier
   </span></span></code></div></div></pre>
2. Create and activate virtual environment:
   <pre class="overflow-visible!" data-start="3616" data-end="3743"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m venv venv
   </span><span>source</span><span> venv/bin/activate   </span><span># On Linux/Mac</span><span>
   venv\Scripts\activate      </span><span># On Windows</span><span>
   </span></span></code></div></div></pre>
3. Install dependencies:
   <pre class="overflow-visible!" data-start="3775" data-end="3826"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -r requirements.txt
   </span></span></code></div></div></pre>
4. Add your **Google Gemini API key** in `app.py`:
   <pre class="overflow-visible!" data-start="3884" data-end="3930"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>api_key = </span><span>"YOUR_API_KEY"</span><span>
   </span></span></code></div></div></pre>
5. Run the Flask app:
   <pre class="overflow-visible!" data-start="3959" data-end="3992"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python app.py
   </span></span></code></div></div></pre>

---

## 🚀 Usage

1. Send a POST request with an Excel file:
   <pre class="overflow-visible!" data-start="4061" data-end="4152"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>curl -X POST -F </span><span>"file=@input.xlsx"</span><span> http://127.0.0.1:5000/processexcelll
   </span></span></code></div></div></pre>
2. Excel file must contain these columns:
   * `sno`
   * `urls` (comma-separated image URLs)
   * `hashtag`
   * `Gemini_hashtag`
3. Processed results will be stored in:
   <pre class="overflow-visible!" data-start="4341" data-end="4374"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>updated_file.xlsx
   </span></span></code></div></div></pre>

---

## 📊 Example Output

<pre class="overflow-visible!" data-start="4404" data-end="4638"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span>{</span><span>
  </span><span>"hashtag"</span><span>:</span><span></span><span>"earthivist"</span><span>,</span><span>
  </span><span>"visible"</span><span>:</span><span></span><span>"1"</span><span>,</span><span>
  </span><span>"number_of_faces"</span><span>:</span><span></span><span>"2"</span><span>,</span><span>
  </span><span>"activity_type"</span><span>:</span><span></span><span>"indoor"</span><span>,</span><span>
  </span><span>"game"</span><span>:</span><span></span><span>"sudoku"</span><span>,</span><span>
  </span><span>"posture"</span><span>:</span><span></span><span>"standing"</span><span>,</span><span>
  </span><span>"confidence_score"</span><span>:</span><span></span><span>0.82</span><span>,</span><span>
  </span><span>"image_url"</span><span>:</span><span></span><span>"https://example.com/img1.jpg"</span><span>
</span><span>}</span><span>
</span></span></code></div></div></pre>

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

MIT License © 2025
