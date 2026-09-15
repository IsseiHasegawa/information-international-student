const form = document.querySelector("#scrape-form");
const urlInput = document.querySelector("#url");
const message = document.querySelector("#message");
const results = document.querySelector("#results");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  message.textContent = "Getting information...";
  results.hidden = true;

  try {
    const response = await fetch("/api/scrape", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlInput.value }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error);
    }

    showResults(data);
    message.textContent = "Done.";
  } catch (error) {
    message.textContent = error.message;
  }
});

function showResults(data) {
  document.querySelector("#page-title").textContent = data.title;

  //GET Headings 
  const headings = document.querySelector("#headings");
  headings.innerHTML = "";

  data.headings.forEach(function (text) {
    const item = document.createElement("li");
    item.textContent = text;
    headings.appendChild(item);
  });

  //GET Paragraphs
  const paragraphs = document.querySelector("#paragraphs");
  paragraphs.innerHTML = "";

  data.paragraphs.forEach(function (text) {
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    paragraphs.appendChild(paragraph);
  });

  // GET Tables
  const tables = document.querySelector("#tables");
  tables.innerHTML = "";

  data.tables.forEach(function (tableData) {

    const table = document.createElement("table");

    tableData.forEach(function (rowData, rowNumber) {

      const row = document.createElement("tr");

      rowData.forEach(function (cellData) {

        let cell;

        if (rowNumber === 0) {
          cell = document.createElement("th");
        } else {
          cell = document.createElement("td");
        }

        cell.textContent = cellData;
        row.appendChild(cell);
      });

      table.appendChild(row);
    });

    tables.appendChild(table);
  });

  //GET links
  const links = document.querySelector("#links");
  links.innerHTML = "";

  data.links.forEach(function (link) {
    const item = document.createElement("li");
    const anchor = document.createElement("a");

    anchor.textContent = link.text;
    anchor.href = link.url;
    anchor.target = "_blank";

    item.appendChild(anchor);
    links.appendChild(item);
  });

  // GET Lists
  const lists = document.querySelector("#lists");
  lists.innerHTML = "";

  data.lists.forEach(function (listData) {

    const list = document.createElement("ul");

    listData.forEach(function (text) {

      const item = document.createElement("li");
      item.textContent = text;

      list.appendChild(item);
    });

    lists.appendChild(list);
  });

  const source = document.querySelector("#source");
  source.textContent = data.source;
  source.href = data.source;

  results.hidden = false;
}
