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

  // Show the page content in its original order
  const content = document.querySelector("#content");
  content.innerHTML = "";

  data.content.forEach(function (item) {

    if (item.type === "heading") {
      const heading = document.createElement(item.level);
      heading.textContent = item.text;
      content.appendChild(heading);
    }

    else if (item.type === "paragraph") {
      const paragraph = document.createElement("p");
      paragraph.textContent = item.text;
      content.appendChild(paragraph);
    }

    else if (item.type === "list") {
      const list = document.createElement(item.list_type);

      item.items.forEach(function (text) {
        const listItem = document.createElement("li");
        listItem.textContent = text;
        list.appendChild(listItem);
      });

      content.appendChild(list);
    }

    else if (item.type === "table") {
      const table = document.createElement("table");

      item.rows.forEach(function (rowData, rowNumber) {
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

      content.appendChild(table);
    }
  });

  // Show useful links
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

  const source = document.querySelector("#source");
  source.textContent = data.source;
  source.href = data.source;

  results.hidden = false;
}
