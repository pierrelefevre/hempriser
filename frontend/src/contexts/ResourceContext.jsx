import { useState, createContext, useEffect } from "react";
import { getListings } from "../api/api";
import locations from "../api/locations.json";

const initialState = {
  listings: [],
};

export const ResourceContext = createContext({
  ...initialState,
});

export const ResourceContextProvider = ({ children }) => {
  const [listings, setListings] = useState([]);

  let forms = new Set();
  const fetchListings = async () => {
    let data = await getListings();

    data.forEach((element) => {
      let city = locations.find((x) => x.id == element.city);
      if (city) element.city = city.fullName;

      let district = locations.find((x) => x.id == element.district);
      if (district) element.district = district.fullName;

      let municipality = locations.find((x) => x.id == element.municipality);
      if (municipality) element.municipality = municipality.fullName;

      let county = locations.find((x) => x.id == element.county);
      if (county) element.county = county.fullName;
    });

    setListings(data);
  };

  useEffect(() => {
    fetchListings();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ResourceContext.Provider
      value={{
        listings,
        locations,
      }}
    >
      {children}
    </ResourceContext.Provider>
  );
};
