import axios from "axios";
import moment from "moment";
import Chart from "chart.js";
import { AxiosError } from "axios";
import { AxiosRequestConfig } from "axios";
import { AxiosResponse } from "axios";
import { ChartConfiguration } from "chart.js";
import { ChartDataSets } from "chart.js";

import conf from "./settings";
import { lighten } from "./colors";
import { soften } from "./colors";


const baseChartConfig = (): ChartConfiguration => ({
  type: "line",
  options: {
    scales: {
      xAxes: [{
        type: "time",
        time: {
          displayFormats: {
            millisecond: conf.momentMsecondFormat,
            second: conf.momentSecondFormat,
            minute: conf.momentMinuteFormat,
            hour: conf.momentHourFormat,
            day: conf.momentDayFormat,
            week: conf.momentWeekFormat,
            month: conf.momentMonthFormat,
            quarter: conf.momentQuarterFormat,
            year: conf.momentYearFormat,
          },
          isoWeekday: true,
          tooltipFormat: conf.momentDefaultFormat,
        },
        ticks: {
          autoSkip: true,
          maxRotation: 60,
        },
      }],
      yAxes: [{
        type: "linear",
        ticks: {
          beginAtZero: true,
        },
      }],
    },
    responsive: true,
    aspectRatio: 2.0,
  },
});


class Graph {
  private slug: string;
  private bar: HTMLProgressElement;
  private chart: Chart;
  private config: AxiosRequestConfig = {
    baseURL: conf.apiPlotBaseUrl,
    method: 'get',
    responseType: "json",
    timeout: 10 * 1000,
  }

  constructor(
    slug: string,
    bar: HTMLProgressElement,
    ctx: CanvasRenderingContext2D,
  ) {
    this.slug = slug;
    this.bar = bar;
    this.chart = new Chart(ctx, baseChartConfig());
  }

  private attach(payload: ChartDataSets[]): void {
    if (!this.chart.data || !this.chart.data.datasets) { return; }
    this.chart.data.datasets = [];

    for (const idx in payload) {
      if (payload.hasOwnProperty(idx)) {
        const obj: ChartDataSets = payload[idx];
        if (obj.borderColor) {
          obj.borderColor = soften(obj.borderColor as string);
          obj.backgroundColor = lighten(obj.borderColor as string);
        }
        this.chart.data.datasets[idx] = obj;
      }
    }

    this.chart.update({duration: 0});
  }

  private showBar(): void { this.bar.classList.remove("is-invisible"); }
  private hideBar(): void { this.bar.classList.add("is-invisible"); }

  private refresh(): void {
    this.showBar();

    axios.get(this.slug, this.config)
      .then((res: AxiosResponse): void => {
        this.attach(res.data as ChartDataSets[]);
      })
      .catch((err: AxiosError): void => {
        // tslint:disable-next-line
        console.error(err);
      })
      .finally((): void => {
        this.hideBar();
      });
  }

  public loop(): void {
    this.refresh();
  }
}


export function drawCharts(): void {
  document.addEventListener("DOMContentLoaded", (): void => {
    function getSlug(container: HTMLElement): (string | null) {
      if (!container.dataset.slug) { return null; }
      return container.dataset.slug;
    }

    function getBar(container: HTMLElement): (HTMLProgressElement | null) {
      for (const element of container.getElementsByTagName("progress") as any) {
        if (element instanceof HTMLProgressElement) {
          return element;
        }
      }
      return null;
    }

    function getCtx(container: HTMLElement): (CanvasRenderingContext2D | null) {
      for (const element of container.getElementsByTagName("canvas") as any) {
        if (element instanceof HTMLCanvasElement) {
          return (element as HTMLCanvasElement).getContext("2d");
        }
      }
      return null;
    }

    function plot(container: HTMLElement): void {
      const slug: (string | null) = getSlug(container);
      if (!slug) { return; }
      const bar: (HTMLProgressElement | null) = getBar(container);
      if (!bar) { return; }
      const ctx: (CanvasRenderingContext2D | null) = getCtx(container);
      if (!ctx) { return; }

      new Graph(slug, bar, ctx).loop();
    }

    for (const container of document.querySelectorAll(".plot") as any) {
      plot(container);
    }
  });
}
