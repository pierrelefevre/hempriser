import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Divider,
  Stack,
  Typography,
} from "@mui/material";
import useResource from "../hooks/useResource";

const About = () => {
  const { models } = useResource();

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
        <CardHeader title="Available models" />
        <CardContent>
          <Stack spacing={2}>
            {models.map((model, index) => (
              <Accordion key={"model-" + index}>
                <AccordionSummary>
                  <Typography variant="h6">{model.name}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography gutterBottom>
                    {"Trained at: " + model.metadata.trainedAt}
                  </Typography>
                  <Typography gutterBottom>
                    {"Target: " + model.metadata.target}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Typography gutterBottom>Features</Typography>
                  <Stack
                    spacing={2}
                    direction={"row"}
                    flexWrap={"wrap"}
                    useFlexGap
                    alignItems={"center"}
                    justifyContent={"flex-start"}
                  >
                    {model.metadata.features.map((feature, featureIndex) => (
                      <Chip label={feature} key={"feature-" + featureIndex} />
                    ))}
                  </Stack>
                </AccordionDetails>
              </Accordion>
            ))}
          </Stack>
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
        <CardHeader title="What's this?" />
        <CardContent>
          <Stack spacing={2}>
            <Typography variant="body1">
              Bostadspriser is a tool for predicting the price of a house in
              Sweden. It is based on a machine learning model trained on data
              from Hemnet.
            </Typography>
            <Typography variant="body1">
              View the source on{" "}
              <a href="https://github.com/pierrelefevre/bostadspriser">
                GitHub
              </a>
              .
            </Typography>
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  );
};

export default About;
