# Davinci Physiotherapy — Vercel + TiDB deployment fix

## What was corrected in this package

- `config.py` now validates `DATABASE_URL` and `SECRET_KEY` with clearer errors.
- It forces the `mysql+pymysql` driver and adds TiDB Cloud Starter TLS verification options.
- It uses a small SQLAlchemy connection pool suitable for serverless functions.
- It writes admin-uploaded files to `/tmp` on Vercel because the deployment filesystem is not persistent/writable.
- `app.py` now exposes `/healthz` to test the database connection without loading the homepage.

## 1. Replace the project files

Extract this ZIP and replace your existing project folder contents with these updated files.
Keep a backup of the old folder first. Do not upload `.env` or database passwords to GitHub.

## 2. Set Vercel environment variables

Vercel Dashboard → `davinciphysiotherapy` → Settings → Environment Variables.

Add these two variables for **Production** (also add Preview if you use preview deployments):

- `DATABASE_URL`
- `SECRET_KEY`

`DATABASE_URL` format (replace every placeholder with the values shown in TiDB Connect):

    mysql+pymysql://USERNAME:URL_ENCODED_PASSWORD@HOST:4000/davinci_physiotherapy?ssl_verify_cert=true&ssl_verify_identity=true

Important:
- Use database `davinci_physiotherapy`, not `sys`.
- URL-encode reserved password characters. For example `@` becomes `%40`, `#` becomes `%23`, `/` becomes `%2F`, and `%` becomes `%25`.
- Do not include angle brackets or quotes around the value.
- Rotate any TiDB password that was previously pasted into a chat or exposed, then use the new password here.
- `SECRET_KEY` should be a long random string, not `change-this-secret`.

Generate a secret key in Windows CMD:

    python -c "import secrets; print(secrets.token_hex(32))"

Copy the output into Vercel as `SECRET_KEY`.

## 3. Check TiDB schema

In TiDB Cloud SQL Editor, select the `davinci_physiotherapy` database and execute the contents of `database/schema.sql` if the tables have not already been created.

The schema creates these tables: `admins`, `services`, `appointments`, `contact_messages`, `testimonials`, and `settings`.

Do not re-run seed INSERT statements on a populated database unless you intend to add duplicate sample rows.

## 4. Redeploy

After saving environment variables:
- Vercel → Deployments
- Open the latest deployment → Redeploy
- Wait for Ready status

## 5. Test database

Open:

    https://davinciphysiotherapy.vercel.app/healthz

Expected response:

    {"status":"ok","database":"connected"}

If it returns HTTP 503, open Vercel → Logs, filter by `/healthz`, and inspect the Python traceback. If it returns an environment-variable error, recheck Step 2.

## Important notes

- A successful build does not prove that the database is reachable at runtime.
- Vercel `/tmp` storage is temporary and can disappear between function instances. Uploaded admin images are therefore not permanent in this configuration. Use persistent object storage (for example, a compatible object-storage service) before relying on image uploads in production.
- This code package cannot set Vercel environment variables or create/import the TiDB database for you; those are dashboard/database actions.
