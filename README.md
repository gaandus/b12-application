# B12 Application Submission

This repository submits a signed application payload to B12 via GitHub Actions.

## Applicant

- Portfolio: https://dtanderson.net/
- LinkedIn: https://www.linkedin.com/in/daniel-anderson-52109721/
- GitHub: https://github.com/gaandus
- Resume (PDF): ./resume/Danny_Anderson_Resume.pdf

## How it works

A GitHub Action runs a Python script that:

- Builds a canonical JSON payload
- Signs it using HMAC-SHA256
- POSTs it to B12’s application endpoint
- Prints the receipt token for confirmation

## Running

1. Add GitHub Actions secrets:
   - B12_NAME
   - B12_EMAIL
   - B12_RESUME_LINK

2. Run the workflow:
   Actions → "B12 Application Submission" → Run workflow

3. Copy the printed receipt from logs into the application form.
