import axios from "axios";
import moment from "moment";
import Chart from "chart.js";

import { conf } from "./settings";

class Graph {
  private slug: string;
  private bar: HTMLProgressElement;
  private chart: Chart;

  constructor(
    slug: string,
    bar: HTMLProgressElement,
    ctx: CanvasRenderingContext2D,
  ) {
    this.slug = slug;
    this.bar = bar;
    this.chart = new Chart(ctx, {});
  }

  private showBar(): void { this.bar.classList.remove("is-invisible"); }
  private hideBar(): void { this.bar.classList.add("is-invisible"); }

  public loop(): void {
    this.showBar();
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
