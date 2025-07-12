function fetchAPI(endpoint, method = "GET", data = null) {
  const baseURL = "http://localhost:5000"; 
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (data) {
    options.body = JSON.stringify(data);
  }

  return fetch(baseURL + endpoint, options).then((res) => res.json());
}
