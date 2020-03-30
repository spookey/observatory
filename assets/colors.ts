import Color from "color";

/* set background color of select options */
export function colorizeSO(): void {
  document.addEventListener("DOMContentLoaded", (): void => {

    function colorize(element: HTMLElement): void {
      if (!(element instanceof HTMLOptionElement)) { return; }
      const value = parseInt(element.value, 10);
      if (Number.isNaN(value)) { return; }

      element.style.color = Color('#ffffff').string();
      element.style.backgroundColor = Color(value).string();
    }

    for (const element of document.querySelectorAll('select') as any) {
      if (element.dataset.colorize) {
        for (const elem of element.querySelectorAll('option') as any) {
          colorize(elem);
        }
      }
    }
  });
}
