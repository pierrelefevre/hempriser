import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Grid,
  LinearProgress,
  Link,
  Stack,
  Typography,
} from "@mui/material";
import useResource from "../hooks/useResource";

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
    <Grid container spacing={2}>
      {listings.map((listing, index) => (
        <Grid item xs={12} sm={6} md={6} key={"listing-" + index}>
          <Card>
            <CardHeader
              title={
                listing.rooms +
                " room " +
                listing.housingForm +
                ", " +
                listing.constructionYear
              }
            />
            <CardContent>
              <Stack spacing={2}>
                <Typography variant="body1">
                  {listing.district +
                    ", " +
                    listing.municipality +
                    ", " +
                    listing.county +
                    ", " +
                    listing.city}
                </Typography>
              </Stack>
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
