import axios from "axios";
import Chart from "chart.js";
import moment from "moment";
import { AxiosError } from "axios";
import { AxiosRequestConfig } from "axios";
import { AxiosResponse } from "axios";
import { ChartConfiguration } from "chart.js";
import { ChartDataSets } from "chart.js";

import "chartjs-plugin-zoom";

import conf from "./settings";
import { colorizeFG } from "./colors";
import { colorLighten } from "./colors";
import { colorParse } from "./colors";
import { colorSoften } from "./colors";
import { dropAttach } from "./dropdowns";
import { momentRel } from "./moments";

interface DisplayInfo {
  plain: object;
  logic: {
    color: string,
    epoch: number,
    stamp: string,
  };
}

interface DispChartDataSets extends ChartDataSets {
  display?: DisplayInfo;
};


const baseChartConfig = (): ChartConfiguration => ({
  type: "line",
  options: {
    aspectRatio: 2.0,
    responsive: true,
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
    plugins: {
      zoom: {
        pan: {
          enabled: true,
          mode: "x",
        },
        zoom: {
          enabled: true,
          drag: false,
          mode: "x",
          speed: 0.01,
        },
      },
    },
  },
});


class Graph {
  private slug: string;
  private bar: HTMLProgressElement;
  private template: HTMLTemplateElement;
  private bucket: HTMLElement;
  private chart: Chart;

  private config: AxiosRequestConfig = {
    baseURL: conf.apiPlotBaseUrl,
    method: "get",
    responseType: "json",
    timeout: 10 * 1000,
  };

  constructor(
    slug: string,
    bar: HTMLProgressElement,
    template: HTMLTemplateElement,
    bucket: HTMLElement,
    context: CanvasRenderingContext2D,
  ) {
    this.slug = slug;
    this.bar = bar;
    this.template = template;
    this.bucket = bucket;
    this.chart = new Chart(context, baseChartConfig());
  }

  private showBar() { this.bar.classList.remove("is-invisible"); }
  private hideBar() { this.bar.classList.add("is-invisible"); }
  private showBucket() { this.bucket.classList.remove("is-hidden"); }
  private hideBucket() { this.bucket.classList.add("is-hidden"); }
  private dropdownBucket() { dropAttach(this.bucket); }
  private clearBucket() {
    for (const child of this.bucket.children as any) {
      this.bucket.removeChild(child);
    }
  }

  private paint(display: DisplayInfo): void {
    const clone: HTMLTemplateElement =
      this.template.cloneNode(true) as HTMLTemplateElement;

    function set(sect: string, name: string, value: string): void {
      const sel: string = `span.${sect}-${name}`;
      for(const elem of clone.content.querySelectorAll(sel) as any) {
        if (elem instanceof HTMLElement) {
          elem.replaceWith(document.createTextNode(value));
        }
      }
    }

    for (const [name, value] of Object.entries(display.plain) as any) {
      set('plain', name, (value as string));
    }

    for(const elem of clone.content.querySelectorAll('.color-value') as any) {
      colorizeFG(elem, colorParse(display.logic.color));
    }
    for(const elem of clone.content.querySelectorAll('.moment-value') as any) {
      momentRel(elem, display.logic.epoch, display.logic.stamp);
    }

    this.bucket.appendChild(clone.content);
    clone.classList.remove("is-hidden");
  }

  private attach(payload: DispChartDataSets[]): void {
    if (!this.chart.data || !this.chart.data.datasets) { return; }
    this.chart.data.datasets = [];

    for (const idx in payload) {
      if (payload.hasOwnProperty(idx)) {
        const obj: DispChartDataSets = payload[idx];
        if (obj.borderColor) {
          obj.borderColor = colorSoften(obj.borderColor as string);
          obj.backgroundColor = colorLighten(obj.borderColor as string);
        }
        if (obj.display) {
          this.paint(obj.display);
          delete obj.display;
        }
        this.chart.data.datasets[idx] = obj;
      }
    }

    this.chart.update({duration: 0});
  }

  private refresh(): void {
    this.showBar();
    this.hideBucket();
    this.clearBucket();

    axios.get(this.slug, this.config)
      .then((res: AxiosResponse): void => {
        this.attach(res.data as DispChartDataSets[]);
      })
      .catch((err: AxiosError): void => {
        // tslint:disable-next-line
        console.error(err);
      })
      .finally((): void => {
        this.hideBar();
        this.dropdownBucket();
        this.showBucket();
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

    function getBar(
      container: HTMLElement): (HTMLProgressElement | null
    ) {
      for (
        const element of container.getElementsByTagName("progress") as any
      ) {
        if (element instanceof HTMLProgressElement) {
          return element;
        }
      }
      return null;
    }

    function getTemplate(
      container: HTMLElement): (HTMLTemplateElement | null
    ) {
      for (
        const element of container.getElementsByTagName("template") as any
      ) {
        if (element instanceof HTMLTemplateElement) {
          return element;
        }
      }
      return null;
    }

    function getBucket(
      container: HTMLElement): (HTMLElement | null
    ) {
      for (
        const element of container.getElementsByClassName("bucket") as any
      ) {
        if (element instanceof HTMLElement) {
          return element;
        }
      }
      return null;
    }

    function getContext(
      container: HTMLElement): (CanvasRenderingContext2D | null
    ) {
      for (
        const element of container.getElementsByTagName("canvas") as any
      ) {
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
      const template: (HTMLTemplateElement | null) = getTemplate(container);
      if (!template) { return; }
      const bucket: (HTMLElement | null) = getBucket(container);
      if (!bucket) { return; }
      const context: (CanvasRenderingContext2D | null) = getContext(container);
      if (!context) { return; }

      new Graph(slug, bar, template, bucket, context).loop();
    }

    for (const container of document.querySelectorAll(".plot") as any) {
      plot(container);
    }
  });
}
