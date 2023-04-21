import { ThemeProvider } from '@emotion/react';
import { colors } from '@mui/material';
import { createTheme, responsiveFontSizes } from '@mui/material/styles';
import React from 'react';
import './App.css';
import Header from './components/layout/header';
import PageContent from './components/pageContent';

let theme = createTheme({
  palette:{
    secondary: {
      main: colors.orange[500],
    },
    MI: {
      main: colors.lightBlue[500],
    },
    RCB: {
      main: colors.red.A700
    },
    CSK: {
      main: colors.yellow[500]
    },
    KKR: {
      main: colors.deepPurple[500]
    },
    SRH: {
      main: colors.orange[600]
    },
    DC: {
      main: colors.indigo[800]
    },
    PK: {
      main: colors.pink.A700
    },
    RR: {
      main: colors.blue.A700
    },
    LSG: {
      main: colors.lightBlue.A700
    },
    GT: {
      main: colors.blueGrey.A700
    }
  },
})

theme = responsiveFontSizes(theme);

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={theme}>
        <Header/>
        <PageContent />
      </ThemeProvider>
    </div>
  )
}

export default App;
