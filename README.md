# Grub AI 💌

[Grub AI](https://grub-poem-ai.onrender.com/) is a subscription based website that delivers curated poems right into your inbox, and yes with no login required. The poems are not hand crafted sadly. The website leverages `ai-agents`, thanks to langchain, to generate these poems based on a given set of themes.
Moreover, a `set_frequency` function, that gets automatically triggered once the emails are verified, lets you decide how often you want your poems.

## Purpose -

For fun.

## Full Documentation :

1. [FastApi + Docker](#1-fastapi-and-docker-setup)
2. [LLMs]((#2-llms-via-langchain))
3. [Cron job](#3-cron-job-integration)

### 1. FastApi and Docker setup -

The is a single container, monorepo project. That is, the project is made on FastApi and runs on docker and is hosted at the same port but can be hosted on different services if required.
For simplicity the static files were copied inside the backend directory right before deployment so, there is no need to deploy them differently (backend and frontend). 

### 2. LLMs via LangChain

The poem generation is handled by a lightweight LangChain setup:

- `llm.py` initializes a local or remote LLM (OpenRouter, SmolLM, etc.)
- `poem_service.py` defines prompt templates and query logic
- Themes are passed dynamically to generate fresh poems each time

All output is wrapped into an `EmailMessageSchema` which contains the poem’s subject and body.

### 3. Cron Job Integration

Poems are delivered based on user-defined frequency:

- A cron-compatible script (`cron_job.py`) runs **once per day**

  ![image](https://github.com/user-attachments/assets/8bcca6df-544d-4d54-b624-86bef06b2fa3)


- Each user is evaluated based on their `frequency` (`daily`, `weekly`)
- A random theme is selected

  ![image](https://github.com/user-attachments/assets/dfda458e-6aac-4969-974a-370c6c9a8269)
  
- A poem is generated and emailed to the user

  ![image](https://github.com/user-attachments/assets/c1bd671d-cf3c-4be4-aa85-52ab00fecb61)



The cron job is triggered via:

- A secure FastAPI route: `/run-poem-cron?key=YOUR_SECRET`
- GitHub Actions (daily schedule)
