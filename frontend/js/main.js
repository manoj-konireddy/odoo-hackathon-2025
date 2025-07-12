async function loadTags() {
  const tags = await fetchAPI("/questions/tags");
  const container = document.getElementById("tagFilters");
  if (tags.data) {
    container.innerHTML = tags.data.map(tag => `
      <button class="bg-gray-200 text-sm px-3 py-1 rounded hover:bg-blue-100" onclick="filterByTag('${tag.name}')">${tag.name}</button>
    `).join("");
  }
}

function filterByTag(tag) {
  console.log("Filter by tag:", tag);
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadTags(); 

});

async function loadQuestions() {
  try {
    const res = await fetch("http://localhost:5000/questions/");
    const data = await res.json();

    const container = document.getElementById("question-list");
    container.innerHTML = ""; // Clear existing

    if (data.success && data.data.length > 0) {
      data.data.forEach((q) => {
        const card = document.createElement("div");
        card.className = "bg-white p-4 rounded shadow";

        card.innerHTML = `
          <h3 class="text-xl font-semibold text-blue-700">${q.title}</h3>
          <p class="text-gray-700 mt-2">${q.description}</p>
          <p class="text-sm text-gray-500 mt-1">Asked by ${q.author}</p>
        `;

        container.appendChild(card);
      });
    } else {
      container.innerHTML = "<p>No questions found.</p>";
    }
  } catch (err) {
    console.error("Failed to load questions", err);
    document.getElementById("question-list").innerHTML = "<p class='text-red-600'>Error loading questions</p>";
  }
}

// Call on page load
window.addEventListener("DOMContentLoaded", loadQuestions);
