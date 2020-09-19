import moment from "moment";

export enum MomentMode {
  none = 0,
  relative,
  absolute,
}

const momentSet = (elem: HTMLElement, value: string, title: string) => {
  const span: HTMLElement = document.createElement("span");
  span.title = title;
  span.appendChild(document.createTextNode(value));
  elem.replaceWith(span);
}

const momentValue = (value: number, mode: MomentMode): (string | null) => {
  if (!Number.isNaN(value)) {
    if (mode === MomentMode.relative) { return moment(value).fromNow(); }
    if (mode === MomentMode.absolute) { return moment(value).format(); }
  }
  return null;
}

export const momentRel = (
  elem: HTMLElement, value: number, title: string
): void => {
  const val: (string | null) = momentValue(value, MomentMode.relative);
  if (!val) { return; }
  momentSet(elem, val, title);
}

/* convert moment timestamps */
export const momentTime = (): void => {
  document.addEventListener("DOMContentLoaded", (): void => {

    const getMode = (classList: DOMTokenList): MomentMode => {
      if (classList.contains("relative")) { return MomentMode.relative; }
      if (classList.contains("absolute")) { return MomentMode.absolute; }
      return MomentMode.none;
    }

    const convert = (element: HTMLElement) => {
      if (!element.dataset.value || !element.innerHTML) { return; }

      const value: (string | null) = momentValue(
        parseInt(element.dataset.value, 10),
        getMode(element.classList)
      );
      if (!value) { return; }

      momentSet(element, value, element.innerHTML.trim());
    }

    for (const element of document.querySelectorAll(".moment") as any) {
      convert(element);
    }
  });
}
