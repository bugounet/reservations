/**
 * Created by bugounet on 07/02/2020.
 */
import { createMuiTheme, makeStyles, ThemeProvider } from '@material-ui/core/styles';
import { blue } from '@material-ui/core/colors';
const theme = createMuiTheme({
    palette: {
        primary: blue,
    },
});

export default theme;