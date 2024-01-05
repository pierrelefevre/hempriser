import {
  Box,
  Card,
  CardContent,
  CardHeader,
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Switch,
  TextField,
} from "@mui/material";
import { useState, useEffect } from "react";
import { predict } from "../api/api";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
  useMapEvents,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

const Predict = () => {
  const [state, setState] = useState({
    latitude: "59.3361328",
    longitude: "18.0726201",
    askingPrice: "",
    fee: "",
    livingArea: "",
    rooms: "",
    constructionYear: "",
    renovationYear: "",
    runningCosts: "",
    housingForm: "",
    housingCooperative: false,
    hasElevator: false,
    hasBalcony: false,
  });
  const [predictedPrice, setPredictedPrice] = useState("");

  const MapEventComponent = () => {
    const map = useMapEvents({
      moveend: () => {
        setState({
          ...state,
          latitude: map.getCenter().lat,
          longitude: map.getCenter().lng,
        });
      },
    });

    return null;
  };

  useEffect(() => {
    if (!Object.values(state).some((value) => value === "")) {
      // Convert state to correct format for the API
      const listing = {};
      listing.lat = parseFloat(state.latitude);
      listing.long = parseFloat(state.longitude);
      listing.askingPrice = parseInt(state.askingPrice);
      listing.fee = parseInt(state.fee);
      listing.livingArea = parseInt(state.livingArea);
      listing.rooms = parseInt(state.rooms);
      listing.constructionYear = parseInt(state.constructionYear);
      listing.renovationYear = parseInt(state.renovationYear);
      listing.runningCosts = parseInt(state.runningCosts);
      listing.housingForm = state.housingForm;
      listing.hasHousingCooperative = state.housingCooperative;
      listing.hasElevator = state.hasElevator;
      listing.hasBalcony = state.hasBalcony;
      listing.soldAt = new Date().toISOString().slice(0, 10);

      predict(listing)
        .then((data) => {
          setPredictedPrice(data.prediction);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }, [state]);

  const housingForms = [
    "Tomt",
    "Vinterbonat fritidshus",
    "Lägenhet",
    "Gård med skogsbruk",
    "Villa",
    "Kedjehus",
    "Parhus",
    "Par-/kedje-/radhus",
    "Radhus",
    "Gård utan jordbruk",
    "Fritidshus",
    "Gård/skog",
    "Övrig",
    "Fritidsboende",
    "Gård med jordbruk",
  ];

  return (
    <Stack spacing={5}>
      <Card
        sx={{
          border: 2,
          borderColor: "#018e51",
          borderRadius: 2,
          boxShadow: 5,
          p: 3,
        }}
      >
        <CardHeader title="House information" />
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={12} md={12}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={10} md={10}>
                  <MapContainer
                    center={[59.3361328, 18.0726201]}
                    zoom={13}
                    scrollWheelZoom={false}
                    style={{ height: "300px", width: "100 %" }}
                  >
                    <TileLayer url="https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png	" />
                    <MapEventComponent />
                    <Marker position={[state.latitude, state.longitude]} />
                  </MapContainer>
                </Grid>
                <Grid item xs={12} sm={2} md={2}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={12} md={12}>
                      <TextField
                        label="Latitude"
                        variant="standard"
                        value={state.latitude}
                        disabled
                      />
                    </Grid>

                    <Grid item xs={12} sm={12} md={12}>
                      <TextField
                        label="Longitude"
                        variant="standard"
                        value={state.longitude}
                        disabled
                      />
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>

            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Asking price"
                variant="outlined"
                onChange={(e) =>
                  setState({
                    ...state,
                    askingPrice: parseInt(e.target.value).toString(),
                  })
                }
                value={state.askingPrice}
                type="number"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Fee"
                variant="outlined"
                onChange={(e) =>
                  setState({
                    ...state,
                    fee: parseInt(e.target.value).toString(),
                  })
                }
                value={state.fee}
                type="number"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Living area"
                variant="outlined"
                onChange={(e) =>
                  setState({
                    ...state,
                    livingArea: parseInt(e.target.value).toString(),
                  })
                }
                value={state.livingArea}
                type="number"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Rooms"
                variant="outlined"
                onChange={(e) =>
                  setState({
                    ...state,
                    rooms: parseInt(e.target.value).toString(),
                  })
                }
                value={state.rooms}
                type="number"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Construction year"
                variant="outlined"
                onChange={(e) =>
                  setState({
                    ...state,
                    constructionYear: parseInt(e.target.value).toString(),
                  })
                }
                value={state.constructionYear}
                type="number"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Renovation year"
                variant="outlined"
                onChange={(e) =>
                  setState({
                    ...state,
                    renovationYear: parseInt(e.target.value).toString(),
                  })
                }
                value={state.renovationYear}
                type="number"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Running costs"
                variant="outlined"
                onChange={(e) =>
                  setState({
                    ...state,
                    runningCosts: parseInt(e.target.value).toString(),
                  })
                }
                value={state.runningCosts}
                type="number"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <FormControl>
                <InputLabel id="housing-form-label">Housing form</InputLabel>
                <Select
                  labelId="housing-form-label"
                  label="Housing form"
                  onChange={(e) =>
                    setState({ ...state, housingForm: e.target.value })
                  }
                  sx={{ width: 300 }}
                  value={state.housingForm}
                >
                  {housingForms.map((housingForm) => (
                    <MenuItem value={housingForm} key={housingForm}>
                      {housingForm}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <FormControlLabel
                control={
                  <Switch
                    onChange={(e) =>
                      setState({
                        ...state,
                        housingCooperative: e.target.checked,
                      })
                    }
                  />
                }
                label="Housing cooperative"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <FormControlLabel
                control={
                  <Switch
                    onChange={(e) =>
                      setState({ ...state, hasElevator: e.target.checked })
                    }
                  />
                }
                label="Has elevator"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={6}>
              <FormControlLabel
                control={
                  <Switch
                    onChange={(e) =>
                      setState({ ...state, hasBalcony: e.target.checked })
                    }
                  />
                }
                label="Has balcony"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card
        sx={{
          border: 2,
          borderColor: "#018e51",
          borderRadius: 2,
          boxShadow: 5,
          p: 3,
        }}
      >
        <CardHeader title="Predicted price" />
        <CardContent>
          <Grid container spacing={2}>
            {/* submit box */}
            <Grid item xs={12} sm={6} md={6}>
              <TextField
                label="Predicted price"
                variant="standard"
                value={predictedPrice}
                disabled
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Stack>
  );
};

export default Predict;
