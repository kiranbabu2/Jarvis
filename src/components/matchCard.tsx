import { Card, CardContent, Grid, Typography } from "@mui/material";
import React from "react";
import PredictionComponent from "./predictionComponent";

interface MatchProps {
    title: string | undefined;
    team1: string;
    team2: string;
    team1prob: number;
}

function MatchCard(props: MatchProps){
    const {title, team1, team2, team1prob} = props;
    const team1Logo = "/assets/images/" + team1 + ".png";
    const team2Logo = "/assets/images/" + team2 + ".png";
    
    return (
        <>
            <Card sx={{ boxShadow: 0 }}>
            {/* <Card> */}
                <CardContent>
                    <Typography sx={{ fontSize: 26, textAlign:"center"}} color="text.primary" gutterBottom>
                        {title}
                    </Typography>
                    
                    <Grid container spacing={2} sx={{
                        alignItems:"center"
                        }}>
                        <Grid item xs={5}>
                            <img src={team1Logo} alt="" width="100%"/>
                        </Grid>
                        <Grid item xs={2}>
                            <Typography sx={{ fontSize: 24 , fontWeight:"bold"}} color="text.primary" gutterBottom>
                                VS
                            </Typography>
                        </Grid>
                        <Grid item xs={5}>
                            <img src={team2Logo} alt="" width="100%"/>
                        </Grid>
                        <Grid item xs={1}></Grid>
                        <Grid item xs={10}>
                            {title === "Today's Match" ? 
                            (<PredictionComponent 
                                team1={team1} 
                                team2={team2} 
                                team1percentage={team1prob}/>) 
                            : null}
                        </Grid>
                        <Grid item xs={1}></Grid>
                    </Grid>
                </CardContent>
            </Card>
        </>
    )
}

export default MatchCard;