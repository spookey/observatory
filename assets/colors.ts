import Color from "color";

const WHITE: Color = Color('#ffffff');


function create(value: string): (Color | null) {
  const num: number = parseInt(value, 10);
  if (Number.isNaN(num)) { return null; }
  return Color(num);
}

function assign(element: HTMLElement, color: (Color | null)): void {
  if (!color) { return; }
  element.style.color = WHITE.string();
  element.style.backgroundColor = color.string();
}


/* set background color of select options */
export function colorizeSO(): void {
  document.addEventListener("DOMContentLoaded", (): void => {

    function colorize(element: HTMLElement): void {
      if (!(element instanceof HTMLOptionElement)) { return; }
      if (!element.value) { return; }

      assign(element, create(element.value));
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


/* set background color of span texts */
export function colorizeTX(): void {
  document.addEventListener("DOMContentLoaded", (): void => {

    function colorize(element: HTMLElement): void {
      if (!element.dataset.value) { return; }

      assign(element, create(element.dataset.value));
    }

    for (const element of document.getElementsByClassName("colorize") as any) {
      colorize(element);
    }
  });
}
