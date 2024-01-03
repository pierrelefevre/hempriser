import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  LinearProgress,
  Link,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { getListings } from "../api/api";

const Listings = () => {
  const [listings, setListings] = useState([]);

  useEffect(() => {
    getListings().then((data) => {
      setListings(data);
    });
  }, []);

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
    <>
      {listings.map((listing, index) => (
        <Card key={"listing-" + index}>
          <CardHeader title={listing.housingForm} />
          <CardContent>
            <Stack spacing={2}>
              <Typography variant="body1">{listing.city}</Typography>
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
      ))}
    </>
  );
};

export default Listings;
