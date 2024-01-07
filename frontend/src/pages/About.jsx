import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
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
  const { models } = useResource();
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
        <CardHeader title="Model performance" />
        <CardContent>
          <LineChart
            dataset={dataset}
            xAxis={[{ dataKey: "timestamp", scaleType: "time" }]}
            series={[
              { dataKey: "r2", label: "R2" },
              { dataKey: "mse", label: "MSE" },
              { dataKey: "rmse", label: "RMSE" },
            ]}
            width={600}
            height={300}
            yAxis={[{ scaleType: "log" }]}
          />
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
