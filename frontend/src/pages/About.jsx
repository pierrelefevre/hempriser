import {
  Card,
  CardContent,
  CardHeader,
  Stack,
  Typography,
} from "@mui/material";

const About = () => {
  return (
    <Card>
      <CardHeader title="What's this?" />
      <CardContent>
        <Stack spacing={2}>
          <Typography variant="body1">
            Bostadspriser is a tool for predicting the price of a house in
            Sweden. It is based on a machine learning model trained on data from
            Hemnet.
          </Typography>
          <Typography variant="body1">
            View the source on{" "}
            <a href="https://github.com/pierrelefevre/bostadspriser">GitHub</a>.
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default About;
