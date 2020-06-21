import Color from "color";

const WHITE: Color = Color(0xffffff);

export function colorParse(value: string): (Color | null) {
  try { return Color(value); }
  catch(err) { return null; }
}

export function colorizeFG(element: HTMLElement, color: (Color | null)): void {
  if (!color) { return; }

  element.style.backgroundColor = color.string();
  element.style.color = WHITE.string();
}

/* set background color of select options */
export function colorizeSO(): void {
  document.addEventListener("DOMContentLoaded", (): void => {

    function colorize(element: HTMLElement): void {
      if (!(element instanceof HTMLOptionElement)) { return; }
      if (!element.value) { return; }

      colorizeFG(element, colorParse(element.value));
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


function colorAlpha(value: string, factor: number): (Color | null) {
  const color: (Color | null) = colorParse(value);
  if (!color) { return null; }
  return color.alpha(factor);
}

export function colorSoften(value: string): string {
  const color: (Color | null) = colorAlpha(value, 0.9);
  if (!color) { return value; }
  return color.string();
}

export function colorLighten(value: string): string {
  const color: (Color | null) = colorAlpha(value, 0.2);
  if (!color) { return value; }
  return color.lighten(0.7).string();
}
