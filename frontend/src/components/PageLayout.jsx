import { Box, Container } from "@mui/material";

import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

const PageLayout = () => {
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <Navbar />
      </Box>
      <Container sx={{ p: 5 }}>
        <Outlet />
      </Container>
    </>
  );
};

export default PageLayout;
