import Chart from "chart.js";
import moment from "moment";


class Settings {
  private store: DOMStringMap = {};
  constructor() {
    for (const script of document.getElementsByTagName("script") as any) {
      this.store = { ...this.store, ...script.dataset };
    }
  }

  public get apiPlotBase(): string {
    return this.store.apiPlotBase || "";
  }
  public get momentDefaultFormat(): string {
    return this.store.momentDefaultFormat || "";
  }


  public initialize(): void {
    Chart.defaults.global.defaultFontColor = "#363636";
    Chart.defaults.global.defaultFontFamily = "'Source Sans Pro', sans-serif";
    Chart.defaults.global.defaultFontSize = 12;
    moment.defaultFormat = this.momentDefaultFormat;
  }
};


export default new Settings();
