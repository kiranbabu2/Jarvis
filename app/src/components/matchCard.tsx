import { Card, CardContent, Grid, Typography } from "@mui/material";
import React from "react";
import PredictionComponent from "./predictionComponent";

interface MatchProps {
  title: string | undefined;
  team1: string;
  team2: string;
  team1prob: number;
  matchResults: any;
}

function MatchCard(props: MatchProps) {
  const { title, team1, team2, team1prob, matchResults } = props;
  const team1Logo = "/assets/images/" + team1 + ".png";
  const team2Logo = "/assets/images/" + team2 + ".png";
  console.log('Match: ', matchResults);
  console.log('test: ', matchResults.data[matchResults.data.length]);
  const isteamTwoBatting = matchResults.data[matchResults.data.length - 1].innings_over[0] === '2';
  // const inningsOneOver = matchResults.data[matchResults.data.length - 1].innings_over.split('_')[1];
  // const inningsOneScore = matchResults.data[matchResults.data.length - 1].innings_score;
  // const inningsoneWickets = matchResults.data[matchResults.data.length - 1].innings_wickets;

  // filter from matchResults array and get last index of innings one data 
  const inningsOneData = matchResults.data.filter((over: any) => {
    return over.innings_over[0] === '1';
  })

  console.log(inningsOneData);
  const inningsOneOver = inningsOneData[inningsOneData.length - 1].innings_over.split('_')[1];
  const inningsOneScore = inningsOneData[inningsOneData.length - 1].innings_score;
  const inningsoneWickets = inningsOneData[inningsOneData.length - 1].innings_wickets;
  const inningsOver = matchResults.data[matchResults.data.length - 1].innings_over.split('_')[1];
  const inningsScore = matchResults.data[matchResults.data.length - 1].innings_score;
  const inningsWickets = matchResults.data[matchResults.data.length - 1].innings_wickets;
  console.log(isteamTwoBatting);
  return (
    <>
      <Card sx={{ boxShadow: 0 }}>
        {/* <Card> */}
        <CardContent>
          <Typography sx={{ fontSize: 26, textAlign: "center" }} color="text.primary" gutterBottom>
            {title}
          </Typography>

          <Grid container spacing={2} sx={{
            alignItems: "center"
          }}>
            <Grid item xs={5}>
              <img src={team1Logo} alt="" width="100%" />
              <div>
                <Typography sx={{ fontSize: 18,  textAlign: "center" }} color="text.primary" gutterBottom>
                  {(inningsOneScore + '/' + inningsoneWickets)}
                </Typography>
                <Typography sx={{ fontSize: 15, fontWeight: 'light', textAlign: "center" }} color="text.primary" gutterBottom> {
                  "(" + inningsOneOver + ")"}
                </Typography>
              </div>
            </Grid>
            <Grid item xs={2}>
              <Typography sx={{ fontSize: 24, fontWeight: "bold" }} color="text.primary" gutterBottom>
                VS
              </Typography>
            </Grid>
            <Grid item xs={5}>
              <img src={team2Logo} alt="" width="100%" />
              <div>
                <Typography sx={{ fontSize: 18, textAlign: "center" }} color="text.primary" gutterBottom>
                  {!isteamTwoBatting && "(Yet To Bat)"}
                  {isteamTwoBatting && (inningsScore + '/' + inningsWickets)}
                </Typography>
                <Typography sx={{ fontSize: 15,textAlign: "center", fontWeight: 'light' }} color="text.primary" gutterBottom> {
                  isteamTwoBatting && "(" + inningsOver + ")"}
                </Typography>
              </div>
            </Grid>
            <Grid item xs={1}></Grid>
            <Grid item xs={10}>
              {title === "Today's Match" ?
                (<PredictionComponent
                  team1={team1}
                  team2={team2}
                  team1percentage={team1prob} />)
                : null}
            </Grid>
            <Grid item xs={1}></Grid>
          </Grid>
        </CardContent>
      </Card>
    </>
  )
}

MatchCard.defaultProps = {
  title: '',
  team1: '',
  team2: '',
  team1prob: 100,
  matchResults: {
    data: [{
      innings_over: '1'
    }]
  },
}
export default MatchCard;