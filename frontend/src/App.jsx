import { ThemeProvider } from "@emotion/react";
import { CssBaseline, createTheme } from "@mui/material";
import Router from "./Router";
import { BrowserRouter } from "react-router-dom";
import { ResourceContextProvider } from "./contexts/ResourceContext";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#018e51",
    },
    secondary: {
      main: "#013a14",
    },
    background: {
      default: "#f9fff9",
    },
  },
});

function App() {
  return (
    <BrowserRouter>
      <ResourceContextProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Router />
        </ThemeProvider>
      </ResourceContextProvider>
    </BrowserRouter>
  );
}

export default App;
