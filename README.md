# B12 Application Submission

This repository contains a small automation project used to submit my application to B12 via GitHub Actions.

The workflow builds a canonical JSON payload, signs it using HMAC-SHA256, and POSTs it to B12’s application endpoint.  
On success, the CI run prints a receipt token used to confirm submission.

---

## Applicant

Danny Anderson  
- Portfolio: https://dtanderson.net/  
- LinkedIn: https://www.linkedin.com/in/daniel-anderson-52109721/  
- GitHub: https://github.com/gaandus  

**Resume (PDF):**  
`.resume/Danny Anderson – Resume.pdf`

---

## How it works

1. A GitHub Action runs a Python script that:
   - Builds a sorted, compact JSON payload
   - Signs it with HMAC-SHA256
   - Sends it to `https://b12.io/apply/submission`

2. The action prints a receipt token returned by B12.

---

## Running the workflow

1. Configure GitHub Actions secrets:
   - `B12_NAME`
   - `B12_EMAIL`
   - `B12_RESUME_LINK`

2. Run:
   Actions → **B12 Application Submission** → Run workflow

3. Copy the printed receipt into the application form.
