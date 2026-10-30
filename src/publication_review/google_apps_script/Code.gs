/* Configure SOURCE_FOLDER_ID and REVIEW_FOLDER_ID in Script Properties. */

const PUBLICATION_FIELDS = [
  { name: "title", label: "Title" },
  { name: "authors", label: "Authors", array: true },
  { name: "affiliations", label: "Author affiliations", array: true },
  { name: "keywords", label: "Keywords", array: true },
  { name: "abstract", label: "Abstract" },
  { name: "publication_title", label: "Publication" },
  { name: "year", label: "Year" },
  { name: "issn", label: "ISSN" },
  { name: "isbn", label: "ISBN" },
  { name: "doi", label: "DOI" },
  { name: "pdf_url", label: "Link" },
  { name: "publisher", label: "Publisher" },
];

function doGet() {
  return HtmlService.createHtmlOutputFromFile("Index")
    .setTitle("Publication review")
    .addMetaTag("viewport", "width=device-width, initial-scale=1");
}

function getCatalog() {
  const settings = settings_();
  const authors = manifest_(settings.source).map((author) => {
    const file = latestReviewFile_(
      reviewFolder_(settings.reviews, author.id, false),
      author.id,
    );
    return {
      id: author.id,
      name: author.name,
      reviewed: file !== null,
      savedAt: file ? file.getDateCreated().toISOString() : null,
    };
  });
  return { authors: authors, fields: PUBLICATION_FIELDS };
}

function loadAuthor(authorId) {
  return withLock_(() => {
    const settings = settings_();
    const author = findAuthor_(settings.source, authorId);
    const source = readSource_(settings.source, author);
    const latest = latestReview_(
      reviewFolder_(settings.reviews, author.id, false),
      author.id,
    );
    assertSourceMatches_(source, latest);
    return {
      id: author.id,
      name: author.name,
      publications: latest
        ? readPublications_(latest.file)
        : source.publications,
      revision: revision_(source.hash, latest),
      reviewed: latest !== null,
      savedAt: latest ? latest.file.getDateCreated().toISOString() : null,
    };
  });
}

function saveReview(authorId, publications, expectedRevision) {
  const validated = validatePublications_(publications);
  return withLock_(() => {
    const settings = settings_();
    const author = findAuthor_(settings.source, authorId);
    const source = readSource_(settings.source, author);
    let folder = reviewFolder_(settings.reviews, author.id, false);
    const latest = latestReview_(folder, author.id);
    assertSourceMatches_(source, latest);
    if (expectedRevision !== revision_(source.hash, latest)) {
      throw new Error(
        "This list changed since you opened it. Your edits have not been saved. " +
          "Download your current edits as a backup, then reload the saved review and apply your changes.",
      );
    }
    if (!folder) folder = reviewFolder_(settings.reviews, author.id, true);
    const name = nextReviewFilename_(folder, author.id);
    // Publish the readable name only after metadata is attached. Incomplete saves stay out of selection.
    const file = folder.createFile(
      ".pending-review-" + Utilities.getUuid() + ".json",
      JSON.stringify(validated, null, 2) + "\n",
      "application/json",
    );
    try {
      file.setDescription(
        JSON.stringify({
          application: "publication-review",
          version: 1,
          sourceHash: source.hash,
        }),
      );
      file.setName(name);
    } catch (error) {
      try {
        file.setTrashed(true);
      } catch (cleanupError) {
        throw new Error(
          "Review could not be published: " +
            error.message +
            ". An incomplete .pending-review file remains in Drive and is ignored by the app.",
        );
      }
      throw error;
    }
    const saved = { file: file, sourceHash: source.hash };
    return {
      id: author.id,
      name: author.name,
      publications: validated,
      revision: revision_(source.hash, saved),
      reviewed: true,
      savedAt: file.getDateCreated().toISOString(),
    };
  });
}

function exportReviews() {
  return withLock_(() => {
    const settings = settings_();
    const authors = manifest_(settings.source);
    const stamp = Utilities.formatDate(
      new Date(),
      "UTC",
      "yyyy-MM-dd'T'HH-mm-ss",
    );
    const blobs = [];
    authors.forEach((author) => {
      const latest = latestReview_(
        reviewFolder_(settings.reviews, author.id, false),
        author.id,
      );
      if (!latest) return;
      const source = readSource_(settings.source, author);
      assertSourceMatches_(source, latest);
      const publications = readPublications_(latest.file);
      const name = readableReviewName_(latest.file.getName(), author.id)
        ? latest.file.getName()
        : reviewFilename_(author.id, latest.file.getDateCreated());
      blobs.push(
        Utilities.newBlob(
          JSON.stringify(publications, null, 2) + "\n",
          "application/json",
          name,
        ),
      );
    });
    if (!blobs.length) throw new Error("No reviews have been saved yet.");
    const filename = "publication-reviews-" + stamp + ".zip";
    const archive = Utilities.zip(blobs, filename);
    return {
      filename: filename,
      base64: Utilities.base64Encode(archive.getBytes()),
      authorCount: blobs.length,
    };
  });
}

// Run this once in the Apps Script editor to authorize access and verify the upload.
function checkSetup() {
  const settings = settings_();
  const authors = manifest_(settings.source);
  authors.forEach((author) => readSource_(settings.source, author));
  const message =
    "Ready: " +
    authors.length +
    " author(s). Input and review folders are accessible.";
  console.log(message);
  return message;
}

function settings_() {
  const properties = PropertiesService.getScriptProperties();
  const sourceId = properties.getProperty("SOURCE_FOLDER_ID");
  const reviewId = properties.getProperty("REVIEW_FOLDER_ID");
  if (!sourceId || !reviewId)
    throw new Error(
      "The coordinator must set SOURCE_FOLDER_ID and REVIEW_FOLDER_ID in Script Properties.",
    );
  if (sourceId === reviewId)
    throw new Error("Input and review folders must be different.");
  return {
    source: DriveApp.getFolderById(sourceId),
    reviews: DriveApp.getFolderById(reviewId),
  };
}

function oneFile_(folder, name) {
  const files = folder.getFilesByName(name);
  if (!files.hasNext()) throw new Error("Missing input file: " + name);
  const file = files.next();
  if (files.hasNext())
    throw new Error(
      "Duplicate input filename: " + name + ". Keep exactly one copy.",
    );
  return file;
}

function readJson_(file) {
  try {
    return JSON.parse(
      file
        .getBlob()
        .getDataAsString("UTF-8")
        .replace(/^\uFEFF/, ""),
    );
  } catch (error) {
    throw new Error(file.getName() + ": " + error.message);
  }
}

function safeSegment_(value) {
  return (
    typeof value === "string" &&
    value.trim() !== "" &&
    value !== "." &&
    value !== ".." &&
    !/[\/\\\x00-\x1f\x7f]/.test(value)
  );
}

function manifest_(folder) {
  const document = readJson_(oneFile_(folder, "authors.json"));
  if (
    !document ||
    document.version !== 1 ||
    !Array.isArray(document.authors) ||
    !document.authors.length
  ) {
    throw new Error(
      "authors.json must contain a version 1 author manifest. Run the preparation command again.",
    );
  }
  const ids = new Set();
  const names = new Set();
  document.authors.forEach((author) => {
    if (
      !author ||
      !safeSegment_(author.id) ||
      typeof author.name !== "string" ||
      !author.name.trim() ||
      !safeSegment_(author.sourceFile) ||
      !author.sourceFile.toLowerCase().endsWith(".json") ||
      author.sourceFile === "authors.json"
    )
      throw new Error("Invalid author entry in authors.json.");
    if (ids.has(author.id) || names.has(author.name.toLowerCase()))
      throw new Error("Duplicate author in authors.json: " + author.name);
    ids.add(author.id);
    names.add(author.name.toLowerCase());
  });
  return document.authors;
}

function findAuthor_(folder, authorId) {
  const author = manifest_(folder).find((item) => item.id === authorId);
  if (!author)
    throw new Error(
      "Unknown author. Reload the page and select a name from the list.",
    );
  return author;
}

function validatePublications_(records) {
  if (!Array.isArray(records))
    throw new Error("Publication JSON must be an array.");
  const allowed = new Set(PUBLICATION_FIELDS.map((field) => field.name));
  return records.map((record, index) => {
    if (!record || typeof record !== "object" || Array.isArray(record))
      throw new Error("Publication " + (index + 1) + " must be an object.");
    Object.keys(record).forEach((key) => {
      if (!allowed.has(key))
        throw new Error(
          "Publication " + (index + 1) + " has an unknown field: " + key,
        );
    });
    const result = {};
    PUBLICATION_FIELDS.forEach((field) => {
      const present = Object.prototype.hasOwnProperty.call(record, field.name);
      const value = present ? record[field.name] : field.array ? [] : "";
      const valid = field.array
        ? Array.isArray(value) &&
          value.every((item) => typeof item === "string")
        : typeof value === "string";
      if (!valid)
        throw new Error(
          "Publication " +
            (index + 1) +
            ": " +
            field.label +
            " must be " +
            (field.array ? "an array of strings." : "a string."),
        );
      result[field.name] = field.array ? value.slice() : value;
    });
    return result;
  });
}

function readPublications_(file) {
  try {
    return validatePublications_(readJson_(file));
  } catch (error) {
    throw new Error(file.getName() + ": " + error.message);
  }
}

function readSource_(folder, author) {
  const file = oneFile_(folder, author.sourceFile);
  const text = file
    .getBlob()
    .getDataAsString("UTF-8")
    .replace(/^\uFEFF/, "");
  let publications;
  try {
    publications = validatePublications_(JSON.parse(text));
  } catch (error) {
    throw new Error(author.sourceFile + ": " + error.message);
  }
  const bytes = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256,
    JSON.stringify([folder.getId(), author.id, author.name, text]),
    Utilities.Charset.UTF_8,
  );
  const hash = bytes
    .map((value) => (value & 255).toString(16).padStart(2, "0"))
    .join("");
  return { hash: hash, publications: publications };
}

function reviewFolder_(root, authorId, create) {
  const folders = root.getFoldersByName(authorId);
  if (folders.hasNext()) {
    const folder = folders.next();
    if (folders.hasNext())
      throw new Error("Duplicate review folder for " + authorId + ".");
    return folder;
  }
  return create ? root.createFolder(authorId) : null;
}

function reviewFilename_(authorId, date) {
  const stamp = Utilities.formatDate(
    date,
    Session.getScriptTimeZone(),
    "yyyy-MM-dd'T'HH-mm-ss",
  );
  return authorId + "-reviewed-" + stamp + ".json";
}

function nextReviewFilename_(folder, authorId) {
  const base = reviewFilename_(authorId, new Date());
  let name = base;
  let sequence = 1;
  while (folder.getFilesByName(name).hasNext()) {
    sequence += 1;
    name = base.slice(0, -5) + "-" + sequence + ".json";
  }
  return name;
}

function readableReviewName_(name, authorId) {
  const prefix = authorId + "-reviewed-";
  return (
    name.startsWith(prefix) &&
    /^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}(?:-\d+)?\.json$/.test(
      name.slice(prefix.length),
    )
  );
}

function latestReviewFile_(folder, authorId) {
  if (!folder) return null;
  const files = folder.getFiles();
  let latest = null;
  while (files.hasNext()) {
    const file = files.next();
    const legacy = /^review-([0-9a-f]{64})-[0-9a-f-]+\.json$/.test(
      file.getName(),
    );
    if (!legacy && !readableReviewName_(file.getName(), authorId)) continue;
    if (
      !latest ||
      file.getDateCreated().getTime() > latest.getDateCreated().getTime() ||
      (file.getDateCreated().getTime() === latest.getDateCreated().getTime() &&
        file.getId() > latest.getId())
    ) {
      latest = file;
    }
  }
  return latest;
}

function latestReview_(folder, authorId) {
  const file = latestReviewFile_(folder, authorId);
  if (!file) return null;
  // Existing reviews keep their original names and remain readable without a migration.
  const legacy = /^review-([0-9a-f]{64})-[0-9a-f-]+\.json$/.exec(
    file.getName(),
  );
  if (legacy) return { file: file, sourceHash: legacy[1] };
  let metadata;
  try {
    metadata = JSON.parse(file.getDescription());
  } catch (error) {
    throw new Error(
      "Missing or invalid review metadata for " + file.getName() + ".",
    );
  }
  if (
    !metadata ||
    metadata.application !== "publication-review" ||
    metadata.version !== 1 ||
    typeof metadata.sourceHash !== "string" ||
    !/^[0-9a-f]{64}$/.test(metadata.sourceHash)
  ) {
    throw new Error(
      "Missing or invalid review metadata for " + file.getName() + ".",
    );
  }
  return { file: file, sourceHash: metadata.sourceHash };
}

function assertSourceMatches_(source, latest) {
  if (latest && latest.sourceHash !== source.hash)
    throw new Error(
      "The normalized input changed after a review was saved. " +
        "Ask the coordinator to start a new review round with new input and review folders. Existing reviews have been preserved.",
    );
}

function revision_(sourceHash, latest) {
  return sourceHash + ":" + (latest ? latest.file.getId() : "unreviewed");
}

function withLock_(action) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    return action();
  } finally {
    lock.releaseLock();
  }
}
