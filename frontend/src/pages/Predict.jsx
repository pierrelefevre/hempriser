import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Checkbox,
  FormControl,
  FormControlLabel,
  FormGroup,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useState, useEffect } from "react";
import { predict } from "../api/api";
import { MapContainer, Marker, TileLayer, useMapEvents } from "react-leaflet";

import "leaflet/dist/leaflet.css";
import prettyNum from "pretty-num";

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
  const [prediction, setPrediction] = useState(null);
  const [askingPrice, setAskingPrice] = useState(false);

  const generateRandomState = () => {
    let randomState = {
      latitude: "59.3361328",
      longitude: "18.0726201",
      fee: Math.floor(Math.random() * 6000).toString(),
      livingArea: Math.floor(50 + Math.random() * 20).toString(),
      rooms: Math.floor(2 + Math.random() * 3).toString(),
      constructionYear: Math.floor(1900 + Math.random() * 124).toString(),
      renovationYear: Math.floor(2010 + Math.random() * 10).toString(),
      runningCosts: Math.floor(Math.random() * 5000).toString(),
      housingForm: "Lägenhet",
      housingCooperative: Math.random() >= 0.5,
      hasElevator: Math.random() >= 0.5,
      hasBalcony: Math.random() >= 0.5,
    };

    let showAskingPrice = Math.random() >= 0.7;
    if (showAskingPrice) {
      (randomState.askingPrice = Math.floor(
        Math.random() * 10000000
      ).toString()),
        setAskingPrice(true);
    } else {
      randomState.askingPrice = "";
      setAskingPrice(false);
    }
    setState(randomState);
  };

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
    // Convert state to correct format for the API
    const listing = {};
    listing.lat = parseFloat(state.latitude);
    listing.long = parseFloat(state.longitude);
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

    if (askingPrice) {
      listing.askingPrice = parseInt(state.askingPrice);
    }

    predict(listing)
      .then((data) => {
        setPrediction(data);
      })
      .catch((error) => {
        setPrediction({ error: error });
      });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state, askingPrice]);

  useEffect(() => {
    generateRandomState();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
                sx={{ width: 300 }}
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
                sx={{ width: 300 }}
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
                sx={{ width: 300 }}
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
                sx={{ width: 300 }}
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
                sx={{ width: 300 }}
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
                sx={{ width: 300 }}
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
              <FormGroup>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={state.housingCooperative}
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
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={state.hasElevator}
                      onChange={(e) =>
                        setState({ ...state, hasElevator: e.target.checked })
                      }
                    />
                  }
                  label="Elevator"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={state.hasBalcony}
                      onChange={(e) =>
                        setState({ ...state, hasBalcony: e.target.checked })
                      }
                    />
                  }
                  label="Balcony"
                />
              </FormGroup>
            </Grid>

            <Grid item xs={12} sm={12} md={12}>
              <Box sx={{ height: 50 }} />
            </Grid>

            <Grid item xs={12} sm={4} md={4}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={askingPrice}
                    onChange={(e) => setAskingPrice(e.target.checked)}
                  />
                }
                label="Have an asking price already?"
              />
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
                disabled={!askingPrice}
              />
            </Grid>

            <Grid item xs={12} sm={5} md={5}></Grid>

            <Grid item xs={12} sm={3} md={3}>
              <Button
                variant="contained"
                onClick={() => generateRandomState()}
                sx={{ width: "100%" }}
              >
                Randomize
              </Button>
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
          {!prediction && (
            <Typography variant="body2">
              Fill in all fields to show price. Predictions with Asking Price is
              optional, and uses a different model
            </Typography>
          )}
          {prediction && prediction.error && (
            <Typography variant="body2">
              {"Could not get price because of error: " +
                JSON.stringify(prediction.error)}
            </Typography>
          )}
          {prediction && !prediction.error && (
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={6}>
                <Typography variant="h3">
                  {prettyNum(Math.floor(prediction.prediction), {
                    thousandsSeparator: " ",
                  }) + " SEK"}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={6}>
                <Typography variant="caption">Model used</Typography>
                <br />
                <Typography variant="h6">{prediction.model}</Typography>
              </Grid>
            </Grid>
          )}
        </CardContent>
      </Card>
    </Stack>
  );
};

export default Predict;
