import {
  Autocomplete,
  Card,
  CardContent,
  CardHeader,
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Switch,
  TextField,
} from "@mui/material";
import { useState } from "react";

import locations from "../api/locations.json";

const Predict = () => {
  const [state, setState] = useState({
    district: "",
    districtInput: "",
    municipality: "",
    municipalityInput: "",
    county: "",
    countyInput: "",
    city: "",
    cityInput: "",
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
    <Card>
      <CardHeader title="Predict" />
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={6}>
            <Autocomplete
              options={locations
                .filter((option) => option.type === "DISTRICT")
                .map((option) => option.fullName + ", " + option.id)}
              onChange={(event, newValue) => {
                setState({ ...state, district: newValue });
              }}
              onInputChange={(event, newInputValue) => {
                setState({ ...state, districtInput: newInputValue });
              }}
              inputValue={state.districtInput}
              value={state.district}
              sx={{ width: 300 }}
              renderInput={(params) => (
                <TextField {...params} label="District" />
              )}
            />
          </Grid>

          <Grid item xs={12} sm={6} md={6}>
            <Autocomplete
              options={locations
                .filter((option) => option.type === "MUNICIPALITY")
                .map((option) => option.fullName + ", " + option.id)}
              onChange={(event, newValue) => {
                setState({ ...state, municipality: newValue });
              }}
              onInputChange={(event, newInputValue) => {
                setState({ ...state, municipalityInput: newInputValue });
              }}
              inputValue={state.municipalityInput}
              value={state.municipality}
              sx={{ width: 300 }}
              renderInput={(params) => (
                <TextField {...params} label="Municipality" />
              )}
            />
          </Grid>

          <Grid item xs={12} sm={6} md={6}>
            <Autocomplete
              options={locations
                .filter((option) => option.type === "COUNTY")
                .map((option) => option.fullName + ", " + option.id)}
              onChange={(event, newValue) => {
                setState({ ...state, county: newValue });
              }}
              onInputChange={(event, newInputValue) => {
                setState({ ...state, countyInput: newInputValue });
              }}
              inputValue={state.countyInput}
              value={state.county}
              sx={{ width: 300 }}
              renderInput={(params) => <TextField {...params} label="County" />}
            />
          </Grid>

          <Grid item xs={12} sm={6} md={6}>
            <Autocomplete
              options={locations
                .filter((option) => option.type === "CITY")
                .map((option) => option.fullName + ", " + option.id)}
              onChange={(event, newValue) => {
                setState({ ...state, city: newValue });
              }}
              onInputChange={(event, newInputValue) => {
                setState({ ...state, cityInput: newInputValue });
              }}
              inputValue={state.cityInput}
              value={state.city}
              sx={{ width: 300 }}
              renderInput={(params) => <TextField {...params} label="City" />}
            />
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
                setState({ ...state, fee: parseInt(e.target.value).toString() })
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
              control={<Switch />}
              label="Housing cooperative"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={6}>
            <FormControlLabel control={<Switch />} label="Has elevator" />
          </Grid>
          <Grid item xs={12} sm={6} md={6}>
            <FormControlLabel control={<Switch />} label="Has balcony" />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default Predict;
