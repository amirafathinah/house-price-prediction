const form = document.getElementById("prediction-form");
const statusText = document.getElementById("status");
const resultSection = document.getElementById("result");
const priceText = document.getElementById("price");

// URL backend lokal untuk pengujian.
// Nanti ganti dengan URL Render setelah deployment.
const API_URL = "http://127.0.0.1:5000/predict";

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  const numericFields = [
    "Kamar Tidur",
    "Kamar Mandi",
    "Garasi",
    "Luas Tanah",
    "Luas Bangunan"
  ];

  
const limits = {
  "Kamar Tidur": [1, 20],
  "Kamar Mandi": [1, 20],
  "Garasi": [0, 10],
  "Luas Tanah": [1, 10000],
  "Luas Bangunan": [1, 10000]
};

for (const field of numericFields) {
  data[field] = Number(data[field]);

  const [min, max] = limits[field];

  if (
    !Number.isFinite(data[field]) ||
    data[field] < min ||
    data[field] > max
  ) {
    statusText.textContent =
      `${field} harus berada di antara ${min} dan ${max}.`;
    resultSection.hidden = true;
    return;
  }
}

if (!data["Kecamatan"]) {
  statusText.textContent = "Silakan pilih kecamatan.";
  return;
}

  statusText.textContent = "Sedang menghitung...";
  resultSection.hidden = true;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Prediksi gagal.");
    }

    priceText.textContent = result.formatted_price;
    resultSection.hidden = false;
    statusText.textContent = "Prediksi berhasil!";
  } catch (error) {
    statusText.textContent =
      "Gagal menghubungi backend. Pastikan server Python berjalan.";
    console.error(error);
  }
});
