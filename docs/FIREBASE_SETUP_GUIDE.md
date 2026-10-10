# 🔥 Firebase Authentication & Cloud Storage Setup Guide
> **Step-by-step setup guide for 1st-year college students**

SAATHI AI supports **Google Firebase Authentication** (Email/Password and Google Login) and **Persistent Chat History**.

---

## 🛠️ How to Set Up Your Free Firebase Project (3 Minutes)

### Step 1: Create a Free Project on Firebase
1. Go to **[https://console.firebase.google.com](https://console.firebase.google.com)** and sign in with your Google account.
2. Click **"Add Project"** and name it `saathi-ai`.
3. (Optional) Disable Google Analytics for simplicity, then click **"Create Project"**.

---

### Step 2: Enable Authentication Providers
1. In the left sidebar of Firebase Console, click on **Build** -> **Authentication**.
2. Click **"Get Started"**.
3. Under the **Sign-in method** tab:
   - Click **Email/Password** -> Toggle **Enable** -> Click **Save**.
   - Click **Google** -> Toggle **Enable** -> Choose your support email -> Click **Save**.

---

### Step 3: Get Your Web API Key
1. In Firebase Console, click the **⚙️ Project Settings** gear icon (top left).
2. Under the **General** tab, look for **Web API Key** (starts with `AIzaSy...`).
3. Copy this key.

---

### Step 4: Add Key to SAATHI AI
Create or edit your `.env` file in the project folder:
```bash
FIREBASE_API_KEY=AIzaSyYourActualApiKeyHere
```
*Note: If you don't add a key right away, SAATHI AI automatically runs in **Local Demo Mode**, saving all your chats and users securely in `data/saathi_chat_history.db`!*
