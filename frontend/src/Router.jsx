import { Navigate, useRoutes } from "react-router-dom";
import PageLayout from "./components/PageLayout";
import Listings from "./pages/Listings";
import Predict from "./pages/Predict";
import About from "./pages/About";

export default function Router() {
    return useRoutes([
      {
        path: "/",
        element: <PageLayout />,
        children: [
          { path: "/", element: <Listings /> },
          { path: "predict", element: <Predict /> },
          { path: "about", element: <About /> },
        ],
      },
      {
        path: "*",
        element: <Navigate to="/" replace />,
      },
    ]);
  }
  