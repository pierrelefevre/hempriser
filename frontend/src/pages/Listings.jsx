import {
  Alert,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  CardMedia,
  Chip,
  Collapse,
  Grid,
  InputAdornment,
  LinearProgress,
  Link,
  Skeleton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import useResource from "../hooks/useResource";
import Iconify from "../components/Iconify";
import { MapContainer, Marker, TileLayer } from "react-leaflet";
import { prettyNum } from "pretty-num";
import { useEffect, useState } from "react";
import { BottomScrollListener } from "react-bottom-scroll-listener";

import { predictWithHemnetURL } from "../api/api";

const Listings = () => {
  const { listings, nextPage } = useResource();
  const [loading, setLoading] = useState(false);

  const [hemnetURL, setHemnetURL] = useState("");
  const [hemnetListing, setHemnetListing] = useState(null);
  const [error, setError] = useState(null);

  const handleBottom = () => {
    setLoading(true);
    nextPage();
  };

  useEffect(() => {
    if (!hemnetURL) {
      setHemnetListing(null);
      setError(null);
      return;
    }
    setHemnetListing(null);
    setError(null);

    predictWithHemnetURL(hemnetURL).then((response) => {
      if (response.error) {
        setError(response.error);
        return;
      }

      setError(null);
      setHemnetListing(response);
    });
  }, [hemnetURL]);

  useEffect(() => {
    setLoading(false);
  }, [listings]);

  const renderPredictions = (listing) => {
    if (!listing.prediction) {
      return null;
    }

    let withAskingPrice = 0;
    let withoutAskingPrice = 0;

    const format = (num) => {
      return prettyNum(Math.floor(num), {
        thousandsSeparator: " ",
      });
    };

    Object.keys(listing.prediction).forEach((key) => {
      if (!listing.prediction[key]) return;

      if (key.includes("with-askingPrice")) {
        withAskingPrice = listing.prediction[key].prediction;
      } else {
        withoutAskingPrice = listing.prediction[key].prediction;
      }
    });

    return (
      <>
        {withAskingPrice > 10000 && (
          <Chip
            icon={<Iconify icon="mdi:currency-usd" />}
            label={`Predicted Price (with asking price): ${format(
              withAskingPrice
            )} SEK`}
            color="secondary"
          />
        )}

        {withoutAskingPrice > 10000 && (
          <Chip
            icon={<Iconify icon="mdi:currency-usd" />}
            label={`Predicted Price (without asking price): ${format(
              withoutAskingPrice
            )} SEK`}
            color="secondary"
          />
        )}
      </>
    );
  };

  const renderListingChips = (listing) => {
    return (
      <Stack
        spacing={2}
        direction={"row"}
        flexWrap={"wrap"}
        useFlexGap
        alignItems={"center"}
        justifyContent={"flex-start"}
      >
        <Chip
          icon={<Iconify icon="mdi:home-city-outline" />}
          label={`Type: ${listing.housingForm}`}
        />
        <Chip
          icon={<Iconify icon="mdi:calendar" />}
          label={`Construction Year: ${listing.constructionYear}`}
        />
        <Chip
          icon={<Iconify icon="mdi:cash" />}
          label={`Monthly fee: ${prettyNum(listing.fee, {
            thousandsSeparator: " ",
          })} SEK`}
        />

        <Chip
          icon={<Iconify icon="mdi:home-floor-0" />}
          label={`Living Area: ${listing.livingArea} m²`}
        />
        <Chip
          icon={<Iconify icon="mdi:calendar-edit" />}
          label={`Renovation Year: ${listing.renovationYear}`}
        />
        <Chip
          icon={<Iconify icon="mdi:door" />}
          label={`Rooms: ${listing.rooms}`}
        />
        <Chip
          icon={<Iconify icon="mdi:cash-multiple" />}
          label={`Running Costs: ${prettyNum(listing.runningCosts, {
            thousandsSeparator: " ",
          })} SEK`}
        />

        {listing.hasBalcony && (
          <Chip
            icon={<Iconify icon="mdi:balcony" />}
            label={"Has Balcony"}
            sx={{ border: 3, borderColor: "#018e51" }}
          />
        )}

        {listing.hasElevator && (
          <Chip
            icon={<Iconify icon="mdi:elevator" />}
            label="Has Elevator"
            sx={{ border: 3, borderColor: "#018e51" }}
          />
        )}
        {listing.housingCooperative && (
          <Chip
            icon={<Iconify icon="mdi:home-group" />}
            label="Housing Cooperative"
            sx={{ border: 3, borderColor: "#018e51" }}
          />
        )}

        <Chip
          icon={<Iconify icon="mdi:currency-usd" />}
          label={`Asking Price: ${prettyNum(listing.askingPrice, {
            thousandsSeparator: " ",
          })} SEK`}
          color="primary"
        />
        {renderPredictions(listing)}
      </Stack>
    );
  };

  const renderListingMap = (listing) => {
    if (!listing.lat || !listing.long) return null;

    return (
      <Box sx={{ height: 194, width: "100%", mt: 3 }}>
        <MapContainer
          center={[listing.lat, listing.long]}
          zoom={13}
          scrollWheelZoom={false}
          style={{ height: "100%", width: "100 %" }}
        >
          <TileLayer url="https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png	" />
          <Marker position={[listing.lat, listing.long]} />
        </MapContainer>
      </Box>
    );
  };

  const renderListingThumbnail = (listing) => {
    if (!listing.thumbnail) return null;

    return (
      <CardMedia
        component="img"
        height="300"
        image={listing.thumbnail}
        alt="house image"
        onClick={() => window.open(listing.url, "_blank")}
        style={{ cursor: "pointer" }}
      />
    );
  };

  const renderListingHeader = (listing) => {
    if (!listing.streetAddress) return null;

    return <CardHeader title={listing.streetAddress} />;
  };

  return (
    <BottomScrollListener onBottom={handleBottom}>
      <Grid container spacing={5}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            placeholder="Search by Hemnet URL"
            onChange={(e) => setHemnetURL(e.target.value)}
            value={hemnetURL}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Iconify icon="mdi:magnify" />
                </InputAdornment>
              ),
              sx: {
                py: 1,
                px: 3,
                borderRadius: 2,
                border: 2,
                borderColor: "#018e51",
                boxShadow: 5,
              },
            }}
          />
        </Grid>
        {error && (
          <Grid item xs={12}>
            <Alert severity="error">{error}</Alert>
          </Grid>
        )}

        <Grid item xs={12}>
          <Collapse in={!error && hemnetURL != ""}>
            {hemnetListing ? (
              <Card
                sx={{
                  border: 2,
                  borderColor: "#018e51",
                  borderRadius: 2,
                  boxShadow: 5,
                }}
              >
                {renderListingThumbnail(hemnetListing)}
                {renderListingHeader(hemnetListing)}

                <CardContent>
                  {renderListingChips(hemnetListing)}
                  {renderListingMap(hemnetListing)}
                </CardContent>
              </Card>
            ) : (
              <Skeleton
                variant="rectangular"
                height={750}
                width={"100%"}
                animation="wave"
                sx={{
                  border: 2,
                  borderColor: "#018e51",
                  borderRadius: 2,
                  boxShadow: 5,
                }}
              />
            )}
          </Collapse>
        </Grid>

        {listings.map((listing, index) => (
          <Grid item xs={12} sm={6} md={6} key={"listing-" + index}>
            <Card
              sx={{
                border: 2,
                borderColor: "#018e51",
                borderRadius: 2,
                boxShadow: 5,
              }}
            >
              {renderListingThumbnail(listing)}
              {renderListingHeader(listing)}

              <CardContent>
                {renderListingChips(listing)}
                {renderListingMap(listing)}
              </CardContent>

              <CardActions>
                <Button
                  size="small"
                  color="primary"
                  LinkComponent={Link}
                  href={listing.url}
                  target="_blank"
                  rel="noopener"
                >
                  View on Hemnet
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      {!(listings && listings.length > 0) ||
        (loading && (
          <Stack spacing={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Loading...
            </Typography>
            <LinearProgress />
          </Stack>
        ))}
    </BottomScrollListener>
  );
};

export default Listings;
