import Chart from "chart.js";
import moment from "moment";

class Settings {
  private _apiPlotBase: string = "";
  public get apiPlotBase(): string { return this._apiPlotBase; }

  public configure(
    apiPlotBase: string,
    momentDefaultFormat: string,
  ) : void {
    this._apiPlotBase = apiPlotBase;
    moment.defaultFormat = momentDefaultFormat;
    Chart.defaults.global.defaultFontColor = "#363636";
    Chart.defaults.global.defaultFontFamily = "'Source Sans Pro', sans-serif";
    Chart.defaults.global.defaultFontSize = 12;
  }
};


export const conf = new Settings();
