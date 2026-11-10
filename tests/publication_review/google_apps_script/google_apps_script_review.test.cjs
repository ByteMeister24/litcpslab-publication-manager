// Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

/* Run with Node.js: node tests/publication_review/google_apps_script/google_apps_script_review.test.cjs. No npm packages needed. */
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const sourceCode = fs.readFileSync(path.join(__dirname, '../../../src/publication_review/google_apps_script/Code.gs'), 'utf8');
const plain = value => JSON.parse(JSON.stringify(value));

function iterator(items) {
  let index = 0;
  return {hasNext: () => index < items.length, next: () => items[index++]};
}

function fixture() {
  let sequence = 0;
  const folders = new Map();
  const state = {failCreate: false, failDescription: false, failRename: false, failTrash: false,
    locked: false, lockReleases: 0, dateFormats: []};
  class File {
    constructor(name, content) { this.name = name; this.content = content; this.number = ++sequence; this.created = new Date(1700000000000 + sequence); }
    getId() { return 'file-' + String(this.number).padStart(6, '0'); }
    getName() { return this.name; }
    getDateCreated() { return this.created; }
    getBlob() { return {getDataAsString: () => this.content}; }
    getDescription() { return this.description || ''; }
    setDescription(value) { if (state.failDescription) throw new Error('Metadata unavailable'); this.description = value; return this; }
    setName(value) { if (state.failRename) throw new Error('Rename unavailable'); this.name = value; return this; }
    setTrashed(value) { if (state.failTrash) throw new Error('Trash unavailable'); this.trashed = value; return this; }
  }
  class Folder {
    constructor(id) { this.id = id; this.files = []; this.children = []; folders.set(id, this); }
    getId() { return this.id; }
    getFilesByName(name) { return iterator(this.files.filter(file => !file.trashed && file.name === name)); }
    getFiles() { return iterator(this.files.filter(file => !file.trashed)); }
    getFoldersByName(name) { return iterator(this.children.filter(folder => folder.id === name)); }
    createFolder(name) { const folder = new Folder(name); this.children.push(folder); return folder; }
    createFile(name, content, mime) {
      if (state.failCreate) throw new Error('Storage unavailable');
      assert.equal(mime, 'application/json');
      const file = new File(name, content); this.files.push(file); return file;
    }
    seed(name, records) { const file = new File(name, typeof records === 'string' ? records : JSON.stringify(records)); this.files.push(file); return file; }
  }
  const source = new Folder('source-folder');
  const reviews = new Folder('review-folder');
  const manifest = source.seed('authors.json', {version: 1, authors: [
    {id: 'ada-researcher', name: 'Ada Researcher', sourceFile: 'ada.json'},
    {id: 'rené-researcher', name: 'René Researcher', sourceFile: 'rené.json'},
  ]});
  const original = source.seed('ada.json', [{title: 'Über systems', authors: ['Ada', 'René'], year: '2026'}, {title: 'Second'}]);
  source.seed('rené.json', []);
  const properties = new Map([['SOURCE_FOLDER_ID', 'source-folder'], ['REVIEW_FOLDER_ID', 'review-folder']]);
  const context = vm.createContext({
    console: {log() {}},
    PropertiesService: {getScriptProperties: () => ({getProperty: key => properties.get(key)})},
    Session: {getScriptTimeZone: () => 'Europe/Vienna'},
    DriveApp: {getFolderById: id => { if (!folders.has(id)) throw new Error('Unknown folder'); return folders.get(id); }},
    LockService: {getScriptLock: () => ({
      waitLock() { assert.equal(state.locked, false); state.locked = true; },
      releaseLock() { state.locked = false; state.lockReleases += 1; },
    })},
    HtmlService: {createHtmlOutputFromFile: name => ({setTitle() { assert.equal(name, 'Index'); return this; }, addMetaTag() { return this; }})},
    Utilities: {
      DigestAlgorithm: {SHA_256: 'sha256'}, Charset: {UTF_8: 'utf8'},
      computeDigest: (algorithm, text) => Array.from(crypto.createHash(algorithm).update(text, 'utf8').digest()),
      getUuid: () => crypto.randomUUID(),
      formatDate: (date, zone, format) => { state.dateFormats.push({zone, format}); return '2026-10-29T14-30-00'; },
      newBlob: (text, mime, name) => ({text, mime, name}),
      zip: (blobs, name) => ({getBytes: () => Buffer.from(JSON.stringify({blobs: plain(blobs), name}))}),
      base64Encode: bytes => Buffer.from(bytes).toString('base64'),
    },
  });
  vm.runInContext(sourceCode, context, {filename: 'Code.gs'});
  return {app: context, source, reviews, original, manifest, properties, state, folders};
}

function runTests() {
  const results = [];
  const test = (name, action) => { action(); results.push(name); };

  test('setup and catalog preserve canonical Unicode names without exposing file IDs', () => {
    const f = fixture();
    assert.match(f.app.checkSetup(), /Ready: 2/);
    assert.deepEqual(plain(f.app.getCatalog().authors).map(author => [author.id, author.name, author.reviewed]),
      [['ada-researcher', 'Ada Researcher', false], ['rené-researcher', 'René Researcher', false]]);
    assert.equal(JSON.stringify(f.app.getCatalog()).includes('source-folder'), false);
    f.app.doGet();
  });

  test('load fills defaults and keeps arrays, strings, Unicode, order, and original bytes', () => {
    const f = fixture(); const before = f.original.content;
    const loaded = f.app.loadAuthor('ada-researcher');
    assert.equal(loaded.publications.length, 2);
    assert.deepEqual(plain(loaded.publications[0].authors), ['Ada', 'René']);
    assert.equal(loaded.publications[0].title, 'Über systems');
    assert.equal(loaded.publications[1].abstract, '');
    assert.equal(Object.keys(loaded.publications[0]).length, 12);
    assert.equal(f.original.content, before);
    assert.equal(f.reviews.children.length, 0);
  });

  test('save added and removed records, duplicates, and ordering as a plain JSON array', () => {
    const f = fixture(); const before = f.original.content;
    const loaded = f.app.loadAuthor('ada-researcher');
    const saved = f.app.saveReview('ada-researcher', [{title: 'Added'}, loaded.publications[0], {title: 'Added'}], loaded.revision);
    const file = f.reviews.children[0].files[0];
    assert.deepEqual(JSON.parse(file.content).map(record => record.title), ['Added', 'Über systems', 'Added']);
    assert.equal(Object.keys(JSON.parse(file.content)[0]).length, 12);
    assert.equal(saved.reviewed, true);
    assert.equal(f.original.content, before);
    assert.deepEqual(plain(f.app.loadAuthor('ada-researcher').publications), plain(saved.publications));
    assert.equal(f.app.getCatalog().authors[0].reviewed, true);
  });

  test('new names are readable, use the script timezone, and keep fingerprints in Drive metadata', () => {
    const f = fixture(); const loaded = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', loaded.publications, loaded.revision);
    const file = f.reviews.children[0].files[0];
    assert.equal(file.name, 'ada-researcher-reviewed-2026-10-29T14-30-00.json');
    const metadata = JSON.parse(file.description);
    assert.equal(metadata.application, 'publication-review');
    assert.equal(metadata.version, 1);
    assert.equal(metadata.sourceHash, loaded.revision.split(':')[0]);
    assert.equal(file.name.includes(metadata.sourceHash), false);
    assert.equal(JSON.stringify(JSON.parse(file.content)).includes('sourceHash'), false);
    assert.deepEqual(f.state.dateFormats[0], {zone: 'Europe/Vienna', format: "yyyy-MM-dd'T'HH-mm-ss"});
  });

  test('same-second saves get short collision suffixes and preserve each revision', () => {
    const f = fixture();
    for (const title of ['First', 'Second', 'Third']) {
      const loaded = f.app.loadAuthor('ada-researcher');
      f.app.saveReview('ada-researcher', [{title}], loaded.revision);
    }
    const files = f.reviews.children[0].files;
    assert.deepEqual(files.map(file => file.name), [
      'ada-researcher-reviewed-2026-10-29T14-30-00.json',
      'ada-researcher-reviewed-2026-10-29T14-30-00-2.json',
      'ada-researcher-reviewed-2026-10-29T14-30-00-3.json',
    ]);
    assert.deepEqual(files.map(file => JSON.parse(file.content)[0].title), ['First', 'Second', 'Third']);
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Third');
  });

  test('existing hash-named reviews load and export cleanly before the next readable save', () => {
    const f = fixture(); const source = f.app.loadAuthor('ada-researcher');
    const hash = source.revision.split(':')[0];
    const folder = f.reviews.createFolder('ada-researcher');
    const legacy = folder.seed('review-' + hash + '-0b69f50f-43dc-4d25-a85e-031019a410d3.json', [{title: 'Existing review'}]);
    const originalName = legacy.name;
    const loaded = f.app.loadAuthor('ada-researcher');
    assert.equal(loaded.publications[0].title, 'Existing review');
    assert.equal(f.app.getCatalog().authors[0].reviewed, true);
    const zipped = JSON.parse(Buffer.from(f.app.exportReviews().base64, 'base64').toString());
    assert.equal(zipped.blobs[0].name, 'ada-researcher-reviewed-2026-10-29T14-30-00.json');
    assert.equal(JSON.parse(zipped.blobs[0].text)[0].title, 'Existing review');
    f.app.saveReview('ada-researcher', [{title: 'Readable successor'}], loaded.revision);
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Readable successor');
    assert.equal(legacy.name, originalName);
    assert.equal(legacy.getDescription(), '');
    assert.equal(folder.files.length, 2);
  });

  test('newer legacy history still wins over readable names by Drive creation time', () => {
    const f = fixture(); const initial = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Readable'}], initial.revision);
    const hash = initial.revision.split(':')[0];
    f.reviews.children[0].seed('review-' + hash + '-aaaaaaaa-bbbb.json', [{title: 'Newer legacy'}]);
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Newer legacy');
  });

  test('metadata or rename failure never publishes an incomplete review and releases the lock', () => {
    for (const failure of ['failDescription', 'failRename']) {
      const f = fixture(); const original = f.app.loadAuthor('ada-researcher');
      f.app.saveReview('ada-researcher', [{title: 'Previous'}], original.revision);
      const loaded = f.app.loadAuthor('ada-researcher');
      f.state[failure] = true;
      assert.throws(() => f.app.saveReview('ada-researcher', [{title: 'Failed'}], loaded.revision), /unavailable/);
      assert.equal(f.state.locked, false);
      assert.equal(f.reviews.children[0].files.filter(file => !file.trashed).length, 1);
      assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Previous');
    }
  });

  test('pending files remain ignored if cleanup also fails', () => {
    const f = fixture(); const initial = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Previous'}], initial.revision);
    const loaded = f.app.loadAuthor('ada-researcher');
    f.state.failDescription = true; f.state.failTrash = true;
    assert.throws(() => f.app.saveReview('ada-researcher', [], loaded.revision), /incomplete .pending-review file/);
    assert.equal(f.reviews.children[0].files.length, 2);
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Previous');
    const zipped = JSON.parse(Buffer.from(f.app.exportReviews().base64, 'base64').toString());
    assert.equal(zipped.blobs.length, 1);
    assert.equal(JSON.parse(zipped.blobs[0].text)[0].title, 'Previous');
  });

  test('invalid latest metadata fails without fallback and does not block the author catalog', () => {
    const f = fixture(); const original = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Old'}], original.revision);
    const loaded = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Latest'}], loaded.revision);
    const file = f.reviews.children[0].files[1];
    const before = file.content;
    for (const description of ['', '{', 'null', '{}', '{"application":"other","version":1,"sourceHash":"bad"}']) {
      file.description = description;
      assert.throws(() => f.app.loadAuthor('ada-researcher'), /invalid review metadata/);
      assert.throws(() => f.app.exportReviews(), /invalid review metadata/);
      assert.equal(f.app.getCatalog().authors.length, 2);
      assert.equal(file.content, before);
    }
  });

  test('invalid metadata on older history does not affect a valid latest review', () => {
    const f = fixture(); const original = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Old'}], original.revision);
    const loaded = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Latest'}], loaded.revision);
    f.reviews.children[0].files[0].description = '';
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Latest');
  });

  test('empty reviews are saved, restored, and exported; unreviewed authors are omitted', () => {
    const f = fixture(); const loaded = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [], loaded.revision);
    assert.deepEqual(plain(f.app.loadAuthor('ada-researcher').publications), []);
    const archive = f.app.exportReviews();
    const zipped = JSON.parse(Buffer.from(archive.base64, 'base64').toString());
    assert.equal(archive.authorCount, 1);
    assert.match(zipped.blobs[0].name, /^ada-researcher-reviewed-.+\.json$/);
    assert.equal(zipped.blobs[0].mime, 'application/json');
    assert.equal(zipped.blobs[0].text, '[]\n');
  });

  test('ZIP includes only the latest review per author at its root with Unicode filenames', () => {
    const f = fixture(); const first = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Old'}], first.revision);
    const next = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Newest'}], next.revision);
    const second = f.app.loadAuthor('rené-researcher');
    f.app.saveReview('rené-researcher', [{title: 'René work'}], second.revision);
    const zipped = JSON.parse(Buffer.from(f.app.exportReviews().base64, 'base64').toString());
    assert.equal(zipped.blobs.length, 2);
    assert.equal(JSON.parse(zipped.blobs[0].text)[0].title, 'Newest');
    assert.deepEqual(zipped.blobs.map(blob => blob.name), [
      'ada-researcher-reviewed-2026-10-29T14-30-00-2.json',
      'rené-researcher-reviewed-2026-10-29T14-30-00.json',
    ]);
    assert.equal(f.reviews.children[0].files.length, 2);
  });

  test('stale concurrent save is rejected without overwriting another review', () => {
    const f = fixture(); const browserA = f.app.loadAuthor('ada-researcher'); const browserB = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Saved by A'}], browserA.revision);
    assert.throws(() => f.app.saveReview('ada-researcher', [{title: 'Stale B'}], browserB.revision), /changed since/);
    assert.equal(f.reviews.children[0].files.length, 1);
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Saved by A');
    assert.equal(f.state.locked, false);
  });

  test('every invalid document, field type, unknown key, and array member rejects the entire save', () => {
    const f = fixture(); const loaded = f.app.loadAuthor('ada-researcher');
    const invalid = [null, {}, 'text', [null], [[]], [{extra: 'value'}], [{year: 2026}], [{title: null}], [{authors: 'Ada'}],
      [{authors: ['Ada', 1]}], [{keywords: [false]}], [{affiliations: {}}], [{title: 'Valid'}, {year: true}]];
    invalid.forEach(records => assert.throws(() => f.app.saveReview('ada-researcher', records, loaded.revision)));
    assert.equal(f.reviews.children.length, 0);
  });

  test('changed source rejects an open session before saving', () => {
    const f = fixture(); const loaded = f.app.loadAuthor('ada-researcher');
    f.original.content = '[{"title":"New normalized input"}]';
    assert.throws(() => f.app.saveReview('ada-researcher', [], loaded.revision), /changed since/);
    assert.equal(f.reviews.children.length, 0);
  });

  test('switching review rounds invalidates previously open sessions even for identical input', () => {
    const f = fixture(); const loaded = f.app.loadAuthor('ada-researcher');
    f.source.id = 'new-round-source'; f.folders.set(f.source.id, f.source);
    f.properties.set('SOURCE_FOLDER_ID', f.source.id);
    assert.throws(() => f.app.saveReview('ada-researcher', [], loaded.revision), /changed since/);
    assert.equal(f.reviews.children.length, 0);
  });

  test('changed source after a review requires a new round and preserves saved history', () => {
    const f = fixture(); const loaded = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [], loaded.revision);
    const before = f.reviews.children[0].files[0].content;
    f.original.content = '[{"title":"New normalized input"}]';
    assert.throws(() => f.app.loadAuthor('ada-researcher'), /new review round/);
    assert.throws(() => f.app.exportReviews(), /new review round/);
    assert.equal(f.reviews.children[0].files[0].content, before);
  });

  test('failed storage preserves the previous review and releases the lock', () => {
    const f = fixture(); const initial = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Previous'}], initial.revision);
    const loaded = f.app.loadAuthor('ada-researcher'); f.state.failCreate = true;
    assert.throws(() => f.app.saveReview('ada-researcher', [], loaded.revision), /Storage unavailable/);
    assert.equal(f.state.locked, false);
    assert.equal(f.reviews.children[0].files.length, 1);
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'Previous');
  });

  test('malformed latest saved review never falls back to older history', () => {
    const f = fixture(); const initial = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Older valid'}], initial.revision);
    const loaded = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Latest'}], loaded.revision);
    f.reviews.children[0].files[1].content = '[invalid';
    assert.throws(() => f.app.loadAuthor('ada-researcher'));
    assert.throws(() => f.app.exportReviews());
    assert.equal(f.state.locked, false);
  });

  test('latest selection uses Drive creation time', () => {
    const f = fixture(); const initial = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'First'}], initial.revision);
    const loaded = f.app.loadAuthor('ada-researcher');
    f.app.saveReview('ada-researcher', [{title: 'Second'}], loaded.revision);
    const files = f.reviews.children[0].files;
    files[0].created = new Date(1900000000000);
    assert.equal(f.app.loadAuthor('ada-researcher').publications[0].title, 'First');
  });

  test('unknown authors and manifest traversal cannot access arbitrary files', () => {
    const f = fixture();
    assert.throws(() => f.app.loadAuthor('../other-folder'), /Unknown author/);
    const manifest = JSON.parse(f.manifest.content); manifest.authors[0].id = '../outside'; f.manifest.content = JSON.stringify(manifest);
    assert.throws(() => f.app.getCatalog(), /Invalid author/);
  });

  test('duplicate input filenames and duplicate author IDs are explicit errors', () => {
    const f = fixture(); f.source.seed('ada.json', []);
    assert.throws(() => f.app.loadAuthor('ada-researcher'), /Duplicate input filename/);
    const manifest = JSON.parse(f.manifest.content); manifest.authors[1].id = manifest.authors[0].id;
    f.manifest.content = JSON.stringify(manifest);
    assert.throws(() => f.app.getCatalog(), /Duplicate author/);
  });

  test('missing setup, identical folders, missing files, and no saved reviews are explicit errors', () => {
    const f = fixture();
    assert.throws(() => f.app.exportReviews(), /No reviews/);
    f.properties.delete('SOURCE_FOLDER_ID'); assert.throws(() => f.app.getCatalog(), /must set/);
    f.properties.set('SOURCE_FOLDER_ID', 'review-folder'); assert.throws(() => f.app.getCatalog(), /must be different/);
    f.properties.set('SOURCE_FOLDER_ID', 'source-folder'); f.source.files.splice(f.source.files.indexOf(f.original), 1);
    assert.throws(() => f.app.loadAuthor('ada-researcher'), /Missing input file/);
  });

  return {passed: results.length, tests: results};
}

module.exports = {runTests, fixture};
if (require.main === module) console.log(JSON.stringify(runTests(), null, 2));
