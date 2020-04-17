import Chart from "chart.js";
import moment from "moment";


export function drawCharts(): void {
  document.addEventListener("DOMContentLoaded", (): void => {
    function getCtx(element: HTMLElement): (CanvasRenderingContext2D | null) {
      if (!element.dataset.slug) { return null; }
      if (!(element instanceof HTMLCanvasElement)) { return null; }
      return (element as HTMLCanvasElement).getContext("2d");
    }

    function draw(element: HTMLElement): void {
      const ctx: (CanvasRenderingContext2D | null) = getCtx(element);
      if (!ctx) { return; }
    }

    for (const element of document.querySelectorAll(".chart") as any) {
      draw(element);
    }
  });
}
