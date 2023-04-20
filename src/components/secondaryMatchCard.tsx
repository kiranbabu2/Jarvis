import { Card, CardContent, Grid, Typography } from "@mui/material";
import { Box } from "@mui/system";
import React from "react";
import PredictionComponent from "./predictionComponent";

interface MatchProps {
    title: string;
    plot: string;
}

const style = { objecFit: "cover", width: "100%", height: "35em", backgroundSize: "cover" };
function SecondaryMatchCard(props: MatchProps) {
    const { title, plot } = props;
    return (
        <Card sx={{ backgroundColor: "#FAFAFA", boxShadow: 0 }}>
            <CardContent>
                <Typography sx={{ fontSize: 20 }} color="text.primary" gutterBottom>
                    {title}
                </Typography>
                <Box sx={{ my: 5, mx: { xs: '10%', md: '20%' } }}>
                    <img style={style} src={plot} alt="Plot" />
                </Box>
            </CardContent>
        </Card>
    )
}

export default SecondaryMatchCard;