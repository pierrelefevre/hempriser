import { useState, createContext, useEffect } from "react";
import { getListings, getModels } from "../api/api";

const initialState = {
  listings: [],
};

export const ResourceContext = createContext({
  ...initialState,
});

export const ResourceContextProvider = ({ children }) => {
  const [listings, setListings] = useState([]);
  const [models, setModels] = useState([]);

  const fetchListings = async () => {
    let data = await getListings();
    setListings(data);
  };

  const fetchModels = async () => {
    let data = await getModels();
    setModels(data);
  };

  useEffect(() => {
    fetchListings();
    fetchModels();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ResourceContext.Provider
      value={{
        listings,
        models,
      }}
    >
      {children}
    </ResourceContext.Provider>
  );
};
