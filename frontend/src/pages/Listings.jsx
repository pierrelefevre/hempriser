import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  CardMedia,
  Chip,
  Grid,
  InputAdornment,
  LinearProgress,
  Link,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import useResource from "../hooks/useResource";
import Iconify from "../components/Iconify";
import { MapContainer, Marker, TileLayer } from "react-leaflet";

const Listings = () => {
  const { listings } = useResource();

  if (!(listings && listings.length > 0)) {
    return (
      <Stack spacing={3}>
        <Typography variant="h5" gutterBottom>
          Loading...
        </Typography>
        <LinearProgress />
      </Stack>
    );
  }

  return (
    <Grid container spacing={5}>
      <Grid item xs={12}>
        <TextField
          fullWidth
          placeholder="Search by Hemnet URL"
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
            <CardMedia
              component="img"
              height="300"
              image={listing.thumbnail}
              alt="house image"
            />
            <CardHeader title={listing.streetAddress} />

            <CardContent>
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
                  icon={<Iconify icon="mdi:currency-usd" />}
                  label={`Asking Price: ${listing.askingPrice}`}
                />
                <Chip
                  icon={<Iconify icon="mdi:calendar" />}
                  label={`Construction Year: ${listing.constructionYear}`}
                />
                <Chip
                  icon={<Iconify icon="mdi:cash" />}
                  label={`Monthly fee: ${listing.fee}`}
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
                  label={`Running Costs: ${listing.runningCosts}`}
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
              </Stack>
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
            </CardContent>

            <CardActions>
              <Button
                size="small"
                color="primary"
                LinkComponent={Link}
                href={listing.url}
              >
                View on Hemnet
              </Button>
            </CardActions>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default Listings;
