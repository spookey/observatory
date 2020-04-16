import Chart from "chart.js";
import moment from "moment";

/* allow configuration from outside */
export function doSettings(
  momentDefaultFormat: string
) : void {

  moment.defaultFormat = momentDefaultFormat;

  Chart.defaults.global.defaultFontColor = "#363636";
  Chart.defaults.global.defaultFontFamily = "'Source Sans Pro', sans-serif";
  Chart.defaults.global.defaultFontSize = 12;
};
