import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Divider,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import useResource from "../hooks/useResource";
import { LineChart } from "@mui/x-charts/LineChart";
import { useEffect, useState } from "react";
import Iconify from "../components/Iconify";

const About = () => {
  const { models, cronPredictions } = useResource();
  const [dataset, setDataset] = useState([]);

  useEffect(() => {
    if (!models) return;

    let data = [];
    models.forEach((model) => {
      if (
        !(
          model.metadata &&
          model.metadata.model &&
          model.metadata.model.r2 &&
          model.metadata.model.rmse &&
          model.metadata.model.mse
        )
      )
        return;

      let unixTime = new Date(model.metadata.trainedAt);
      data.push({
        timestamp: unixTime,
        r2: model.metadata.model.r2,
        mse: model.metadata.model.mse,
        rmse: model.metadata.model.rmse,
      });
    });

    setDataset(data);
  }, [models]);

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
                  <Typography gutterBottom>Training results</Typography>
                  <TableContainer component={Paper}>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Model Type</TableCell>
                          <TableCell>MSE</TableCell>
                          <TableCell>RMSE</TableCell>
                          <TableCell>R2</TableCell>
                          <TableCell>Best</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {Object.keys(model.results).map(
                          (modelType, modelTypeIndex) => (
                            <TableRow
                              key={modelTypeIndex + "row"}
                              sx={
                                modelTypeIndex === 0
                                  ? {
                                      background: "#f0f0f0",
                                    }
                                  : null
                              }
                            >
                              <TableCell>{modelType}</TableCell>
                              <TableCell>
                                {model.results[modelType].mse}
                              </TableCell>
                              <TableCell>
                                {model.results[modelType].rmse}
                              </TableCell>
                              <TableCell>
                                {model.results[modelType].r2}
                              </TableCell>
                              <TableCell>
                                <Iconify
                                  icon={
                                    modelTypeIndex === 0
                                      ? "mdi:check"
                                      : "mdi:close"
                                  }
                                />
                              </TableCell>
                            </TableRow>
                          )
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>

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
                      <Chip
                        label={feature}
                        key={"feature-" + featureIndex}
                        color={
                          feature === "askingPrice" ? "primary" : "default"
                        }
                      />
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
        <CardHeader title="Training results" />
        <CardContent>
          <LineChart
            dataset={dataset}
            xAxis={[{ dataKey: "timestamp", scaleType: "time" }]}
            series={[
              { dataKey: "r2", label: "R2" },
              { dataKey: "mse", label: "MSE" },
              { dataKey: "rmse", label: "RMSE" },
            ]}
            style={{ width: "100%" }}
            height={300}
            yAxis={[{ scaleType: "log" }]}
          />
        </CardContent>
      </Card>
      {cronPredictions && (
        <Card
          sx={{
            border: 2,
            borderColor: "#018e51",
            borderRadius: 2,
            boxShadow: 5,
            p: 3,
          }}
        >
          <CardHeader title="Batch inference results" />
          <CardContent>
            <Stack spacing={2}>
              {cronPredictions["predictions"] && (
                <LineChart
                  xAxis={[
                    {
                      scaleType: "time",
                      data: cronPredictions["predictions"].x.map(
                        (x) => new Date(x)
                      ),
                    },
                  ]}
                  series={[
                    {
                      label: "predictions over time (change in %)",
                      data: cronPredictions["predictions"].yPercent,
                    },
                  ]}
                  style={{ width: "100%" }}
                  height={300}
                />
              )}

              <Box sx={{ width: "100%", overflowX: "scroll" }}>
                {cronPredictions["predictions"] && (
                  <LineChart
                    xAxis={[
                      {
                        scaleType: "time",
                        data: cronPredictions["predictions"].x.map(
                          (x) => new Date(x)
                        ),
                      },
                    ]}
                    series={[
                      {
                        label: "predictions over time ",
                        data: cronPredictions["predictions"].y,
                      },
                    ]}
                    width={5000}
                    height={300}
                  />
                )}
              </Box>

              {cronPredictions["rmse"] && (
                <LineChart
                  xAxis={[
                    {
                      scaleType: "time",
                      data: cronPredictions["rmse"].x.map((x) => new Date(x)),
                    },
                  ]}
                  series={[{ label: "RMSE", data: cronPredictions["rmse"].y }]}
                  style={{ width: "100%" }}
                  height={300}
                />
              )}
            </Stack>
          </CardContent>
        </Card>
      )}

      <Card
        sx={{
          border: 2,
          borderColor: "#018e51",
          borderRadius: 2,
          boxShadow: 5,
          p: 3,
        }}
      >
        <CardHeader title="Comparing to Booli" />
        <CardContent>
          <Stack spacing={2}>
            <Typography variant="body1">
              As a good sanity check, we wanted to compare to an established
              source of property price predictions in Sweden. Booli has a{" "}
              <a href="https://www.booli.se/vardera">free tool</a> for
              predicting prices with most parameters overlapping ours. We
              designed a test set of properties to be quite broad, yet we could
              not test summer houses, plots nor farms as these are not supported
              by Booli.
            </Typography>
            <Typography variant="body1">
              Most results were within 20% of the estimated price by Booli,
              however it is clear that the prices in Stockholm, Göteborg and
              Malmö are much more accurate than those outsite these larger
              cities.
            </Typography>

            <iframe
              width="100%"
              height="315px"
              src="https://docs.google.com/spreadsheets/d/e/2PACX-1vSOHaDYHNmf6ToxAlEQie3N7AxtFhvhdsUhHoRFriU_Xpnd0flEGz9TYqDkh78r9AY_Qj-WtcCnWyJ9/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false"
            ></iframe>
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
              Hempriser is a tool for predicting the price of a house in
              Sweden. It is based on a machine learning model trained on data
              from Hemnet.
            </Typography>
            <Typography variant="body1">
              View the source on{" "}
              <a href="https://github.com/pierrelefevre/hempriser">
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
