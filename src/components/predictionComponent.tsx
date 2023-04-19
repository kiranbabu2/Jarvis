import { Box, LinearProgress, LinearProgressProps, styled, Typography } from "@mui/material";
import React from "react";

interface StyledProgressProps extends LinearProgressProps {
    team1: string,
    team2: string
}

const StyledProgress = styled(LinearProgress, {
    shouldForwardProp: (prop) => prop !== 'team1' && prop!=='team2'
  })<StyledProgressProps>(({ team1, team2, theme }) => ({
    height: 10,
    [`& .MuiLinearProgress-bar`]: { 
        backgroundColor: 
            team1 === "MI" ? theme.palette.MI?.main :
            team1 === "RCB" ? theme.palette.RCB?.main : 
            team1 === "CSK" ? theme.palette.CSK?.main :
            team1 === "KKR" ? theme.palette.KKR?.main :
            team1 === "DC" ? theme.palette.DC?.main :
            team1 === "RR" ? theme.palette.RR?.main :
            team1 === "SRH" ? theme.palette.SRH?.main :
            team1 === "PK" ? theme.palette.PK?.main :
            "palevioletred"},
    
        backgroundColor: 
            team2 === "MI" ? theme.palette.MI?.main :
            team2 === "RCB" ? theme.palette.RCB?.main : 
            team2 === "CSK" ? theme.palette.CSK?.main :
            team2 === "KKR" ? theme.palette.KKR?.main :
            team2 === "DC" ? theme.palette.DC?.main :
            team2 === "RR" ? theme.palette.RR?.main :
            team2 === "SRH" ? theme.palette.SRH?.main :
            team2 === "PK" ? theme.palette.PK?.main :
            "mediumaquamarine",

  }));

  interface PredictionComponentProps {
    team1: string,
    team2: string,
    team1percentage: number
  }

function PredictionComponent(props: PredictionComponentProps){
    const {team1, team2, team1percentage} = props;

    return(
        <>
            <StyledProgress variant="determinate" value={team1percentage} team1={team1} team2={team2}></StyledProgress>
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography fontSize={18}>
                    {team1percentage}%
                </Typography>
                <Typography fontSize={18}>
                    {100- team1percentage}%
                </Typography>
            </Box>
        </>
    )
}

export default PredictionComponent;