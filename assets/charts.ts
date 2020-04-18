import Chart from "chart.js";
import moment from "moment";


export function drawCharts(): void {
  document.addEventListener("DOMContentLoaded", (): void => {
    function getCtx(container: HTMLElement): (CanvasRenderingContext2D | null) {
      for (const element of container.getElementsByTagName("canvas") as any) {
        if (element instanceof HTMLCanvasElement) {
          return (element as HTMLCanvasElement).getContext("2d");
        }
      }
      return null;
    }

    function plot(container: HTMLElement): void {
      const ctx: (CanvasRenderingContext2D | null) = getCtx(container);
      if (!ctx) { return; }
    }

    for (const container of document.querySelectorAll(".plot") as any) {
      plot(container);
    }
  });
}
