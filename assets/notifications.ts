/* remove notifications */
export const flashClose = (): void => {
  document.addEventListener("DOMContentLoaded", (): void => {

    const remove = (target: HTMLElement): void => {
      const enclose: (HTMLElement | null) = target.parentElement;
      if (!enclose) { return; }

      enclose.removeChild(target);
      if (enclose.children.length) { return; }

      const section: (HTMLElement | null) = enclose.parentElement;
      if (!section) { return; }

      const parent: (HTMLElement | null) = section.parentElement;
      if (!parent) { return; }

      parent.removeChild(section);
    }

    for (const delButton of document.querySelectorAll(".delete.click") as any) {
      delButton.addEventListener("click", (): void => {

         for (const selector of [".message", ".notification"]) {

          const target: (HTMLElement | null) = delButton.closest(selector);
          if (target) { remove(target); }

        }

      });
    }

  });
}
