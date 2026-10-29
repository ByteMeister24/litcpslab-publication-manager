# Publication review with Google Apps Script

This app gives everyone one browser link. A colleague selects their name, edits
their publication table, and saves a reviewed JSON file. You can download the
latest saved review for every author in one ZIP for the Markdown workflow.

Google hosts the app, and your Google Drive stores the files. You need a Google
account to deploy it. Colleagues do not need to install Python, this project, or
an application. The anonymous-access deployment described below does not require
them to sign in.

The source files are in `src/publication_review/google_apps_script/`:

| File | Purpose |
| --- | --- |
| [Code.gs](../src/publication_review/google_apps_script/Code.gs) | Read inputs, validate and save reviews, and export the ZIP |
| [Index.html](../src/publication_review/google_apps_script/Index.html) | Author selector and editable publication table |
| [appsscript.json](../src/publication_review/google_apps_script/appsscript.json) | Apps Script runtime, timezone, and Drive permission |

The page is designed for a trusted group: anyone with its link can select any
author and edit or download that author's publications. Selecting a name does
not verify identity. This is the name-only access model agreed for this app.

## 1. Prepare the files to upload

The app needs publication JSON and an `authors.json` index. The index maps a
database author name to the corresponding file. Publication records themselves
do not identify the owner of the list, and a slug such as `mainak-majumder`
does not preserve the database name's capitalization.

### Option A: use the optional preparation helper

`prepare_upload.py` gathers the normalized files into one new folder and
generates this index. It is a coordinator convenience, not part of the deployed
app. Colleagues never run it. It reads the database and existing normalized
JSON, validates records using the existing reader, and writes upload copies;
it does not modify your database or original publication files.

After installing the project with `python -m pip install -e .`, use the existing
project environment and the short `prepare_upload` command:

```bash
source .venv/bin/activate
prepare_upload --output /tmp/publication-review-upload
```

By default this includes all database authors with normalized files. Valid empty
lists are included, and missing files are reported as skipped. For a small pilot:

```bash
prepare_upload \
  --author "Mainak Majumder" \
  --output /tmp/publication-review-pilot
```

The output directory must be new. Choose another path for another preparation
run. The helper follows your configured normalized directory and filename
formats and accepts author names case-insensitively. Upload the contents of the
new folder, including `authors.json`, in step 2.

You can also run `python -m publication_review.prepare_upload` with the same
arguments. Relative output paths start at your current working directory;
absolute paths work from any directory.

### Option B: upload your existing JSON files directly

You can skip the Python helper. Gather the normalized JSON files you want to
share, and create an `authors.json` file with this structure:

```json
{
  "version": 1,
  "authors": [
    {
      "id": "mainak-majumder",
      "name": "Mainak Majumder",
      "sourceFile": "mainak-majumder-publications.json"
    },
    {
      "id": "rene-researcher",
      "name": "René Researcher",
      "sourceFile": "rene-researcher-publications.json"
    }
  ]
}
```

Replace the examples with your actual authors and filenames. `id` must be the
existing database author slug, exactly as used in your local data folders;
`name` is the canonical database name. `sourceFile` must match the uploaded
filename exactly. Every author ID and name must be unique. File and folder names
cannot contain path separators. Each source file contains the normal plain JSON
array of `Publication` records. No JSON-to-spreadsheet conversion is required.

## 2. Create two Google Drive folders

1. Open [Google Drive](https://drive.google.com/).
2. Create an input folder, for example **Publication review — inputs**.
3. Open it and upload **all the files from step 1**, including `authors.json`.
   Put the files directly in this folder, not in another nested folder. You can
   select and upload all of them together.
4. Create a second, empty folder, for example **Publication review — saved**.
5. Keep both folders private. The app will access them as you; colleagues only
   receive the app link.
6. Copy each folder's ID from its address. For example, in
   `https://drive.google.com/drive/folders/ABC123`, the ID is `ABC123`. Copy just
   the ID, without the rest of the URL or query parameters.

Use two different folders. Keep exactly one copy of every input filename;
Google Drive can contain files with duplicate names, which the app rejects.

## 3. Create the Apps Script project

1. Open [Google Apps Script](https://script.google.com/) and select **New project**.
2. Give the project a name such as **Publication review**.
3. Replace the default contents of **Code.gs** with the complete contents of
   the supplied `Code.gs` file.
4. Next to **Files**, select **+ → HTML**. Name the file **Index**; the editor
   adds `.html`. Replace its contents with the supplied `Index.html` file.
5. Open **Project Settings** using the gear icon.
6. Enable **Show "appsscript.json" manifest file in editor**.
7. Return to the editor, open **appsscript.json**, and replace its contents with
   the supplied manifest file.
8. Save the project.

No npm packages, external JavaScript libraries, advanced Google APIs, or Google
Cloud billing setup are needed. The manifest requests Drive access because the
app reads inputs and creates review files under your account. Google's consent
grants the script Drive read/write access; the supplied code uses the two
configured folders. Do not put Google
passwords, API keys, or OAuth tokens in the HTML.

## 4. Set the two folder IDs

1. Open **Project Settings**.
2. Under **Script Properties**, select **Add script property**.
3. Add these two properties:

   | Property | Value |
   | --- | --- |
   | `SOURCE_FOLDER_ID` | The ID of the input folder containing `authors.json` |
   | `REVIEW_FOLDER_ID` | The ID of the empty saved-review folder |

4. Save the properties. These values belong in Script Properties, not in
   `Index.html`. There are no hardcoded folder IDs to replace in the supplied code.

## 5. Authorize and check the setup

1. Return to the Apps Script editor.
2. Select **checkSetup** from the function dropdown near the Run button.
3. Select **Run**.
4. When Google asks for authorization, choose the account that owns the folders
   and review the requested Drive access. This step is for you as the deployer.
5. If Google shows an unverified-app notice for this project you just created,
   its **Advanced → Go to Publication review** option may be needed to authorize
   your own script. An organization's account policy can disallow this.
6. Check the execution log. Success looks like:

   ```text
   Ready: 12 author(s). Input and review folders are accessible.
   ```

Resolve any missing input, duplicate filename, or invalid JSON errors before
sharing the app. Record values must follow `Publication`: three arrays of strings
(`authors`, `affiliations`, `keywords`) and string values for every other field,
including `year`. Missing fields receive empty defaults; unknown fields fail.

## 6. Deploy the browser app

1. Select **Deploy → New deployment**.
2. Next to **Select type**, choose **Web app**.
3. Set **Execute as** to **Me**.
4. Set **Who has access** to **Anyone**, allowing access without a Google login.
   Do not choose the option limited to users with Google accounts.
5. Select **Deploy** and complete any owner authorization prompts.
6. Copy the **Web app URL** ending in **`/exec`**.

Share this same URL with every colleague. Do not share the script editor URL or
the `/dev` test URL. The latter is only accessible to project editors.

If **Anyone** is unavailable, your account or organization policy does not allow
this deployment mode. Use an account that permits anonymous web apps or ask its
administrator. The supplied app does not authenticate reviewers individually.

These deployment and execution options follow Google's
[web-app documentation](https://developers.google.com/apps-script/guides/web).

## 7. Try it before distributing the link

1. Open the `/exec` URL in a private/incognito browser window.
2. Check that it opens without requiring reviewer authorization.
3. Select a name and verify the publications and metadata.
4. Try unchecking **Include**, adding a publication, and editing **Details**.
5. Select **Save review** and check that the page says the review was saved.
6. Reload the page and select the same name. The saved list should reappear.
7. Check Drive: the original input JSON should be unchanged, while the saved
   folder contains an author subfolder with a new review JSON file.
8. Select **Refresh status**, then **Download all saved reviews (.zip)**.
   Confirm that the ZIP has the reviewed JSON and the expected directory layout.

Use a pilot upload first if you do not want trial edits in the real review round.
The local automated tests cover the app logic and browser interaction, but a
live Google deployment still needs this account-specific smoke test.

## 8. Instructions for colleagues

1. Open the shared link and select your name.
2. Check your publications. Uncheck **Include** for work that is not yours.
   You can re-check it before saving if you change your mind. Unchecked records
   are omitted from the saved JSON.
3. Correct the table fields directly. Use **Details** for the full record,
   including abstract, affiliations, keywords, identifiers, publisher, and link.
   Enter one author, affiliation, or keyword per line in array fields.
4. Select **Add publication** to add missing work, then **Apply changes**.
5. Select **Save review** when finished. This marks the review as saved even
   if you did not change any records.

Search only changes the displayed rows; saving includes all checked publications
in the complete list. Publication order and duplicates are retained. Edits are
not saved automatically. **Download current edits** creates a local JSON backup
but does not submit it. **Reload saved list** discards unsaved edits after asking.

Each save creates a readable filename in the author's saved-review folder:

```text
alois-zoitl-reviewed-2026-10-29T14-30-00.json
```

The timestamp uses the Apps Script project's timezone, configured as
`Europe/Vienna` in the supplied manifest. Saves within the same second receive
short suffixes such as `-2.json` and `-3.json`, preserving every revision.
The original-input fingerprint is stored in the Drive file's description
metadata, using the built-in [File API](https://developers.google.com/apps-script/reference/drive/file),
so publication JSON still contains only the `Publication` fields. Keep that
description intact: the app reads it to detect changed normalized inputs.

Existing `review-<fingerprint>-<UUID>.json` files remain supported and retain
their names. No migration is required. Future saves use readable names.

An empty saved review is valid, but the app asks for confirmation because the
Markdown workflow uses an empty review to remove its final Markdown output.
Cancelling the addition of a publication does not add a blank record.

If another browser saved the same author's list while it was open, a stale save
is rejected. Download your current edits as a backup, reload the saved list,
and reapply your changes. One person's stale browser does not overwrite another
person's completed review.

## 9. Collect the reviews and generate Markdown

1. Open the same app URL and select **Refresh status** to see the current
   completion count and **review saved** markers next to names.
2. Select **Download all saved reviews (.zip)**. It exports only the latest
   saved review for each author. Authors who have not saved are omitted;
   explicitly saved empty lists are included as `[]`.
3. Extract the ZIP into the project directory, merging its `data/` folder with
   the project's existing `data/` folder. It contains paths such as:

   ```text
   data/mainak-majumder/updated/mainak-majumder-reviewed-2026-10-29T14-30-00.json
   ```

   New reviews keep their readable saved filenames, including any same-second
   suffix. Older hash-named reviews receive readable export names based on their
   Drive creation time; their original Drive files are unchanged. Each exported
   document is a plain `Publication` array, without app-specific fields. Raw and
   normalized files are not present in the ZIP and are not overwritten.
4. If you configured a different data directory or updated-folder layout, copy
   the author `updated/` contents into those configured locations instead.
5. Run the existing workflow in your project environment:

   ```bash
   publication_markdown all
   ```

The Markdown workflow selects each author's latest JSON by filesystem creation
time. Import the newest export, and avoid re-extracting older exports over a
later review round: extracting a file can give it a new creation time. See the
[Markdown guide](publication-markdown.md) for its CLI and validation behavior.

## 10. Later changes and new review rounds

To update the app code while retaining its link, change the files in Apps Script,
then select **Deploy → Manage deployments → Edit → New version → Deploy**.
Saving code in the editor alone does not update an existing versioned deployment.

For a new set of normalized inputs, prepare a new upload folder and create new
input and saved-review folders in Drive. Update both Script Properties to the
new folder IDs. The app reads those properties on each request; changing them
does not require publishing a new code version. Keep the old folders as the
previous round's history, and have colleagues reload the page.

Do not replace normalized inputs mid-review. The app detects changed source
content or a changed source folder and refuses to combine an old review with
the new inputs. Each save creates a new file; previous reviews are retained.

When upgrading to readable filenames, replace `Code.gs` and publish a new
deployment version. The new code reads both filename styles. Incomplete saves
use temporary `.pending-review-` names until metadata is attached and the final
name is published. These temporary files are ignored by review selection and
export, and are moved to Drive trash if a save fails. A cleanup failure is
reported explicitly and does not replace the previous saved review.

## Troubleshooting and limits

| Message or symptom | What to check |
| --- | --- |
| Folder properties are missing | Set both Script Properties exactly as shown in step 4 |
| Missing `authors.json` | Upload the index directly into the configured input folder |
| Duplicate input filename or author | Keep one file per manifest filename and unique author IDs/names |
| Invalid publication field | Use strings for scalar fields and arrays of strings for the three list fields |
| The list changed since it was opened | Back up unsaved edits, reload, and apply them to the newer saved review |
| Normalized input changed | Start a new review round with new input and saved-review folders |
| Missing or invalid review metadata | The latest readable review's Drive description was removed or changed; restore that description from its original metadata before retrying |
| Colleagues cannot open the page | Check `/exec`, **Execute as: Me**, and anonymous **Anyone** access |
| Editing code has no effect | Publish a new version through Manage deployments |
| New saved reviews are not shown in the completion count | Select Refresh status |

This is a small-group review tool. It uses Google's standard Apps Script and
Drive limits, including a six-minute maximum per script execution. Large bulk
exports and heavy simultaneous use may reach those limits. Your Drive storage
also holds every saved revision. No paid services or external database are used.
Review Google's [current quotas](https://developers.google.com/apps-script/guides/services/quotas)
when sizing a larger review round.

## Developer verification

The preparation helper has Python tests; the server has tests using in-memory
Apps Script/Drive substitutes. The JavaScript tests use only Node.js built-ins:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_review_upload.py'
node tests/google_apps_script_review.test.cjs
```

Node.js is only needed to run those developer tests, not to deploy or use the app.
The browser uses Google's
[asynchronous script bridge](https://developers.google.com/apps-script/guides/html/communication),
and batch export uses the built-in
[ZIP utility](https://developers.google.com/apps-script/reference/utilities/utilities#zip(BlobSource,String)).
