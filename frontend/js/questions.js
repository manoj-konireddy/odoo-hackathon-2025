document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("askForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const title = document.getElementById("title").value;
      const description = document.getElementById("description").value;
      const tags = document.getElementById("tags").value;

      const res = await fetchAPI("/questions/ask", "POST", {
        user_id: 1, // Use actual session user id
        title,
        description,
        tags
      });

      alert(res.message);
      if (res.success) window.location.href = "index.html";
    });
  }
});

function getCurrentUserId() {
  const user = JSON.parse(localStorage.getItem("stackit_user"));
  return user?.user_id || null;
}

async function vote(answerId, type) {
  const userId = getCurrentUserId();
  if (!userId) {
    alert("You must be logged in to vote.");
    return;
  }

  try {
    const res = await fetch(`http://localhost:5000/votes/${type}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        answer_id: answerId,
        user_id: userId
      })
    });

    const data = await res.json();
    if (data.success) {
      // Reload or update UI without full reload
      location.reload(); // optional: or update count manually
    } else {
      alert(data.message || "Voting failed");
    }
  } catch (err) {
    console.error("Voting error:", err);
    alert("Something went wrong while voting.");
  }
}

// Load Quill
const quill = new Quill("#editor", {
  theme: "snow",
  placeholder: "Describe your question...",
  modules: {
    toolbar: [
      ["bold", "italic", "strike"],
      [{ list: "ordered" }, { list: "bullet" }],
      ["link", "image"],
      [{ align: [] }],
      ["clean"],
    ],
  },
});

const askForm = document.getElementById("askForm");

askForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const title = document.getElementById("title").value;
  const description = quill.root.innerHTML;
  const tags = document.getElementById("tags").value;
  const user = JSON.parse(localStorage.getItem("stackit_user"));

  if (!user) {
    document.getElementById("askMessage").textContent = "You must be logged in to post a question.";
    return;
  }

  try {
    const res = await fetch("http://localhost:5000/questions/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description,
        tags,
        user_id: user.user_id,
      }),
    });

    const data = await res.json();
    if (data.success) {
      window.location.href = "index.html"; // or wherever your question list is
    } else {
      document.getElementById("askMessage").textContent = data.message || "Something went wrong.";
    }
  } catch (err) {
    console.error(err);
    document.getElementById("askMessage").textContent = "Server error. Please try again.";
  }
});

