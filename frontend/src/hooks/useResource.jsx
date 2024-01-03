import { useContext } from "react";
import { ResourceContext } from "../contexts/ResourceContext";

const useResource = () => useContext(ResourceContext);

export default useResource;
