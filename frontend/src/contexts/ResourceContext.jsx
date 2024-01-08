import { useState, createContext, useEffect } from "react";
import { getCronPredictions, getListings, getModels } from "../api/api";

const initialState = {
  listings: [],
};

export const ResourceContext = createContext({
  ...initialState,
});

export const ResourceContextProvider = ({ children }) => {
  const [listings, setListings] = useState([]);
  const [models, setModels] = useState([]);
  const [cronPredictions, setCronPredictions] = useState([]);
  const [page, setPage] = useState(0);
  const n = 10;

  const fetchListings = async () => {
    let data = await getListings(page, n);
    if (data.length === 0) {
      return;
    }
    setListings([...listings, ...data]);
  };

  const fetchModels = async () => {
    let data = await getModels();
    setModels(data);
  };

  const fetchCronPredictions = async () => {
    let data = await getCronPredictions();
    setCronPredictions(data);
  };

  const nextPage = () => {
    setPage(page + 1);
    fetchListings();
  };

  useEffect(() => {
    fetchListings();
    fetchModels();
    fetchCronPredictions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ResourceContext.Provider
      value={{
        listings,
        models,
        cronPredictions,
        nextPage,
      }}
    >
      {children}
    </ResourceContext.Provider>
  );
};
