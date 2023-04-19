import { PaletteColor, PaletteColorOptions } from "@mui/material/styles";
import React from "react";

declare module '@mui/material/styles' {
    interface Palette{
        MI?: PaletteColor,
        RCB?: PaletteColor,
        CSK?:PaletteColor,
        KKR?:PaletteColor,
        SRH?:PaletteColor,
        DC?:PaletteColor,
        PK?:PaletteColor,
        RR?:PaletteColor,
    }
    interface PaletteOptions{
        MI?: PaletteColorOptions,
        RCB?: PaletteColorOptions,
        CSK?: PaletteColorOptions,
        KKR?: PaletteColorOptions,
        SRH?: PaletteColorOptions,
        DC?: PaletteColorOptions,
        PK?: PaletteColorOptions,
        RR?: PaletteColorOptions
    }
}
  