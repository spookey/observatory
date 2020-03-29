import moment from "moment";

/* allow moment config from outside */
(window as any).momentConfig = (format: string) => {
  moment.defaultFormat = format;
};

/* convert moment timestamps */
export function momentTime(): void {
  document.addEventListener("DOMContentLoaded", (): void => {

    function convert(element: HTMLElement) {
      if (!element.dataset.value || !element.innerHTML) { return; }
      const value: number = parseInt(element.dataset.value, 10);
      if (Number.isNaN(value)) { return; }

      function assign(conv: string) {
        element.title = element.innerHTML.trim();
        element.innerHTML = conv;
      }

      if (element.classList.contains("relative")) {
        assign(moment(value).fromNow());
      } else if (element.classList.contains("absolute")) {
        assign(moment(value).format());
      }
    }

    for (const element of document.querySelectorAll(".moment") as any) {
      convert(element);
    }
  });
}
