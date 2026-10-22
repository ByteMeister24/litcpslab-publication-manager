"use strict";

const reportFile = document.getElementById("report-file");
const reportStatus = document.getElementById("report-status");

document.getElementById("update-report").addEventListener("click", () => reportFile.click());
reportFile.addEventListener("change", async () => {
  const file = reportFile.files[0];
  if (!file) return;
  try {
    const data = JSON.parse(await file.text());
    updateTables(data);
    reportStatus.textContent = `Updated from ${file.name}.`;
  } catch (error) {
    reportStatus.textContent = `Report update failed: ${error.message}`;
  } finally {
    reportFile.value = "";
  }
});

function updateTables(data) {
  const isObject = value => value !== null && typeof value === "object" && !Array.isArray(value);
  if (!isObject(data)) throw new Error("Report JSON must be an object.");
  if (typeof data.updated_at !== "string" || !/(Z|[+-]\d{2}:\d{2})$/.test(data.updated_at)) {
    throw new Error("Report updated_at must be an ISO datetime with a timezone.");
  }
  const updatedAt = new Date(data.updated_at);
  if (Number.isNaN(updatedAt.getTime())) throw new Error("Invalid report timestamp.");

  const tables = [...document.querySelectorAll("table")];
  const rows = tables.flatMap(table => [...table.querySelectorAll("tbody tr")]);
  const authors = Object.keys(data).filter(author => author !== "updated_at");
  const memberNames = new Set(rows.map(row => row.dataset.author));
  if (authors.length !== memberNames.size || authors.some(author => !memberNames.has(author))) {
    throw new Error("Report JSON authors must match the HTML member tables.");
  }
  const sources = new Set();
  for (const author of authors) {
    if (!isObject(data[author])) throw new Error(`Invalid counts for ${author}.`);
    for (const [source, count] of Object.entries(data[author])) {
      if (!source.trim() || !Number.isSafeInteger(count) || count < 0) {
        throw new Error(`Invalid publication count for ${author} [${source}].`);
      }
      sources.add(source);
    }
  }

  // Validate the whole file before replacing any displayed values.
  for (const table of tables) {
    const header = table.querySelector("thead tr");
    const columns = [...header.querySelectorAll("th[data-source]")].map(cell => cell.dataset.source);
    for (const source of sources) {
      if (!columns.includes(source)) {
        const heading = document.createElement("th");
        heading.scope = "col";
        heading.dataset.source = source;
        heading.textContent = source.toUpperCase();
        header.append(heading);
        columns.push(source);
      }
    }
    for (const row of table.querySelectorAll("tbody tr")) {
      for (const source of columns) {
        let cell = [...row.querySelectorAll("td")].find(cell => cell.dataset.source === source);
        if (!cell) {
          cell = document.createElement("td");
          cell.dataset.source = source;
          row.append(cell);
        }
        const counts = data[row.dataset.author];
        cell.textContent = Object.hasOwn(counts, source) ? counts[source] : "";
        cell.removeAttribute("class");
      }
    }
  }
  const timestamp = document.getElementById("last-updated");
  timestamp.dateTime = data.updated_at;
  timestamp.textContent = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Vienna", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23", timeZoneName: "short",
  }).format(updatedAt);
}
