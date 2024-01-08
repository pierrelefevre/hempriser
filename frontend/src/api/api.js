export const api_url = "https://bostadspriser-api.app.cloud.cbh.kth.se";
// export const api_url = "http://localhost:8080";

export const getListings = async (page, pageSize) => {
  if (page === undefined) {
    page = 10;
  }
  if (pageSize === undefined) {
    pageSize = 0;
  }
  const response = await fetch(
    api_url + "/listings?page=" + page + "&pageSize=" + pageSize
  );
  const data = await response.json();

  return data;
};

export const getModels = async () => {
  const response = await fetch(api_url + "/models");
  const data = await response.json();

  return data;
};

export const predict = async (listing) => {
  const response = await fetch(api_url + "/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(listing),
  });

  if (response.status !== 200) {
    return response.json();
  }

  return response.json();
};

export const predictWithHemnetURL = async (url) => {
  const response = await fetch(api_url + "/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: url }),
  });

  if (response.status !== 200) {
    return response.json();
  }

  return response.json();
};

export const getCronPredictions = async () => {
  const response = await fetch(api_url + "/predictions");
  const data = await response.json();

  return data;
};
