import {
  AppBar,
  Button,
  IconButton,
  Tab,
  Tabs,
  Toolbar,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import Iconify from "./Iconify";
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

const Navbar = () => {
  const [currentTab, setCurrentTab] = useState(0);

  let location = useLocation();

  useEffect(() => {
    if (location.pathname === "/") {
      setCurrentTab(0);
    } else if (location.pathname.startsWith("/predict")) {
      setCurrentTab(1);
    } else if (location.pathname.startsWith("/about")) {
      setCurrentTab(2);
    }
  }, [location]);

  return (
    <AppBar position="static" sx={{ background: "#e4e8da", color: "#013a14" }}>
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 1 }}
          component={Link}
          to="/"
        >
          <img src="bostadspriser-transparent.png" style={{ height: "3rem" }} />
        </IconButton>

        <Typography
          variant="h6"
          sx={{
            flexGrow: 1,
            display: { xs: "none", sm: "none", md: "inline" },
            textDecoration: "none",
            fontWeight: 900,
          }}
          component={Link}
          to="/"
          color="inherit"
        >
          Bostadspriser
        </Typography>

        <Tabs value={currentTab}>
          <Tab
            label="Listings"
            icon={<Iconify icon="ph:house-fill" />}
            iconPosition="start"
            component={Link}
            to="/"
          />
          <Tab
            label="Predict"
            icon={<Iconify icon="fluent:predictions-24-filled" />}
            iconPosition="start"
            component={Link}
            to="/predict"
          />
          <Tab
            label="About"
            icon={<Iconify icon="fluent:question-circle-12-filled" />}
            iconPosition="start"
            component={Link}
            to="/about"
          />
        </Tabs>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
