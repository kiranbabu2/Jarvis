import { Box, Grid, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import MatchCard from "./matchCard";
import SecondaryMatchCard from "./secondaryMatchCard";
import Papa, { ParseResult } from "papaparse"

const PageContent = () => {

  type Data = {
    matchType: string,
    Team1: string,
    Team2: string,
    predicted_team1: number,
    predicted_team2: number,
  }

  type Plot = {
    plot1: string,
    plot2: string
  }

  type Values = {
    data: Data[]
  }

  const zeroData = {
    matchType: '',
    Team1: '',
    Team2: '',
    predicted_team1: 0,
    predicted_team2: 0,
  }

  const defaultPlot = {
    plot1: '',
    plot2: '',
  }

  const [values, setValues] = useState<Values | undefined>()
  const [currentMatch, setCurrentMatch] = useState <Data>(zeroData)
  const [plots, setPlots] = useState<Plot>(defaultPlot)
  // const [previousMatch, setPreviousMatch] = useState<Data>(zeroData)
  // const [nextMatch, setNextMatch] = useState<Data>(zeroData)

  const getCurrentMatch = async () => {
    const response = await fetch('https://api.github.com/repos/kiranbabu2/Jarvis/contents/current_matches.csv', {
      method: 'get',
      headers: new Headers({
        'Authorization': 'token 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'
      })
    })
    console.log(response);
    const parsedResponse = await new Response(response.body).json();
    const encodedContent = parsedResponse.content;
    console.log(encodedContent);
    var decodedContent = atob(encodedContent);
    return decodedContent;
  }
  const listFiles = async () => {
    const response = await fetch('https://api.github.com/repos/kiranbabu2/Jarvis/contents/data/', {
      method: 'get',
      headers: new Headers({
        'Authorization': 'token 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'
      })
    })
    const parsedResponse = await new Response(response.body).json();
    return parsedResponse;
  }

  const getCharts = async () => {
    const streamPlot1 = await fetch('https://api.github.com/repos/kiranbabu2/Jarvis/contents/plot_3.png', {
      method: 'get',
      headers: new Headers({
        'Authorization': 'token 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'
      })
    });

    const plot1= `data:image/png;base64, ` + (await new Response(streamPlot1.body).json()).content;

    const streamPlot2 = await fetch('https://api.github.com/repos/kiranbabu2/Jarvis/contents/plot_1.png', {
      method: 'get',
      headers: new Headers({
        'Authorization': 'token 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'
      })
    })

    const plot2 = `data:image/png;base64, ` + (await new Response(streamPlot2.body).json()).content;
    
    setPlots({plot1, plot2});
  }
  const getCSV = async () => {
    // get current match
    const currentMatch = await getCurrentMatch();
    const currentMatchIds = currentMatch.split('\n').splice(1,2);

    // get all matches data files
    const files = await listFiles();
    const allMatchIds = files.map((file: { name: string; }) => {
      return file.name.split('_')[0];
    })
    let currentMatchId = currentMatchIds[0];
    // find correct match id
    if(allMatchIds.indexOf(currentMatchIds[1]) > -1) {
      currentMatchId = currentMatchIds[1];
    } 
    // make call and get csv data
    const response = await fetch(`https://api.github.com/repos/kiranbabu2/Jarvis/contents/data/${currentMatchId}_results.csv`, {
      method: 'get',
      headers: new Headers({
        'Authorization': 'token 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'
      })
    })


   
    console.log(response);
    const parsedResponse = await new Response(response.body).json();
    const encodedContent = parsedResponse.content;
    console.log(encodedContent);
    var decodedContent = atob(encodedContent);
    console.log(decodedContent);
    const file = new File([decodedContent], "data.csv", {
      type: "text/csv",
    });
    Papa.parse(file, {
      header: true,
      download: true,
      skipEmptyLines: true,
      delimiter: ",",
      complete: (results: ParseResult<Data>) => {
        getCharts()
        console.log('results: ', results)
        results.data[results.data.length - 1].predicted_team1 = Math.floor(results.data[results.data.length - 1].predicted_team1 * 100);
        setValues(results)
        setCurrentMatch(results.data[results.data.length - 1]);
      },
    })
  }

  useEffect(() => {
    getCSV()
  }, [])


  return (
    <>
      <Box sx={{ mt: 5, mx: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4} sx={{ opacity: 0.5 }}>
            {/* <MatchCard
                            title="Previous Match"
                            team1={previousMatch.team1}
                            team2={previousMatch.team2}
                            team1prob={previousMatch.team1ProbRavens} /> */}
          </Grid>
          <Grid item xs={12} md={4}>
            <MatchCard
              title="Today's Match"
              team1={currentMatch.Team1}
              team2={currentMatch.Team2}
              team1prob={currentMatch.predicted_team1} />
          </Grid>
          <Grid item xs={12} md={4} sx={{ opacity: 0.5 }}>
            {/* <MatchCard
                            title="Next Match"
                            team1={nextMatch.team1}
                            team2={nextMatch.team2}
                            team1prob={nextMatch.team1ProbRavens} /> */}
          </Grid>
          <Grid item xs={12} md={6}>
            <SecondaryMatchCard
                            title="Chart 1"
                            plot={plots.plot1} />
          </Grid>
          <Grid item xs={12} md={6}>
            <SecondaryMatchCard
                            title="Chart 2"
                            plot={plots.plot2} />
          </Grid>
        </Grid>
      </Box>
      <Typography sx={{ mt: 5, mx: 3, textAlign: "end" }}>www.ravens.lilly.com</Typography>
    </>
  )
}

export default PageContent;