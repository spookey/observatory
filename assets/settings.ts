import Chart from "chart.js";
import moment from "moment";


class Settings {
  private store: DOMStringMap = {};
  constructor() {
    for (const script of document.getElementsByTagName("script") as any) {
      this.store = { ...this.store, ...script.dataset };
    }
  }

  public get apiPlotBaseUrl(): string { return this.store.apiPlotBaseUrl || ""; }
  public get apiPlotRefreshMs(): number { return parseInt(this.store.apiPlotRefreshMs || "0", 10); }
  public get momentDefaultFormat(): string { return this.store.momentDefaultFormat || ""; }
  public get momentMsecondFormat(): string { return this.store.momentMsecondFormat || ""; }
  public get momentSecondFormat(): string { return this.store.momentSecondFormat || ""; }
  public get momentMinuteFormat(): string { return this.store.momentMinuteFormat || ""; }
  public get momentHourFormat(): string { return this.store.momentHourFormat || ""; }
  public get momentDayFormat(): string { return this.store.momentDayFormat || ""; }
  public get momentWeekFormat(): string { return this.store.momentWeekFormat || ""; }
  public get momentMonthFormat(): string { return this.store.momentMonthFormat || ""; }
  public get momentQuarterFormat(): string { return this.store.momentQuarterFormat || ""; }
  public get momentYearFormat(): string { return this.store.momentYearFormat || ""; }


  public initialize(): void {
    Chart.defaults.global.defaultFontColor = "#363636";
    Chart.defaults.global.defaultFontFamily = "'Source Sans Pro', sans-serif";
    Chart.defaults.global.defaultFontSize = 12;
    moment.defaultFormat = this.momentDefaultFormat;
  }
};


export default new Settings();
